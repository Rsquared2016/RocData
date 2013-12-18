package in.fount.tools;

import in.fount.model.mobile.Tweet;

import java.util.ArrayList;
import java.util.List;

import org.ektorp.CouchDbConnector;
import org.ektorp.CouchDbInstance;
import org.ektorp.Options;
import org.ektorp.Page;
import org.ektorp.PageRequest;
import org.ektorp.Revision;
import org.ektorp.ViewQuery;
import org.ektorp.http.HttpClient;
import org.ektorp.http.StdHttpClient;
import org.ektorp.impl.StdCouchDbConnector;
import org.ektorp.impl.StdCouchDbInstance;

public class OriginalRevision {
    private static HttpClient httpClient;
    
    public OriginalRevision() throws Exception {

        // --- Connect to couchDB
        CouchDbInstance dbInstance = new StdCouchDbInstance(httpClient);
        CouchDbConnector tweets = new StdCouchDbConnector("nyc_app", dbInstance);

        // --- First thing: build the request query.
        int q = 2000;
        PageRequest pageRequest = PageRequest.firstPage(q);

        ViewQuery query = new ViewQuery().designDocId("_design/Tweet")
            .viewName("rev").includeDocs(true).staleOkUpdateAfter();

        // --- Page through all the tweets that haven't been traced.
        int i = 0;
        Page<Tweet> result = tweets.queryForPage(
                query,
                pageRequest,
                Tweet.class);
        
        
        while (i==0 || result.getNextPageRequest() != null) {
        	System.out.println("processing :: "+ i*pageRequest.getPageSize() +" - "+ (i+1)*pageRequest.getPageSize() + " / "+result.getTotalSize());
        	List<Object> bulkRevert = new ArrayList<Object>();
            
        	for (Tweet tweet : result) {
                    
        		//Get all of the revisions for each document.
        		List<Revision> revs = tweets.getRevisions(tweet.getId());
        		
        		if(revs.size()>1 && tweet.getText().toLowerCase().contains("now saying")){
        			//Retrieve the original rev
	        		Options options = new Options().revision(revs.get(revs.size()-1).getRev());
	        		tweet = tweets.get(Tweet.class, tweet.getId(),options);

	        		//Set that version to the current
	        		tweet.setRevision(revs.get(0).getRev());
	        		
	        		//Queue for updating
	        		bulkRevert.add(tweet);
        		}
            }
            
        	//Update the bulk docs.
        	System.out.println(bulkRevert.size());
        	tweets.executeBulk(bulkRevert);
            
            
            try{
            result = tweets.queryForPage(
                    query,
                    result.getNextPageRequest(),
                    Tweet.class);
            }catch(NullPointerException e){
                result = tweets.queryForPage(
                        query,
                        PageRequest.firstPage(q),
                        Tweet.class);
                
                System.out.println("Got Old");    
            }
            i++;
        }        
    }

    public static void main(String[] args) {
        try {
            httpClient = new StdHttpClient.Builder().url(
            		"http://192.237.163.178:5984").build();
            
            System.out.println("hi");
            new OriginalRevision();
            System.out.println("bye");
            
            httpClient.shutdown();
        
        } catch (Exception e) {
            System.out.println(e.toString());
        }
    }

}

package in.fount.tools;

import java.util.List;
import org.ektorp.CouchDbConnector;
import org.ektorp.CouchDbInstance;
import org.ektorp.ViewQuery;
import org.ektorp.http.HttpClient;
import org.ektorp.http.StdHttpClient;
import org.ektorp.impl.StdCouchDbConnector;
import org.ektorp.impl.StdCouchDbInstance;
import in.fount.model.diseases.DiseaseTweetLightweight;

public class Reindex {
    private static HttpClient httpClient;
    
    public Reindex() throws Exception {

    	@SuppressWarnings("unused")
        final String DESIGN_TWEET = "_design/Tweet";
    	final String DESIGN_DISEASES = "_design/DiseaseTweetLightweight";

        // --- Connect to couchDB
        CouchDbInstance dbInstance = new StdCouchDbInstance(httpClient);

        // --- Index NYC
        @SuppressWarnings("unused")
        CouchDbConnector tweets = new StdCouchDbConnector("nyc2010", dbInstance);
        @SuppressWarnings("unused")
        String[] ViewsNYC = {"all","days","by_day","by_date"};

        // --- Index Diseases
        CouchDbConnector diseases = new StdCouchDbConnector("diseases_new", dbInstance);
        String[] ViewsDiseases = {
        			"all","stats","by_quad",
        			"by_quad_disease_term","by_quad_disease_term_hour",
        			"by_quad_disease_hour","by_quad_disease_hour_1","by_quad_disease_hour_2","by_quad_disease_hour_3","by_quad_disease_hour_4","by_quad_disease_hour_5","by_quad_disease_hour_6","by_quad_disease_hour_7","by_quad_disease_hour_8","by_quad_disease_hour_9","by_quad_disease_hour_10","by_quad_disease_hour_11","by_quad_disease_hour_12",
        			"by_quad_disease_term_hour","by_quad_disease_term_hour_1","by_quad_disease_term_hour_2","by_quad_disease_term_hour_3","by_quad_disease_term_hour_4","by_quad_disease_term_hour_5","by_quad_disease_term_hour_6","by_quad_disease_term_hour_7","by_quad_disease_term_hour_8","by_quad_disease_term_hour_9","by_quad_disease_term_hour_10","by_quad_disease_term_hour_11","by_quad_disease_term_hour_12",
        			};

        for(String view: ViewsDiseases){
	        // --- Setup the view
        	ViewQuery query = new ViewQuery()
	        	.designDocId(DESIGN_DISEASES)
	            .viewName(view)
	            .includeDocs(false)
	            .staleOkUpdateAfter();

	        // --- Reindex the view
	        @SuppressWarnings("unused")
            List<DiseaseTweetLightweight> result = diseases.queryView(
	                query,
	                DiseaseTweetLightweight.class);
        }

    }

    public static void main(String[] args) {
        try {
            httpClient = new StdHttpClient.Builder().url(
            "http://roc.cs.rochester.edu:5984").build();
            
            System.out.println("hi");
            new Reindex();
            System.out.println("bye");
            
            httpClient.shutdown();
        
        } catch (Exception e) {
            System.out.println(e.toString());
        }
    }

}
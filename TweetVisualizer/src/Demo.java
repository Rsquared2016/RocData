//License: GPL. Copyright 2008 by Jan Peter Stotz
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import org.openstreetmap.gui.jmapviewer.events.JMVCommandEvent;
import org.openstreetmap.gui.jmapviewer.interfaces.JMapViewerEventListener;
import org.openstreetmap.gui.jmapviewer.interfaces.TileLoader;
import org.openstreetmap.gui.jmapviewer.interfaces.TileSource;
import org.openstreetmap.gui.jmapviewer.tilesources.BingAerialTileSource;
import org.openstreetmap.gui.jmapviewer.tilesources.OsmTileSource;
import org.openstreetmap.gui.jmapviewer.*;
import org.ektorp.*;
import org.ektorp.http.HttpClient;
import org.ektorp.http.StdHttpClient;
import org.ektorp.impl.StdCouchDbConnector;
import org.ektorp.impl.StdCouchDbInstance;
import org.ektorp.support.View;


/**
 *
 * Demonstrates the usage of {@link JMapViewer}
 *
 * @author Jan Peter Stotz
 * edited and adapted by: John Hinkel and Vedant Ahluwalia
 *
*/
public class Demo extends JFrame implements JMapViewerEventListener  {

    private static final long serialVersionUID = 1L;

    private static JMapViewerTree treeMap = null;

    private JLabel zoomLabel=null;
    private JLabel zoomValue=null;

    private JLabel mperpLabelName=null;
    private JLabel mperpLabelValue = null;
	static volatile String[] parsedLats;
	static volatile String[] parsedLongs;
	static volatile String[] tweetids;
	static volatile String[] temp = null;
	static ArrayList<ImageMarker> imageMarkers = new ArrayList<ImageMarker>();
	static volatile String username = "";
	static volatile String content = "";
	//static volatile Database[] db;
	static volatile CouchDbConnector[] db2;
	static volatile Layer[] DBx;
	static ImageMarker[] locs;
	static int choice;
	static String dbaseUser;
	static String dbasePass;
    /**
     * Constructs the {@code Demo}.
     * @param dbs 
     * @param choice 
     */
    @SuppressWarnings({ "rawtypes", "unchecked" })
	public Demo(final String[] dbs) {
        super("TweetVisualizer");
        setSize(400, 400);

        treeMap = new JMapViewerTree("Zones");

        // Listen to the map viewer for user operations so components will
        // recieve events and update
        map().addJMVListener(this);
       

        setLayout(new BorderLayout());
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        JPanel panel = new JPanel();
        JPanel panelTop = new JPanel();
        final JPanel panelBottom = new JPanel();
        JPanel helpPanel = new JPanel();
        
        mperpLabelName=new JLabel("Meters/Pixels: ");
        mperpLabelValue=new JLabel(String.format("%s",map().getMeterPerPixel()));

        zoomLabel=new JLabel("Zoom: ");
        zoomValue=new JLabel(String.format("%s", map().getZoom()));

        add(panel, BorderLayout.NORTH);
        add(helpPanel, BorderLayout.SOUTH);
        panel.setLayout(new BorderLayout());
        panel.add(panelTop, BorderLayout.NORTH);
        panel.add(panelBottom, BorderLayout.SOUTH);
        JLabel helpLabel = new JLabel("Use right mouse button to move,\n "
                + "left double click or mouse wheel to zoom.");
        helpPanel.add(helpLabel);
        JButton button = new JButton("setDisplayToFitMapMarkers");
        button.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                map().setDisplayToFitMapMarkers();
            }
        });
        JComboBox tileSourceSelector = new JComboBox(new TileSource[] { 
                new OsmTileSource.CycleMap(), new BingAerialTileSource()});
        tileSourceSelector.addItemListener(new ItemListener() {
            public void itemStateChanged(ItemEvent e) {
                map().setTileSource((TileSource) e.getItem());
            }
        });
        panelBottom.add(tileSourceSelector);
        //map().setTileSource(new BingAerialTileSource());
        map().setTileSource(new OsmTileSource.CycleMap());
        JComboBox tileLoaderSelector;
        try {
            tileLoaderSelector = new JComboBox(new TileLoader[] { new OsmFileCacheTileLoader(map()),
            new OsmTileLoader(map()) });
        } catch (IOException e) {
            tileLoaderSelector = new JComboBox(new TileLoader[] { new OsmTileLoader(map()) });
        }
        tileLoaderSelector.addItemListener(new ItemListener() {
            public void itemStateChanged(ItemEvent e) {
                map().setTileLoader((TileLoader) e.getItem());
            }
        });
        map().setTileLoader((TileLoader) tileLoaderSelector.getSelectedItem());
       
        final JCheckBox showMapMarker = new JCheckBox("Map markers visible");
        showMapMarker.setSelected(map().getMapMarkersVisible());
        showMapMarker.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                map().setMapMarkerVisible(showMapMarker.isSelected());
            }
        });
        panelBottom.add(showMapMarker);
        
        final JCheckBox showTreeLayers = new JCheckBox("Tree Layers visible");
        showTreeLayers.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                treeMap.setTreeVisible(showTreeLayers.isSelected());
            }
        });
        panelBottom.add(showTreeLayers);
       
        final JCheckBox showTileGrid = new JCheckBox("Tile grid visible");
        showTileGrid.setSelected(map().isTileGridVisible());
        showTileGrid.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                map().setTileGridVisible(showTileGrid.isSelected());
            }
        });
        panelBottom.add(showTileGrid);
        final JCheckBox showZoomControls = new JCheckBox("Show zoom controls");
        showZoomControls.setSelected(map().getZoomContolsVisible());
        showZoomControls.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                map().setZoomContolsVisible(showZoomControls.isSelected());
            }
        });
        panelBottom.add(showZoomControls);
       
        map().setScrollWrapEnabled(true);
       
        final JLabel Loading = new JLabel("Loading tweet details....");
        Loading.setForeground(Color.red);
        Loading.setSize(20,40);
        Loading.setVisible(false);
        
        panelBottom.add(button);
        panelBottom.add(Loading);

        panelTop.add(zoomLabel);
        panelTop.add(zoomValue);
        panelTop.add(mperpLabelName);
        panelTop.add(mperpLabelValue);

        add(treeMap, BorderLayout.CENTER);
        
        map().addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
            	
                if (e.getButton() == MouseEvent.BUTTON1) {
                	boolean allLayersActive = true;
                	for(int i=0;i<DBx.length;i++){
                		if(DBx[i].isVisible() == false){
                			allLayersActive = false;
                			break;
                		}
                	}
                	if(allLayersActive){
                		map().getAttribution().handleAttribution(e.getPoint(), true);
                		//get latitude and longitude of the point you click on
                		Coordinate mouselatlong;
                		mouselatlong = map().getPosition(e.getX(),e.getY());
                		//JOptionPane.showMessageDialog(null, mouselatlong.toString());

                		//establish the "hot zone" for clicking.... i.e. it counts as having clicked on the marker if the mouse
                		//latitude and longitude are within .1 of the latitude and longitude stored in couchdb
                		double latlowbound = mouselatlong.getLat() - .01;
                		double lathighbound = mouselatlong.getLat() + .01;
                		double lonlowbound = mouselatlong.getLon() - .01;
                		double lonhighbound = mouselatlong.getLon() + .01; 
                		
                		String matchingid = "";

                		
                		//for every latitude and longitude number, compare it to the mouse position.  If there's a match, return
                		//the tweetid that corresponds to that coordinate.
                		for (int i=1;i<imageMarkers.size();i++){
                			try{                				
                				if(Double.compare(imageMarkers.get(i).getLat(), lathighbound)<0 && Double.compare(imageMarkers.get(i).getLat(), latlowbound) > 0){
                					if(Double.compare(imageMarkers.get(i).getLon(), lonhighbound)<0 && Double.compare(imageMarkers.get(i).getLon(), lonlowbound) > 0){
                						matchingid = imageMarkers.get(i).getID();
                						break;
                					}
                				}
                			}
                			catch (Exception e2){

                			}
                		}
                		                		                		                		                	
                		ViewResult results[] = new ViewResult[dbs.length];
                		//if the user actually clicked on a marker, display that info to the user.
                		if (matchingid != ""){                    	
                				//queries database and returns info for clicked-on tweet
                				
                				for(int i=0;i<dbs.length;i++){
                					//gets all documents from the database.
                            		ViewQuery alldocs = new ViewQuery();
                            		alldocs.allDocs();    		
                            		    		        	    		
                            		ViewResult docs = db2[Integer.parseInt(dbs[i])].queryView(alldocs);

                            		ViewQuery q = new ViewQuery();
                            		//sets up a query for the view that each database has for the matchingid (limited to 50,000 tweets).
                            		if(docs.getRows().get(0).toString().contains("_design")) {
                            			q.designDocId(docs.getRows().get(0).getId());
                                		q.viewName(q.getDesignDocId().substring(q.getDesignDocId().indexOf("/")+1, q.getDesignDocId().length()));
                                		q.key(matchingid);
                                		q.limit(50000);
                            		}
                            		else {
                            			q.designDocId(docs.getRows().get(1).getId());
                                		q.viewName(q.getDesignDocId().substring(q.getDesignDocId().indexOf("/")+1, q.getDesignDocId().length()));
                                		q.key(matchingid);
                                		q.limit(50000);
                            		}
//                					//queries the view
                            		results[i] = db2[Integer.parseInt(dbs[i])].queryView(q);
                				}
                				//string processing for the username and tweet content
                				for(int i=0;i<dbs.length;i++){
                						if (results[i].getRows().toString().contains("[]}") == false && results[i].getRows().toString().equals("[]") == false){
                						
                							temp = results[i].getRows().toString().split("\"username\":\"");
                							temp = temp[1].toString().split("\"");
                							
                								
                						}
                						                					
                				}
                				username = temp[0];
                				content = temp[4];
                	
                				
                				JOptionPane.showMessageDialog(null, "Username: " + username + "\n" + "Tweet Content: " + content + "\n","Tweet Details", getDefaultCloseOperation(), null);
                				
                		}

                	}
                }
            }
        });

        map().addMouseMotionListener(new MouseAdapter() {
            @Override
            public void mouseMoved(MouseEvent e) {
                Point p = e.getPoint();
                boolean cursorHand = map().getAttribution().handleAttributionCursor(p);
                if (cursorHand) {
                    map().setCursor(new Cursor(Cursor.HAND_CURSOR));
                } else {
                    map().setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
                }
               
            }
        });
        try {
        	InitializeTwitter(dbs);
        }
        catch(Exception e) {
        	JOptionPane.showMessageDialog(null, "Error:  database not added to server in correct format.");
        	System.exit(0);
        }
        
    }
    private void InitializeTwitter(String[] dbs) {

    	HttpClient httpClient = null;
		try {
			if (choice == 1){
				httpClient = new StdHttpClient.Builder().build();
	    	}
	    	else{
	    		httpClient = new StdHttpClient.Builder().url("http://192.237.163.178:5984").username(dbaseUser).password(dbasePass).build();
	    	}
			
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
    	CouchDbInstance dbInstance = new StdCouchDbInstance(httpClient);
    	
    	//get list of databases from couchdb
    	List<String> databasenames = dbInstance.getAllDatabases();
    	
    	//parse out the databases we don't need to view
    	if(choice!=1){
    		//parse out the databases we don't need to view
    		databasenames.remove(databasenames.indexOf("_users"));
    		databasenames.remove(databasenames.indexOf("_replicator"));    	
    		databasenames.remove(databasenames.indexOf("test_suite_db"));
    		databasenames.remove(databasenames.indexOf("test_suite_db/with_slashes"));
    		databasenames.remove(databasenames.indexOf("test_suite_db_c"));
    		databasenames.remove(databasenames.indexOf("test_suite_foobar"));
    		databasenames.remove(databasenames.indexOf("test_suite_reports"));    	    	
    	}
    	else{
    		databasenames.remove(databasenames.indexOf("_users"));
    		databasenames.remove(databasenames.indexOf("_replicator"));
    	}
    	
    	//convert the array list to an array.
    	Object[] ParsedDatabasenames = databasenames.toArray();
    	

    	//initialize all databases and layers.
    	db2 = new CouchDbConnector[ParsedDatabasenames.length];

    	DBx = new Layer[ParsedDatabasenames.length];
    	for(int i=0;i<db2.length;i++){    		
    		db2[i] = new StdCouchDbConnector(ParsedDatabasenames[i].toString(), dbInstance);    		
    		DBx[i] = treeMap.addLayer(ParsedDatabasenames[i].toString());    		
    	}
    	
    	//array of potential dot colors.
    	File f = new File("Images/");
    	File[] icons = f.listFiles();
    	System.out.println(icons[0].getPath());
    	String[] dotColorURL = {icons[0].getPath(),icons[1].getPath(),icons[2].getPath(), icons[3].getPath(),icons[4].getPath(), icons[5].getPath(), icons[6].getPath()};
    	
    	//for each database, that view that it contains, and then pass the results of running that view to the plotPoints method.
    	for(int i=0; i<dbs.length;i++){
    		//gets all documents from the database.
    		ViewQuery alldocs = new ViewQuery();
    		alldocs.allDocs();    		
    		    		        	    		
    		ViewResult docs = db2[Integer.parseInt(dbs[i])].queryView(alldocs);

    		ViewQuery q = new ViewQuery();
    		//set up the query for the view that each database contains
    		if(docs.getRows().get(0).toString().contains("_design")) {
    			q.designDocId(docs.getRows().get(0).getId());
        		q.viewName(q.getDesignDocId().substring(q.getDesignDocId().indexOf("/")+1, q.getDesignDocId().length()));
        		q.limit(50000);
    		}
    		else {
    			q.designDocId(docs.getRows().get(1).getId());
        		q.viewName(q.getDesignDocId().substring(q.getDesignDocId().indexOf("/")+1, q.getDesignDocId().length()));
        		q.limit(50000);
    		}
    		
        	String viewpath = ""; 
        	//passes the result of the query to the plotPoints method        	
        	ViewResult TweetQueryResult = db2[Integer.parseInt(dbs[i])].queryView(q);
        
        	try {
        	plotPoints(TweetQueryResult,DBx[Integer.parseInt(dbs[i])],dotColorURL[i%7]);
        	}
        	catch(Exception e) {
        		JOptionPane.showMessageDialog(null, "Error:  database not added to server in correct format.");
            	System.exit(0);
        	}
    	} 
    	
		
	}
	public static ImageMarker[] plotPoints(ViewResult tweetQueryResult, Layer DBx, String URL) {
				
		//next five lines sets up array of Lats and Longs for parsing.
		String Lats[] = tweetQueryResult.getRows().toString().split("latitude\":");
		String Longs[] = tweetQueryResult.getRows().toString().split("longitude\":");	    	    	
    	parsedLats = new String[Lats.length];
    	parsedLongs = new String[Longs.length];
    	locs = new ImageMarker[Lats.length];
    	tweetids = tweetQueryResult.getRows().toString().split("key\":\"");
    	for(int i=1;i<tweetids.length;i++){
    		tweetids[i] = tweetids[i].substring(0,32);
    	}
    	    	
    	//regex matcher that actually grabs the latitude and longitude numbers from the strings.
    	for(int i=1;i<Lats.length;i++){
    		Pattern p = Pattern.compile("(\\+|-)?([0-9]+(\\.[0-9]+))");
    		Matcher m = p.matcher(Lats[i]);
    		try{
    		m.find();
    		parsedLats[i] = m.group();
    		}
    		catch(Exception e){
    		parsedLats[i] = "";	
    		}
    		try{
    			m.find();
    			parsedLongs[i] = m.group();
    		}
    		catch(Exception e){
    			parsedLongs[i] = "";
    		}
    		//plots the points on the map and sets marker colors.
    		if(parsedLats[i]!= "" && parsedLongs[i] != ""){
    			                        
            	locs[i] = new ImageMarker(DBx, Double.parseDouble(parsedLats[i]),Double.parseDouble(parsedLongs[i]), URL, tweetids[i]);    			
    			map().addMapMarker(locs[i]);
    					    			
    		}   

    	}
    	//sorts the image markers according to their lattitude
    	Collections.addAll(imageMarkers, locs);
    	Collections.sort(imageMarkers,new Comparator<ImageMarker>(){
			@Override
			public int compare(ImageMarker o1, ImageMarker o2) {
				if (o1==null || o2==null){
					return -1;
				}else{
				return Double.compare(o1.getLat(),o2.getLat());
				}
			}
			    	
    	});
    	return locs;		
	}
	private static JMapViewer map(){
        return treeMap.getViewer();
    }
    
	@SuppressWarnings("unused")
	private static Coordinate c(double lat, double lon){
        return new Coordinate(lat, lon);
    }
    
    /**
     * @param args
     */
    public static void main(String[] args) {
    	try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (ClassNotFoundException | InstantiationException
				| IllegalAccessException | UnsupportedLookAndFeelException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
    	choice = JOptionPane.showConfirmDialog(null, "Do you want to connect to the server?", "Connect to server?", JOptionPane.YES_NO_OPTION);
    	if (choice != 1) {
    		dbaseUser = JOptionPane.showInputDialog("Database Username:");
    		dbasePass = JOptionPane.showInputDialog("Database Password:");
    	}
    	HttpClient httpClient = null;
		try {
			if (choice == 1){
				httpClient = new StdHttpClient.Builder().build();
	    	}
	    	else{
	    		httpClient = new StdHttpClient.Builder().url("http://192.237.163.178:5984").username(dbaseUser).password(dbasePass).build();
	    	}
			
		} catch (Exception e) {
			JOptionPane.showMessageDialog(null, "Error.  Incorrect database username/password or local database has not been started");
			System.exit(0);
		}
    	CouchDbInstance dbInstance = new StdCouchDbInstance(httpClient);
    	List<String> databasenames = null;
    	try {
    	 databasenames = dbInstance.getAllDatabases();
    	}
    	catch(Exception e) {
    		JOptionPane.showMessageDialog(null, "Error.  Incorrect database username or password");
			System.exit(0);
    	}
    	

    	if(choice!=1){
    		//parse out the databases we don't need to view
    		databasenames.remove(databasenames.indexOf("_users"));
    		databasenames.remove(databasenames.indexOf("_replicator"));    	
    		databasenames.remove(databasenames.indexOf("test_suite_db"));
    		databasenames.remove(databasenames.indexOf("test_suite_db/with_slashes"));
    		databasenames.remove(databasenames.indexOf("test_suite_db_c"));
    		databasenames.remove(databasenames.indexOf("test_suite_foobar"));
    		databasenames.remove(databasenames.indexOf("test_suite_reports"));    	    	
    	}
    	else{
    		databasenames.remove(databasenames.indexOf("_users"));
    		databasenames.remove(databasenames.indexOf("_replicator"));
    	}
    	
    	//convert the array list to an array.
    	String names = null;
    	Object[] ParsedDatabasenames = databasenames.toArray();
    	for (int i=0;i<ParsedDatabasenames.length;i++){
    		if (names != null){
    			names = names + Integer.toString(i)+"= " + ParsedDatabasenames[i] + " ";
    		}
    		else{
    			names = Integer.toString(i)+"= " + ParsedDatabasenames[i] + " ";
    		}
    		if (i==(ParsedDatabasenames.length/2)){
    			names = names + "\n";
    		}
    	}
    	
    	//have the user enter the databases they want to see.
    	String[] dbs = JOptionPane.showInputDialog("Please enter the databases you want displayed, separated by a comma.\n" + names).split(",");    	

    	JOptionPane.showMessageDialog(null, "Please wait while the map renders.  could take up to 7 minutes...");
    	new Demo(dbs).setVisible(true);    	
                
    }
   
    private void updateZoomParameters() {
        if (mperpLabelValue!=null)
            mperpLabelValue.setText(String.format("%s",map().getMeterPerPixel()));
        if (zoomValue!=null);
            zoomValue.setText(String.format("%s", map().getZoom()));
    }

    @Override
    public void processCommand(JMVCommandEvent command) {
        if (command.getCommand().equals(JMVCommandEvent.COMMAND.ZOOM) ||
                command.getCommand().equals(JMVCommandEvent.COMMAND.MOVE)) {
            updateZoomParameters();
        }
    }    
    
}


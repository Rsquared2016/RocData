import org.openstreetmap.gui.jmapviewer.events.JMVCommandEvent;
import org.openstreetmap.gui.jmapviewer.interfaces.JMapViewerEventListener;
import org.openstreetmap.gui.jmapviewer.interfaces.MapMarker;
import org.openstreetmap.gui.jmapviewer.interfaces.MapPolygon;
import org.openstreetmap.gui.jmapviewer.interfaces.TileLoader;
import org.openstreetmap.gui.jmapviewer.tilesources.BingAerialTileSource;
import org.openstreetmap.gui.jmapviewer.*;

import java.awt.AlphaComposite;
import java.awt.Color;
import java.awt.Composite;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;

import javax.imageio.ImageIO;

public class ImageMarker extends MapObjectImpl implements MapMarker {

    private Coordinate coord;
    private String ImageURL;
    private STYLE markerStyle;
    private String id;
    
    private BufferedImage img = null;
    public ImageMarker(Coordinate coord, String ImageURL, String id) {
        this(null, null, coord, ImageURL, id);
        
        try {
    	    img = ImageIO.read(new File(ImageURL));
    	} catch (IOException e) {
    	}
    }
    public ImageMarker(String name, Coordinate coord, String ImageURL, String id) {
        this(null, name, coord, ImageURL, id);

        try {
    	    img = ImageIO.read(new File(ImageURL));
    	} catch (IOException e) {
    	}
    }
    public ImageMarker(Layer layer, Coordinate coord, String ImageURL, String id) {
        this(layer, null, coord, ImageURL, id);

        try {
    	    img = ImageIO.read(new File(ImageURL));
    	} catch (IOException e) {
    	}
    }
    public ImageMarker(double lat, double lon, String ImageURL, String id) {
        this(null, null, new Coordinate(lat,lon), ImageURL, id);

        try {
    	    img = ImageIO.read(new File(ImageURL));
    	} catch (IOException e) {
    	}
    }
    public ImageMarker(Layer layer, double lat, double lon, String ImageURL, String id) {
        this(layer, null, new Coordinate(lat,lon), ImageURL, id);

        try {
    	    img = ImageIO.read(new File(ImageURL));
    	} catch (IOException e) {
    	}
    }
    public ImageMarker(Layer layer, String name, Coordinate coord, String ImageURL, String id) {
        this(layer, name, coord, ImageURL, STYLE.VARIABLE, getDefaultStyle(), id);

        try {
    	    img = ImageIO.read(new File(ImageURL));
    	} catch (IOException e) {
    	}
    }
    public ImageMarker(Layer layer, String name, Coordinate coord, String ImageURL, STYLE markerStyle, Style style, String id) {
        super(layer, name, style);
        this.markerStyle = markerStyle;
        this.coord = coord;
        this.ImageURL = ImageURL;
        this.id = id;
        
    }

    public Coordinate getCoordinate(){
        return coord;
    }
    public double getLat() {
        return coord.getLat();
    }
    public String getID(){
    	return id;
    }
    public double getLon() {
        return coord.getLon();
    }

    public String getImageURL() {
        return ImageURL;
    }
    public void setImageURL(String imageLoc){
    	ImageURL = imageLoc;
    }
    public STYLE getMarkerStyle() {
        return markerStyle;
    }

    public void paint(Graphics g, Point position, int radio) {
    	
    	g.drawImage(img, position.x-14, position.y-14, 29, 29, null);
    
        if(getLayer()==null||getLayer().isVisibleTexts()) paintText(g, position);
        
    }

    public static Style getDefaultStyle(){
        return new Style(Color.ORANGE, new Color(200,200,200,200), null, getDefaultFont());
    }
    @Override
    public String toString() {
        return "MapMarker at " + getLat() + " " + getLon();
    }
    @Override
    public void setLat(double lat) {
        if(coord==null) coord = new Coordinate(lat,0);
        else coord.setLat(lat);
    }
    @Override
    public void setLon(double lon) {
        if(coord==null) coord = new Coordinate(0,lon);
        else coord.setLon(lon);
    }
	@Override
	public double getRadius() {
		// TODO Auto-generated method stub
		return 0;
	}
}

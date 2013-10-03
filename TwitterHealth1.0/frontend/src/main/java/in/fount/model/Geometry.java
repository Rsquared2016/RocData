package in.fount.model;

import java.util.ArrayList;

public class Geometry{
	private String type="Point";
	private ArrayList<Double> coordinates;

	// --- Getters & Setters
	public String getType(){ return type;}
	public void setType(String s){type=s;}

	public ArrayList<Double> getCoordinates(){ return coordinates;}
	public void setCoordinates(ArrayList<Double> d){coordinates = d;}
}
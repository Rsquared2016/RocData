function(doc) {
    if (doc.created_at && doc.geo.coordinates.length==2) {
        var date = new Date(doc.created_at);
        var lat = doc.geo.coordinates[0];
        var lon = doc.geo.coordinates[1];
        if (lat >= 40.583 && lat <= 40.930 && lon <= -73.567 && lon >= -74.206) {
        	emit([date.getUTCFullYear(), date.getUTCMonth() + 1, date.getUTCDate()], 1);
    	}
    }
}
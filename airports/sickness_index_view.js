function(doc) {
    
    function calcDistance(lat1, lon1, lat2, lon2) {                      
        var rad = 0.017453292519943;
        var yDistance = (lat2 - lat1) * 60.00721;
        var xDistance = (Math.cos(lat1 * rad) + Math.cos(lat2 * rad)) * (lon2 - lon1) * 30.053965;
        var distance = Math.sqrt( yDistance*yDistance + xDistance*xDistance );
        return Math.round(distance * 1852.00088832);
    }

    var dist = -1;
    var closestCityID = "?";

    var centers = [
      [42.3644,-71.059,"BOS"], // Boston
      [40.716667,-74.00,"NYC"], // NYC
      [33.995,-118.063,"LA"], //LA
      [51.514,-0.122,"LON"], //London
      [47.577,-122.229,"SEA"], // Seattle
      [37.566,-122.327,"SF"] // SF
    ];

    if (doc.geo.coordinates.length == 2) {
      var minDist = 999999999;
      for (var i=0; i<centers.length; i++) {
        dist = calcDistance(doc.geo.coordinates[0], doc.geo.coordinates[1], centers[i][0], centers[i][1]);
        if (dist < minDist) {
          minDist = dist;
          closestCityID = centers[i][2];
        }
      }
    }

    if (doc.health > 0.8) {
       var nd = new Date(doc.created_at);    
       //emit([doc.from_user, nd.getUTCFullYear(), nd.getUTCMonth() + 1, nd.getUTCDate(), closestCityID], 1);
       emit([closestCityID, nd.getUTCFullYear(), nd.getUTCMonth() + 1, nd.getUTCDate()], doc.health);
    }
}
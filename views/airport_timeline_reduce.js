function(key, values, rereduce) {
    var vals = (function() {
        var thisVals = [];
        for(var i = 0; i < values.length; i++) {
            if(!rereduce) {
                var airport = values[i][0];
                var date_str = values[i].slice(1, 4).join("-");
                thisVals = thisVals.concat(airport + " " + date);
            } else {
                var thisVal = values[i].split(", ");
                thisVals = thisVals.concat(thisVal);
            }
        }
        return thisVals;
    })();

    var ports = [];
    for(var i = 0; i < vals.length; i++) {
        if(ports.indexOf(vals[i]) < 0) {
            ports.push(vals[i]);
        }
    }
    return ports.join(", ").sort();
}
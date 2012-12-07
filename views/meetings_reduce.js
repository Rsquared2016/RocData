function(key, values, rereduce) {
    var vals = (function() {
        if(!rereduce) {
            return values;
        } else {
            var thisVals = [];
            for(var i = 0; i < values.length; i++) {
                var thisVal = values[i].split(", ");
                thisVals = thisVals.concat(thisVal);
            }
            return thisVals;
        }
    })();

    var ids = [];
    for(var i = 0; i < vals.length; i++) {
        if(ids.indexOf(vals[i]) < 0) {
            ids.push(vals[i]);
        }
    }
    return ids.join(", ");
}
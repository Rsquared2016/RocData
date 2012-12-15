function(key, values, rereduce) {
    var vals = (function() {
        var pairs = [];
        for(var i = 0; i < values.length; i++) {
            if(!rereduce)
                // we get: [[airport, timeStr], ... ]
                pairs.push(values[i][0] + " && " + values[i][1]);
            else
                // we get: "airport && timeStr || ... "
                pairs = pairs.concat(values[i].split(" || "));
        }
        return pairs;
    })();

    var pairs = [];
    for(var i = 0; i < vals.length; i++)
        if(pairs.indexOf(vals[i]) < 0)
            pairs.push(vals[i]);
    pairs.sort(function(a, b) {
        var aTimeStr = a.split(" && ")[1], bTimeStr = b.split(" && ")[1];
        return (new Date(aTimeStr).getTime() - new Date(bTimeStr).getTime());
    });
    return pairs.join(" || ");
}
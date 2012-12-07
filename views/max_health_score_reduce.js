function(key, values, rereduce) {
    var max_risk = values[0];
    for(var i = 1; i < values.length; i++)
        max_risk = Math.max(max_risk, values[i]);
    return max_risk;
}
function(doc) {
    if (doc.created_at && doc.geo.coordinates.length==2) {
        var date = new Date(doc.created_at);
        emit([date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()], 1);
    }
}
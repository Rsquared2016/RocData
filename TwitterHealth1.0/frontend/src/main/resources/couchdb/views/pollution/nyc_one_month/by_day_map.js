function(doc) {
    if (doc.created_at && doc.health > .5) {
        var date = new Date(doc.created_at);
        emit([date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()], 1);
    }
}
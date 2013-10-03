function(doc) {
    var date;
    if (doc.health > .18 && doc.created_at) {
        date = new Date(doc.created_at);
        emit([date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()], 1);
    }
}
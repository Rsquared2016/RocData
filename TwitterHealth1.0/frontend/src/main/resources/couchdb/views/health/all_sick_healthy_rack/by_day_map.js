function(doc) {
    if (doc.health > .18 && doc.created_at ) {
        var date = new Date(doc.created_at);
        emit([date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()], doc);
    }
}
function(doc) {
    if(doc.airport) {
        var d = new Date(doc.created_at);
        emit([doc.airport, d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()], doc.from_user_id_str);
    }
}
function(doc) {
    if(doc.airport && doc.created_at) {
        var d = new Date(doc.created_at);
        var dateStr = d.toISOString().replace("T", " ");
        dateStr = dateStr.substring(0, dateStr.length - 5);
        emit([doc.from_user_id_str, dateStr], doc.airport);
    }
}
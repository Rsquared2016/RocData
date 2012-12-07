function(doc) {
    if(doc.from_user_id_str && doc.created_at && doc.health) {
        var d = new Date(doc.created_at);
        emit([doc.from_user_id_str, d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()], doc.health);
    }
}
function(doc) {
    if (doc.geo) {
        emit(null, doc._id);
    }
};
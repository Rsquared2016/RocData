function(doc){
	if (doc.created_at && doc.geo!=null) {
		var date = new Date(doc.created_at);
		emit([doc.taxonomy.disease, doc.taxonomy.terms, date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), 1],1);
	}
}
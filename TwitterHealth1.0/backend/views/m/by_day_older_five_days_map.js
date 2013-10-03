function(doc) {
	if (doc.created_at) {
		var date = new Date(doc.created_at);
		var diff = (new Date()).getTime() - date.getTime();
		if (diff >= 432000000) { // doc is older than 5 days
			emit([date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()], 1);
		}
	}
}
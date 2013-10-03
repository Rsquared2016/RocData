function(doc) {
    if(doc._id == doc.id_str && doc.geo && doc.created_at) {
        // default bbox coords
        var rootSw = [22.000, -123.000];
        var rootNe = [50.000, -65.000];
        var maxDepth = 1;
        
        // helper for finding quad id
        function findQuad(geo, sw, ne, id, depth) {
            if(depth >= maxDepth) {
                return id;
            }
            
            // find quadsection coords
            var slat = sw[0], wlng = sw[1];
            var nlat = ne[0], elng = ne[1];
            var mlat = (nlat + slat) / 2.0, mlng = (elng + wlng) / 2.0;
            var glat = geo.coordinates[0], glng = geo.coordinates[1];
            // 0: SW quad
            if(glat < mlat && glng < mlng) {
                id[depth] = 0;
                var nextSw = [slat, wlng];
                var nextNe = [mlat, mlng];
                return findQuad(geo, nextSw, nextNe, id, depth + 1);
            }
            // 1: SE quad
            else if(glat < mlat && glng >= mlng) {
                id[depth] = 1;
                var nextSw = [slat, mlng];
                var nextNe = [mlat, elng];
                return findQuad(geo, nextSw, nextNe, id, depth + 1);
            }
            // 2: NE quad
            else if(glat >= mlat && glng >= mlng) {
                id[depth] = 2;
                var nextSw = [mlat, mlng];
                var nextNe = [nlat, elng];
                return findQuad(geo, nextSw, nextNe, id, depth + 1);
            }
            // 3: NW quad
            else if(glat >= mlat && glng < mlng) {
                id[depth] = 3;
                var nextSw = [mlat, wlng];
                var nextNe = [nlat, mlng];
                return findQuad(geo, nextSw, nextNe, id, depth + 1);
            }
        }
        
        // get quad ID, date if in original bounding box
        var olat = doc.geo.coordinates[0], olng = doc.geo.coordinates[1];
        if(olat >= rootSw[0] && olat <= rootNe[0] && olng >= rootSw[1] && olng <= rootNe[1]) {
            var date = new Date(doc.created_at);
            var infokey = [
                           date.getUTCFullYear(),
                           date.getUTCMonth(),
                           date.getUTCDate()
                           ];
            var quadkey = findQuad(doc.geo, rootSw, rootNe, [], 0);
            emit(infokey.concat(quadkey).concat([doc.taxonomy.disease, doc.taxonomy.terms, date.getUTCHours()]), 1);
        }
    }
}
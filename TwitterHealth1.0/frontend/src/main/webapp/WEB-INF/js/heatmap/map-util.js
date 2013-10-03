define([], function() {
    return {
        formatTime: function(millis) {
            var date = new Date(millis);
            return date.toString("HH:mm");
        },
        getNyBounds: function() {
            var psw = new google.maps.LatLng(40.467597, -74.409908);
            var pne = new google.maps.LatLng(41.046156, -73.548989);
            return nybounds = new google.maps.LatLngBounds(psw, pne);
        }
    };
});

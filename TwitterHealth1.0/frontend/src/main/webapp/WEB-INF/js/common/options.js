// Options 
// ----------------
// These contain any configuration details for the app

define([], function() {
    return {
        mapStyle: {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 11,
            minZoom: 5,
            scrollwheel: true,
            draggable: true,
            panControl: false,
            mapTypeControl: false,
            streetViewControl: false,
            scaleControl: false,
            disableDoubleClickZoom: false,
            styles: [
              {
                "featureType": "road",
                "elementType": "labels.icon",
                "stylers": [
                  { "visibility": "off" }
                ]
              },{
                "featureType": "administrative",
                "stylers": [
                  { "visibility": "off" }
                ]
              },{
                "featureType": "water",
                "stylers": [
                  { "color": "#3ba7db" },
                  { "lightness": 49 }
                ]
              },{
                "featureType": "poi",
                "stylers": [
                  { "visibility": "off" }
                ]
              },{
                "featureType": "transit",
                "stylers": [
                  { "visibility": "off" }
                ]
              },{
                "featureType": "landscape.natural"  },{
                "featureType": "road.highway",
                "stylers": [
                  { "color": "#505050" },
                  { "visibility": "simplified" }
                ]
              },{
                "featureType": "road.arterial",
                "stylers": [
                  { "color": "#787878" },
                  { "visibility": "simplified" }
                ]
              },{
              }
            ],
            zoomControl: true,
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL
            },
            draggableCursor: 'default'
        }
    };
});


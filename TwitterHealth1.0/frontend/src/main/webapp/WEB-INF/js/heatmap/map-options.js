define([], function() {
    return {
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: false,
        scrollwheel: true,
        draggable: true,
        navigationControl: false,
        mapTypeControl: true,
        scaleControl: false,
        disableDoubleClickZoom: false,
        styles: [{
            stylers: [{
                invert_lightness: true
            }, {
                saturation: -56
            }, {
                lightness: -56
            }, {
                visibility: "simplified"
            }]
        }, {
            featureType: "road",
            stylers: [{
                visibility: "simplified"
            }, {
                lightness: -34
            }, {
                saturation: -44
            }, {
                hue: "#00f6ff"
            }]
        }, {
            featureType: "road",
            elementType: "labels",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "water",
            stylers: [{
                hue: "#0066ff"
            }, {
                invert_lightness: true
            }, {
                saturation: -68
            }, {
                lightness: -71
            }]
        }],
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL
        },
        draggableCursor: 'default'
    };
});

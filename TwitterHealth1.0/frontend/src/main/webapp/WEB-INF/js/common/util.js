// Util
// ----------------
// some common global utility functions 
define([],
    function() {
        return {
            isValidLocation: function(loc) {
                return loc.lat >= -180.0 && loc.lat <= 180.0 && loc.lng >= -180.0
                    && loc.lng <= 180.0;
            },
            geoToLatLng: function(geo) {
                return new google.maps.LatLng(geo.lat, geo.lng, false);
            },
            coordinatesToLatLng: function(coordinates) {
                var lat = coordinates[0];
                var lng = coordinates[1];
                if (!_.isNumber(lat) || !_.isNumber(lng)) {
                    // log.info("wrong coordinates: [lat: " + lat + ", lng: " +
                    // lng + "]");
                    return null;
                }
                return new google.maps.LatLng(lat, lng, false);
            },
            latLngToGeo: function(latLng) {
                return {
                    lat: latLng.lat(),
                    lng: latLng.lng()
                };
            },
            latLngToCoordinates: function(latLng) {
                return { 'coordinates': [ latLng.lat(), latLng.lng() ] };
            },
            getLatLngBounds: function(bottomLeftLat, bottomLeftLong, topRightLat,
                topRightLong) {
                return new google.maps.LatLngBounds(new google.maps.LatLng(bottomLeftLat,
                    bottomLeftLong), new google.maps.LatLng(topRightLat, topRightLong));
            },
            getBoundsNyc: function() {
                return _.getLatLngBounds(40.467597, -74.409908, 41.046156, -73.548989);
            },
            getBoundsSf: function() {
                return _.getLatLngBounds(37.4857775, -122.8497405, 38.0643365,
                    -121.98882150);
            },
            isInBounds: function(latLng, arg) {
                var inBounds = function(city) {
                    if (city == "nyc")
                        return _.getBoundsNyc().contains(latLng);
                    else if (city == "sf")
                        return _.getBoundsSf().contains(latLng);
                    else
                        return false;
                };
                
                if (_.isArray(arg))
                    return _.all(arg, inBounds);
                else if (_.isString(arg))
                    return inBounds(arg);
                else
                    return false;
            },
            nycDefault: function() {
                return {
                    lat: 40.7566,
                    lng: -73.9863
                };
            },
            sfDefault: function() {
                return {
                    lat: 37.775057,
                    lng: -122.419281
                };
            },
            defaultFor: function(city) {
                if (city == "nyc")
                    return _.nycDefault();
                else if (city == "sf")
                    return _.sfDefault();
                else
                    return null;
            },
            dateToSimple: function(date) {
                return date.toString("yyyy-MM-dd HH:mm:ss");
            },
            simpleToDate: function(simple) {
                return Date.parseExact(simple, "yyyy-MM-dd HH:mm:ss");
            },
            currentTimeAsSimple: function() {
                return _.dateToSimple(new Date());
            },
            dateToTwitterFormat: function(date) {
                return date.toString("ddd, dd MMM yyyy HH:mm:ss O");
            },
            twitterFormatToDate: function(tform) {
                return Date.parseExact(tform.substring(0, tform.length - 6),
                    "ddd, dd MMM yyyy HH:mm:ss");
            },
            currentTimeAsTwitterFormat: function() {
                return _.dateToTwitterFormat(new Date());
            },
            healthToClassification: function(rating) {
                if (rating < .82) {
                    return "Low";
                } else if (rating < 1.02) {
                    return "Medium";
                } else {
                    return "High";
                }
            },
            healthRiskToColor: function(rating) {
                if (rating < .82) {
                    return "#2CBD2A";
                } else if (rating < .86) {
                    return "#BDD55E";
                } else if (rating < .90) {
                    return "#E9E45C";
                } else if (rating < .94) {
                    return "#FBEB5E";
                } else if (rating < .98) {
                    return "#FDCC56";
                } else if (rating < 1.02) {
                    return "#FC9F41";
                } else if (rating < 1.06) {
                    return "#FFBB33";
                } else if (rating < 1.1) {
                    return "#F6573C";
                } else if (rating < 1.14) {
                    return "#F43837";
                } else {
                    return "#F31B33";
                }
            },
            healthToColorClass: function(rating) {
                if (rating < .82) {
                    return "health_01";
                } else if (rating < .86) {
                    return "health_02";
                } else if (rating < .90) {
                    return "health_03";
                } else if (rating < .94) {
                    return "health_05";
                } else if (rating < .98) {
                    return "health_05";
                } else if (rating < 1.02) {
                    return "health_06";
                } else if (rating < 1.06) {
                    return "health_07";
                } else if (rating < 1.1) {
                    return "health_08";
                } else if (rating < 1.14) {
                    return "health_09";
                } else {
                    return "health_10";
                }
            },
            zeroToTwenty_healthToClassification: function(rating) {
                if (rating < 7) {
                    return "Low";
                } else if (rating < 14) {
                    return "Medium";
                } else {
                    return "High";
                }
            },
            zeroToTwenty_healthToColorClass: function(rating) {
                if (rating < 2) {
                    return "health_01";
                } else if (rating < 4) {
                    return "health_02";
                } else if (rating < 6) {
                    return "health_03";
                } else if (rating < 8) {
                    return "health_05";
                } else if (rating < 10) {
                    return "health_05";
                } else if (rating < 12) {
                    return "health_06";
                } else if (rating < 14) {
                    return "health_07";
                } else if (rating < 16) {
                    return "health_08";
                } else if (rating < 18) {
                    return "health_09";
                } else {
                    return "health_10";
                }
            },
            healthRiskToColor: function(rating) {
                if (rating < 2) {
                    return "#2CBD2A";
                } else if (rating < 4) {
                    return "#BDD55E";
                } else if (rating < 6) {
                    return "#E9E45C";
                } else if (rating < 8) {
                    return "#FBEB5E";
                } else if (rating < 10) {
                    return "#FDCC56";
                } else if (rating < 12) {
                    return "#FC9F41";
                } else if (rating < 14) {
                    return "#FFBB33";
                } else if (rating < 16) {
                    return "#F6573C";
                } else if (rating < 18) {
                    return "#F43837";
                } else {
                    return "#F31B33";
                }
            },
            feedbackHealthToColor: function(rating) {
                if (rating < 1) {
                    return "#2CBD2A";
                } else if (rating < 2) {
                    return "#BDD55E";
                } else if (rating < 3) {
                    return "#E9E45C";
                } else if (rating < 4) {
                    return "#FBEB5E";
                } else if (rating < 5) {
                    return "#FDCC56";
                } else if (rating < 6) {
                    return "#FC9F41";
                } else if (rating < 7) {
                    return "#F96D3D";
                } else if (rating < 8) {
                    return "#F6573C";
                } else if (rating < 9) {
                    return "#F43837";
                } else {
                    return "#F31B33";
                }
            },
            imageForHealth: function(health) {
                var retina = window.devicePixelRatio > 1 ? true : false;
                var baseUrl = "/css/images/mobile/map_pins/";
                if (health < 0.4) {
                    return (baseUrl + 'lg_dot_01' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.45) {
                    return (baseUrl + 'lg_dot_02' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.5) {
                    return (baseUrl + 'lg_dot_03' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.55) {
                    return (baseUrl + 'lg_dot_04' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.6) {
                    return (baseUrl + 'lg_dot_05' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.65) {
                    return (baseUrl + 'lg_dot_06' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.7) {
                    return (baseUrl + 'lg_dot_07' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.75) {
                    return (baseUrl + 'lg_dot_08' + (retina ? '@2x' : '') + '.png');
                } else if (health < 0.8) {
                    return (baseUrl + 'lg_dot_09' + (retina ? '@2x' : '') + '.png');
                } else {
                    return (baseUrl + 'lg_dot_10' + (retina ? '@2x' : '') + '.png');
                }
            },
            setLinkWithIcon: function(jElem, text, icon) {
                jElem.html(text + '<i class="' + icon + ' icon-white"></i>')
            },
            setHealthClassification: function(jElem, health_risk) {
                console.log("Health Risk: " + health_risk)
                jElem.text(_.zeroToTwenty_healthToClassification(health_risk));
                jElem.removeClass().addClass(
                    _.zeroToTwenty_healthToColorClass(health_risk));
            },
            setButtonAsActive: function(jElem) {
                jElem.parent().children().each(function() {
                    $(this).removeClass('active');
                });
                $(jElem).addClass('active');
            },
            generateUniqueUserId: function() {
                // props to broofa of StackOverflow
                // http://stackoverflow.com/a/2117523
                return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,
                    function(c) {
                        var r = Math.random() * 16 | 0, v = c == 'x' ? r
                            : (r & 0x3 | 0x8);
                        return v.toString(16);
                    });
            },
            getCookie: function(name) {
                return $.cookies.get(name);
            },
            setCookie: function(name, attr) {
                $.cookies.set(name, attr.value, {
                    expiresAt: attr.max_age || new Date(2112, 1, 1),
                    path: attr.path
                });
            },
            tweetRating: function(attributes) {
                var result = 0;
                if (attributes.indexOf('yes') !== -1) {
                    result = 1;
                } else if (attributes.indexOf('no') !== -1) {
                    result = -1;
                }
                
                return result;
            },
            intersection: function(a, b) {
                var c = [];
                var len = a.length;
                while (len--) {
                    var item = a[len];
                    if (b.indexOf(item) != -1)
                        c.push(item);
                }
                return c;
            },
            padWithLeadingZeros: function(number, numDigits) {
                var str = number + "";
                var strLen = str.length;
                var lenDiff = numDigits - strLen;
                if (lenDiff > 0)
                    while (lenDiff--)
                        str = "0" + str;
                return str;
            },
            calcDistance: function(lat1, lng1, lat2, lng2) {
                var nauticalMilePerLat = 60.00721;
                var nauticalMilePerLongitude = 60.10793;
                var rad = Math.PI / 180.0;
                var milesPerNauticalMile = 1.15078;

                var yDistance = (lat2 - lat1) * nauticalMilePerLat;
                var xDistance = (Math.cos(lat1 * rad) + Math.cos(lat2 * rad))
                        * (lng2 - lng1) * (nauticalMilePerLongitude / 2);

                var distance = Math.sqrt(yDistance * yDistance + xDistance * xDistance);

                return distance * milesPerNauticalMile * 1609.344;
            },
            calcDistanceOptimized: function(lat1, lng1, lat2, lng2) {
                var rad = 0.017453292519943;
                var yDistance = (lat2 - lat1) * 60.00721;
                var xDistance = (Math.cos(lat1 * rad) + Math.cos(lat2 * rad))
                        * (lng2 - lng1) * 30.053965;
                var distance = Math.sqrt(yDistance * yDistance + xDistance * xDistance);
                return distance * 1852.00088832;
            }
        };
    });

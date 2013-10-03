define(['text!/resources/templates/heatmap/button-control.html',
        'text!/resources/templates/heatmap/loading-control.html',
        'text!/resources/templates/heatmap/text-control.html',
        'text!/resources/templates/heatmap/traffic-control.html'], function(button,
    loading, text, traffic) {
    return {
        createButton: function(attr) {
            var wrap = document.createElement("div");
            wrap.innerHTML = _.template(button, attr);
            return wrap;
        },
        
        createLoadingBar: function() {
            var wrap = document.createElement("div");
            wrap.innerHTML = loading;
            return wrap;
        },
        
        createTextControl: function(textParam) {
            var wrap = document.createElement("div");
            wrap.innerHTML = _.template(text, textParam);
            return wrap;
        },
        
        createTrafficControl: function() {
            var wrap = document.createElement("div");
            wrap.innerHTML = traffic;
            return wrap;
        }
    };
});

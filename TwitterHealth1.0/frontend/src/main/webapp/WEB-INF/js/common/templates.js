define(['text!/resources/templates/common/player-control.html'], function(playerControl) {
    return {
        createPlayerControl: function() {
            var wrap = document.createElement("div");
            wrap.innerHTML = playerControl;
            return wrap;
        }
    };
});

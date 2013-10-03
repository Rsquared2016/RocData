define(["map-util", "map-controls"], function(mapUtil, controls) {
    return {
        radius: 15,
        visible: true,
        opacity: 60,
        showTimeCallback: function(time) {
            $(".text-control", controls.clockControl).text(
                "Time: " + mapUtil.formatTime(time));
        },
        framesPerHour: 2,
        initialState: "play",
        cityBounds: mapUtil.getNyBounds(),
        taskCallback: function(task, text) {
            setTimeout(function() {
                task();
            }, 15);
        },
        animationPeriod: 75,
        animated: true,
        minimumOpacity: 0.6
    };
});

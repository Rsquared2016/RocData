define(["./templates"], function(templates) {
    
    PlayerControl = function(player) {
        this.player = player;
        
        var controlDiv = templates.createPlayerControl();
        
        var playBtn = $("#playButton", controlDiv);
        var prevBtn = $("#previousButton", controlDiv);
        var nextBtn = $("#nextButton", controlDiv);
        
        this.controlDiv = controlDiv;
        this.playBtn = playBtn;
        this.prevBtn = prevBtn;
        this.nextBtn = nextBtn;
        
        // play & pause
        $(playBtn).click({
            player: player,
            control: this
        }, function(event) {
            var player = event.data.player;
            var control = event.data.control;
            if (player.getState() == "play") {
                player.pause();
                control.updateControls();
            } else {
                player.play();
                control.updateControls();
            }
        });
        
        // next
        $(nextBtn).click({
            player: player,
            control: this
        }, function(event) {
            var player = event.data.player;
            if (player.getState() == "pause") {
                player.next();
            }
        });
        
        // previous
        $(prevBtn).click({
            player: player,
            control: this
        }, function(event) {
            var player = event.data.player;
            if (player.getState() == "pause") {
                player.previous();
            }
        });
        
    };
    
    PlayerControl.prototype.updateControls = function() {
        var state = this.player.getState();
        if (state == "pause") {
            $(this.playBtn).removeClass("ui-icon-pause");
            $(this.playBtn).addClass("ui-icon-play");
        } else {
            $(this.playBtn).removeClass("ui-icon-play");
            $(this.playBtn).addClass("ui-icon-pause");
        }
    };
    
    return PlayerControl;
    
});

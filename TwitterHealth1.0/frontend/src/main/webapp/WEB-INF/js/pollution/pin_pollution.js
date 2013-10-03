
function PinsLoadingDisplay() {
	// create and style div
	this.loadOverlay = document.createElement('div');
	$(this.loadOverlay).attr('id', 'loadOverlay');
	// style
	this.loadOverlay.style.width = '400px';
	this.loadOverlay.style.paddingRight = '10px';
	this.loadOverlay.style.fontSize = '15px';
	this.loadOverlay.style.textAlign = 'center';
	this.loadOverlay.style.color = '#FFFFFF';
	this.loadOverlay.style.paddingBottom = '20px';
	$(this.loadOverlay).text('Loading Markers for Tweets...');
	$(this.loadOverlay).effect('pulsate', {}, 500);
	
	// event handler
	$(this.loadOverlay).bind('stopLoadAnimation', function() {
		var overlay = this;
		$(overlay).effect('fade', {}, 3000, function() {
			$(overlay).detach();
		});
	});
	
	// not sure if this is necessary
	this.loadOverlay.index = 1;
	allControls['loadDisplay'] = this;
}
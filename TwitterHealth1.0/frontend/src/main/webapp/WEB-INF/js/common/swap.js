
function SwapPagesButton(map) {
	this.map = map;
	this.button = document.createElement('div');
	this.active = true;
	
	this.button.style.width = '98px';
	this.button.style.textAlign = 'center';
	this.button.style.marginLeft = '12px';
	this.button.style.marginRight = '12px';
	this.button.style.marginBottom = '12px';
	this.button.style.float = 'left';
	$(this.button).addClass('ui-selectee');
	
	var context = this;
	var http = window.location.protocol;
	var host = window.location.host;
	var pagetype = window.location.pathname.split('/')[1];
	
	if(pagetype == 'pollution' || pagetype == '') {
		$(this.button).text('Heatmap');
		$(this.button).bind('click', function(event) {
			if(context.active) {
				window.location = http + '//' + host + '/heatmap';
			}
		});
	}
	else if(pagetype == 'heatmap') {
		$(this.button).text('Home');
		$(this.button).bind('click', function(event) {
			if(context.active) {
				window.location = http + '//' + host + '/pollution';
			}
		});
	}
	
	allControls['swapButton'] = this;
}
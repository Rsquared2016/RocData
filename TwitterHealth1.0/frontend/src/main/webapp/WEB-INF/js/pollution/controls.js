
function MapControl() {
	this.map = null;
	this.container = null;
	this.active = false;
	
	this.getMap() { return this.map; };
	this.getContainer() { return this.container; };
	this.getActive() { return this.active; };
	this.setMap(map) { this.map = map; };
	this.setContainer(container) { this.container = container };
	this.setActive(active) { this.active = active; };
};

function AboutButton(map) {
	// initialize component divs
	this.map = map;
	this.button = document.createElement('div');
	this.window = new AboutWindow(map);
	this.active = true;
	// style
	this.button.style.width = '98px';
	this.button.style.height = '18px';
	this.button.style.marginLeft = '12px';
	this.button.style.marginRight = '12px';
	this.button.style.marginBottom = '10px';
	this.button.style.textAlign = 'center';
	$(this.button).text('About');
	$(this.button).addClass('ui-selectee');
	
	// event handlers
	var context = this;
	$(this.button).bind('click', function(event) {
		if(context.active) {
			if(!context.window.open) {
				$(context.window.window).show();
				$(context.window.window).effect('size', {
					to: {
						width: $("#map_canvas").width() * 4/5,
						height: $("#map_canvas").height() * 3/4
					},
					origin: ['top', 'left'],
					scale: 'box'
				}, 250, function() {
					// reposition close button
					context.window.wrapper.style.left = $(context.window.window).width() - 32 + 'px';
					context.window.wrapper.style.top = '0px';
					$(context.window.closeButton).addClass('ui-icon');
					$(context.window.closeButton).addClass('ui-icon-closethick');
					$(context.window.wrapper).addClass('ui-state-active');
				});
				context.window.window.style.padding = '8px';
				context.window.open = true;
			}
		}
	});
	
	this.button.index = 1;
}

function AboutWindow(map) {
	// initialize component divs
	this.map = map;
	this.window = document.createElement('div');
	this.wrapper = document.createElement('div');
	this.closeButton = document.createElement('div');
	this.open = false;
	// stylin'
	this.window.style.position = 'absolute';
	$(this.window).hide();
	this.window.style.width = '0px';
	this.window.style.height = '0px';
	this.window.style.overflow = 'auto';
	this.window.style.marginLeft = $("#map_canvas").width() * 1/10 + 'px';
	$(this.window).addClass('ui-selectee');
	$(this.window).append(this.wrapper);
	$(this.wrapper).append(this.closeButton);
	this.wrapper.style.width = '16px';
	this.wrapper.style.height = '16px';
	this.wrapper.style.position = 'relative';
	
	$(this.window).append("<div class='aboutText'><h2>Our Mission: Empower People with Meaningful Insights Learned from Data</h2>" +
	"<p>Given that three of your friends have flu-like symptoms, and that you have recently met eight people, possibly strangers, who complained about having runny noses and headaches, what is the probability that you will soon become ill as well?</p>" +
	"<p>This app enables you to see the spread of infectious diseases, such as flu, throughout a real-life population.</p>" +
	"<p>We apply machine learning and natural language understanding techniques to determine the health state of Twitter users.</p>" +
	"<p>Since a large fraction of tweets is geo-tagged, we can plot them on a map, and observe how sick and healthy people interact. Our model then predicts if and when an individual will fall ill with high accuracy, thereby improving our understanding of the emergence of global epidemics from people's day-to-day interactions.</p>" +
	"<p>The fine-grained epidemiological models we show here are just one instance of the general class of problems that our system solves. Other domains include understanding of the public sentiment around your company or products, the diffusion of information throughout a population, and predicting customer behavior.</p>" +
	"<p>By augmenting existing datasets with real-time insights and cues from social media, we are able to connect the dots, visualize patterns, and refine models based on user feedback.</p>" +
	"<p>To learn more about our models, visit <a href='http://www.cs.rochester.edu/~sadilek/research/'>our research website</a>.</p></div>");
	
	// event handlers
	var context = this;
	$(this.closeButton).bind('click', function(event) {
		if(context.open) {
			$(context.window).effect('size', {
				to: {
					width: 0,
					height: 0
				},
				origin: ['right', 'bottom'],
				scale: 'box'
			}, 250, function() {
				$(context.window).hide();
				context.open = false;
				$(context.closeButton).removeClass('ui-icon');
				$(context.closeButton).removeClass('ui-icon-closethick');
				$(context.wrapper).removeClass('ui-state-active');
			});
		}
	});
}
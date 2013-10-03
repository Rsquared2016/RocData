// Controls
// ----------------
// all sorts of controls used in our mobile app

define(["text!/resources/templates/mobile/control-button.html",
        "text!/resources/templates/mobile/control-slider.html"],
    function(buttonTmpl, sliderTmpl) {
        // Control
        var control = function(attr) {
            this.element = document.createElement("div");
            this.classes = attr.classes || [];
            this.prepend = attr.prepend || false;
            this.parent = attr.parent || null;
            this.map = attr.map || null;
            this.position = attr.position || null;
        };
        
        control.prototype = {
            add: function() {
                var parent = this.getParent(), map = this.getMap(), prepend = this
                    .getPrepend(), position = this.getPosition(), element = this
                    .getElement();
                if (!parent && !map)
                    return;
                
                if (map) {
                    map.gmap.controls[position].push(element);
                } else {
                    if (prepend)
                        $(element).prependTo(parent);
                    else
                        $(element).appendTo(parent);
                }
                
                // for method chaining
                return this;
            },
            
            remove: function() {
                var map = this.getMap(), position = this.getPosition(), element = this
                    .getElement();
                if (map) {
                    map.gmap.controls[position].forEach(function(control, i) {
                        if (control == element)
                            index = i;
                    });
                    map.gmap.controls[position].removeAt(index);
                } else {
                    $(element).remove();
                }
            },
            
            // add actual content to the element
            draw: function(html) {
                var element = this.getElement(), classes = this.getClasses();
                $(element).append(html);
                $.each(classes, function(index, klass) {
                    $(element).addClass(klass);
                });
            },
            
            getElement: function() {
                return this.element;
            },
            
            getClasses: function() {
                return this.classes;
            },
            
            getPrepend: function() {
                return this.prepend;
            },
            
            getParent: function() {
                return this.parent;
            },
            
            getPosition: function() {
                return this.position;
            },
            
            getMap: function() {
                return this.map;
            }
        };
        
        // Button
        var button = function(attr) {
            control.call(this, attr);
            this.text = attr.text;
            this.draw(_.template(buttonTmpl, {
                text: attr.text || ''
            }));
            
            // event handlers
            var element = this.getElement();
            this.click = attr.click;
            $(element).click(this.click);
            $(element).hover(this.hoverIn, this.hoverOut);
        };
        
        _.extend(button.prototype, control.prototype);
        _.extend(button.prototype, {
            hoverIn: function(event) {
                if(!$(event.target).hasClass('inactive'))
                    $(event.target).css('cursor', 'pointer');
            },
            
            hoverOut: function(event) {
                if(!$(event.target).hasClass('inactive'))
                    $(event.target).css('cursor', 'default');
            },
            
            isActive: function() {
                return !$(this.element).hasClass('inactive');
            }
        });
        
        // Slider
        var slider = function(attr) {
            control.call(this, attr);
            this.title = attr.title || '';
            this.poles = attr.poles || ['0', '10'];
            this.options = {
                handle: '#slider-handle',
                min: attr.min || 0,
                max: attr.max || 10,
                value: attr.max/2 || 5,
                step: attr.step || 1,
                range: attr.range || false,
                orientation: attr.orientation || "horizontal"
            };
            this.draw(_.template(sliderTmpl, {
                title: this.title,
                poles: this.poles,
                defaultValue: this.options.value
            }));
            
            // event handlers
            var element = this.getElement();
            this.change = attr.change;
            this.slide = attr.slide || this.slide;
            $(".ui-slider-element", element).bind("slidechange", this.change);
            $(".ui-slider-element", element).bind("slide", this.slide);
        };
        
        _.extend(slider.prototype, control.prototype);
        _.extend(slider.prototype, {
            draw: function(html) {
                control.prototype.draw.call(this, html);
                // create slider
                var element = this.getElement();
                $(".ui-slider-element", element).slider(this.options);
            },
            
            // default slide event handler
            // (user free to override this)
            slide: function(event, ui) {
                var element = $(event.target).parent().get(0);
                $(".ui-slider-value", element).text(ui.value);
            }
        });
        
        return {
            Button: button,
            Slider: slider
        };
    });

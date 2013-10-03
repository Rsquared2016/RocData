/* 
 * heatmap.js 1.0 -    JavaScript Heatmap Library
 *
 * Copyright (c) 2011, Patrick Wied (http://www.patrick-wied.at)
 * Dual-licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and the Beerware (http://en.wikipedia.org/wiki/Beerware) license.
 */

(function(w) {
    // the heatmapFactory creates heatmap instances
    var heatmapFactory = (function() {
        
        /*
         * store object constructor a heatmap contains a store the store has to
         * know about the heatmap in order to trigger heatmap updates when
         * datapoints get added
         */
        function store(hmap) {
            this.data = [];
            this.heatmap = hmap;
        }
        
        store.prototype = {
            setDataSet: function(dataSet) {
                
                var heatmap = this.heatmap;
                var data = [];
                var dataSetData = dataSet.data;
                var dlen = dataSetData.length;
                var lookup = [];
                
                this.min = heatmap.minCount(dataSetData);
                this.max = heatmap.maxCount(dataSetData);
                var shift = (this.min == this.max ? 0 : this.min);
                
                for ( var i = 0; i < dlen; i += 1) {
                    var point = dataSetData[i];
                    if (!data[point.x])
                        data[point.x] = [];
                    
                    if (!data[point.x][point.y])
                        data[point.x][point.y] = 0;
                    
                    data[point.x][point.y] = point.count - shift;
                    var count = data[point.x][point.y];
                    
                    if (this.max < count)
                        this.max = count;
                    
                    lookup.push(point);
                }
                
                this.pointLookup = lookup;
                this.data = data;
                
                if (heatmap.animated) {
                    var h = heatmap;
                    log.info(h.numFrames + " images of size [width: " + h.width
                        + ", height: " + h.height
                        + "] will be generated for animation, taking "
                        + ((h.numFrames * h.width * h.height * 4) / 1000000)
                        + " MB of RAM");
                    
                    heatmap.storeLocalizedMidnightTime();
                    var frameData = heatmap.prepareFrameData(dataSet);
                    heatmap.prepareImageSequence(frameData);
                }
            }
        };
        
        // heatmap object constructor
        function heatmap(config) {
            this.element = {};
            this.canvas = {};
            this.acanvas = {};
            this.ctx = {};
            this.actx = {};
            this.visible = true;
            this.width = 0;
            this.height = 0;
            this.gradient = false;
            this.opacity = 180;
            this.debug = true;
            /*
             * heatmap store containing the datapoints and information about the
             * maximum accessible via instance.store
             */
            this.store = new store(this);
            this.currentFrameIdx = -1;
            this.timeLabels = this.getTimeLabels();
            this.timelineFillStyle = "rgba(255,255,0,0.2)";
            this.timeWindowFillStyle = "rgba(0,0,255,0.8)";
            this.timelineTextFillStyle = "rgba(100,255,100,0.8)";
            this.timeWindowFont = "11pt Courier";
            this.timeWindowOn = false;
            this.premultiplyAlpha = false;
            // configure the heatmap when an instance gets created
            this.configure(config);
            // and initialize it
            this.init();
        }
        
        // public functions
        heatmap.prototype = {
            configure: function(config) {
                this.radius = config.radius || 40;
                this.element = (config.element instanceof Object) ? config.element
                    : document.getElementById(config.element);
                this.visible = config.visible;
                // default is the common blue to red gradient
                this.gradient = config.gradient || {
                    "0.45": "rgb(0,0,255)",
                    "0.55": "rgb(0,255,255)",
                    "0.65": "rgb(0,255,0)",
                    "0.95": "yellow",
                    "1.0": "rgb(255,0,0)"
                };
                this.opacity = parseInt(255 / (100 / config.opacity), 10) || 180;
                this.width = config.width || 0;
                this.height = config.height || 0;
                this.debug = config.debug;
                this.timeWindow = config.timeWindow || 60000 * 90;
                this.animationPeriod = config.animationPeriod || 50;
                this.showTimeCallback = config.showTimeCallback;
                this.state = config.initialState ? config.initialState : "none";
                this.framesPerHour = config.framesPerHour || 5;
                this.minimumOpacity = config.minimumOpacity || 0.5;
                this.maximumOpacity = config.maximumOpacity || 1.0;
                this.animated = config.animated || false;
                this.timezoneOffsetMillis = config.timezoneOffsetMillis || 0;
            },
            resize: function(acanvas, canvas) {
                var element = this.element;
                
                this.width = element.style.width.replace(/px/, "")
                    || this.getWidth(element);
                
                this.height = acanvas.height = element.style.height.replace(/px/, "")
                    || this.getHeight(element);
                
                canvas.width = acanvas.width = this.width;
                canvas.height = acanvas.height = this.height;
                
                if (this.animated) {
                    var w = this.width;
                    var h = this.height;
                    this.timeLineWidth = 0.8 * w;
                    this.horizPos = (w - this.timeLineWidth) / 2.0;
                    this.vertPos = h * 0.9;
                    this.hourWidth = this.timeLineWidth / 24.0;
                    this.timeWindowWidth = this.timeWindow / 3600000.0 * this.hourWidth;
                    this.timeStepWidth = this.timeStep / 3600000.0 * this.hourWidth;
                }
            },
            init: function() {
                var canvas = document.createElement("canvas");
                var acanvas = document.createElement("canvas");
                
                this.canvas = canvas;
                this.acanvas = acanvas;
                
                // frames for the animation
                var numFrames = 24 * this.framesPerHour;
                this.numFrames = numFrames;
                this.timeStep = (60 * 60 * 1000) / this.framesPerHour;
                
                this.resize(acanvas, canvas);
                
                this.frames = new Array(numFrames);
                
                this.initColorPalette();
                
                canvas.style.cssText = acanvas.style.cssText = "position:absolute;top:0;left:0;z-index:10000000;";
                
                if (!this.visible)
                    canvas.style.display = "none";
                
                this.element.appendChild(canvas);
                // debugging purposes only
                if (this.debug)
                    document.body.appendChild(acanvas);
                this.ctx = canvas.getContext("2d");
                this.actx = acanvas.getContext("2d");
            },
            initColorPalette: function() {
                var canvas = document.createElement("canvas");
                canvas.width = "1";
                canvas.height = "256";
                var ctx = canvas.getContext("2d");
                var grad = ctx.createLinearGradient(0, 0, 1, 256);
                
                /*
                 * Test how the browser renders alpha by setting a partially
                 * transparent pixel and reading the result. A good browser will
                 * return a value reasonably close to what was set. Some
                 * browsers (e.g. on Android) will return a ridiculously wrong
                 * value.
                 */
                testData = ctx.getImageData(0, 0, 1, 1);
                testData.data[0] = testData.data[3] = 64; // 25% red & alpha
                testData.data[1] = testData.data[2] = 0; // 0% blue & green
                ctx.putImageData(testData, 0, 0);
                testData = ctx.getImageData(0, 0, 1, 1);
                this.premultiplyAlpha = (testData.data[0] < 60 || testData.data[0] > 70);
                
                var gradient = this.gradient;
                for ( var x in gradient) {
                    grad.addColorStop(x, gradient[x]);
                }
                
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, 1, 256);
                
                this.gradient = ctx.getImageData(0, 0, 1, 256).data;
            },
            getWidth: function(element) {
                var width = element.offsetWidth;
                if (element.style.paddingLeft)
                    width += element.style.paddingLeft;
                if (element.style.paddingRight)
                    width += element.style.paddingRight;
                
                return width;
            },
            getHeight: function(element) {
                var height = element.offsetHeight;
                if (element.style.paddingTop)
                    height += element.style.paddingTop;
                if (element.style.paddingBottom)
                    height += element.style.paddingBottom;
                
                return height;
            },
            /**
             * Colorizes a given <code>ImageData</code> object in a following
             * way; for each pixel's alpha value, lookup a color in a
             * precomputed alpha-to-color table (a palette) and set it as this
             * pixel's color.
             * 
             * @param image
             */
            colorize: function(image) {
                // some performance tweaks
                var imageData = image.data;
                var length = imageData.length;
                var palette = this.gradient;
                var opacity = this.opacity;
                var premultiplyAlpha = this.premultiplyAlpha;
                // loop thru the area
                for ( var i = 3; i < length; i += 4) {
                    
                    // [0] -> r, [1] -> g, [2] -> b, [3] -> alpha
                    var alpha = imageData[i];
                    var offset = alpha * 4;
                    
                    if (!offset)
                        continue;
                    
                    // we ve started with i=3 set the new r, g and b values
                    var finalAlpha = (alpha < opacity) ? alpha : opacity;
                    imageData[i - 3] = palette[offset];
                    imageData[i - 2] = palette[offset + 1];
                    imageData[i - 1] = palette[offset + 2];
                    
                    if (premultiplyAlpha) {
                        /*
                         * To fix browsers that premultiply incorrectly, we'll
                         * pass in a value scaled appropriately so when the
                         * multiplication happens the correct value will result.
                         */
                        imageData[i - 3] /= 255 / finalAlpha;
                        imageData[i - 2] /= 255 / finalAlpha;
                        imageData[i - 1] /= 255 / finalAlpha;
                    }
                    
                    /*
                     * we want the heatmap to have a gradient from transparent
                     * to the colors as long as alpha is lower than the defined
                     * opacity (maximum), we'll use the alpha value
                     */
                    imageData[i] = finalAlpha;
                }
            },
            drawAlpha: function(x, y, count, actx) {
                var minOpacity = this.minimumOpacity;
                var maxOpacity = this.maximumOpacity;
                
                // the center of the radial gradient has .1 alpha value
                var alpha = Math.max(minOpacity, count / this.store.max);
                alpha = Math.min(maxOpacity, alpha);
                actx.shadowColor = "rgba(0,0,0," + alpha + ")";
                actx.shadowOffsetX = 1000;
                actx.shadowOffsetY = 1000;
                actx.shadowBlur = 15;
                actx.beginPath();
                actx.arc(x - 1000, y - 1000, this.radius, 0, Math.PI * 2, true);
                actx.closePath();
                actx.fill();
            },
            toggleDisplay: function() {
                var visible = this.visible;
                var canvas = this.canvas;
                
                if (!visible)
                    canvas.style.display = "block";
                else
                    canvas.style.display = "none";
                
                this.visible = !visible;
            },
            // dataURL export
            getImageData: function() {
                return this.canvas.toDataURL();
            },
            clear: function() {
                var w = this.width;
                var h = this.height;
                this.ctx.clearRect(0, 0, w, h);
                this.actx.clearRect(0, 0, w, h);
            },
            cleanup: function() {
                this.element.removeChild(this.canvas);
            },
            drawDataSet: function() {
                var data = this.store.data;
                
                for ( var x in data)
                    for ( var y in data[x])
                        this.drawAlpha(x, y, data[x][y], this.actx);
                
                var image = this.actx.getImageData(0, 0, this.width, this.height);
                this.colorize(image);
                this.ctx.putImageData(image, 0, 0);
            },
            drawFrame: function(index) {
                if (!this.frames || this.frames.length == 0 || !this.frames[index])
                    return;
                this.clear();
                this.ctx.putImageData(this.frames[index], 0, 0);
            },
            drawCurrentFrame: function() {
                this.drawFrame(this.currentFrameIdx);
                
                if (this.animated) {
                    if (this.timeWindowOn)
                        this.drawTimeWidnow(this.currentFrameIdx);
                    
                    this.showTimeCallback(this.getTimeWindowEndTime());
                }
            },
            drawTimeWidnow: function(index) {
                var ctx = this.ctx;
                var horizPos = this.horizPos;
                var vertPos = this.vertPos;
                var timeLineWidth = this.timeLineWidth;
                
                // horizontal line
                ctx.fillStyle = this.timelineFillStyle;
                ctx.fillRect(horizPos, vertPos - 3, timeLineWidth, 6);
                
                // time window
                ctx.fillStyle = this.timeWindowFillStyle;
                ctx.fillRect(this.currentWindowPos, vertPos - 3, this.timeWindowWidth, 6);
                
                // hour markers
                ctx.moveTo(horizPos, vertPos);
                this.curPos = horizPos;
                var hour = 0;
                while (hour < 25) {
                    ctx.fillStyle = this.timelineFillStyle;
                    ctx.moveTo(this.curPos, vertPos - 5);
                    ctx.lineTo(this.curPos, vertPos + 5);
                    ctx.stroke();
                    ctx.fillStyle = this.timelineTextFillStyle;
                    ctx.font = this.timeWindowFont;
                    ctx.fillText(this.timeLabels[hour++], this.curPos - 10, vertPos - 10);
                    this.curPos += this.hourWidth;
                }
            },
            play: function() {
                if (!this.timer) {
                    var animationPeriod = this.animationPeriod;
                    var self = this;
                    this.timer = setInterval(function() {
                        self.drawCurrentFrame();
                        self.seekNextFrame();
                    }, animationPeriod);
                }
                ;
                this.state = "play";
            },
            pause: function() {
                if (this.timer) {
                    clearInterval(this.timer);
                    this.timer = null;
                }
                this.state = "pause";
            },
            interrupt: function() {
                if (this.state == "play" || this.state == "pause")
                    this.pause();
                else
                    this.state = "interrupted";
            },
            resume: function() {
                if (this.state == "pause" || this.state == "play") {
                    this.play();
                } else if (this.state == "interrupted") {
                    this.drawFrame(this.currentFrameIdx);
                    if (this.timeWindowOn)
                        this.drawTimeWidnow(this.currentFrameIdx);
                } else
                    this.drawDataSet();
            },
            toggleTimeWindow: function() {
                this.timeWindowOn = !this.timeWindowOn;
            },
            /**
             * Prepares a sequence of <code>ImageData</code> object, each
             * representing an animation frame.
             * 
             * @param frameData
             */
            prepareImageSequence: function(frameData) {
                var clen = this.numFrames;
                var actx = this.actx;
                while (clen--) {
                    var fData = frameData[clen];
                    if (!fData)
                        continue;
                    var image = this.createImageData(actx);
                    actx.putImageData(image, 0, 0);
                    var flen = fData.length;
                    while (flen--) {
                        var point = fData[flen];
                        var data = this.store.data;
                        this.drawAlpha(point.x, point.y, data[point.x][point.y], actx);
                    }
                    var image = actx.getImageData(0, 0, this.width, this.height);
                    this.colorize(image);
                    this.frames[clen] = image;
                }
            },
            /**
             * Creates a sequence of data points in a time interval between the
             * <code>start</code> and the <code>end</code>.
             * 
             * @param data
             * @param start
             * @param end
             * @returns {Array}
             */
            prepareFrameDataItem: function(data, start, end) {
                var i1 = 0;
                var i2 = 0;
                
                var index = this.indexOfInSortedArray(data, start);
                i1 = i2 = (index == data.length - 1 ? index : index + 1);
                /*
                 * keep adding data points until we reach the end of the
                 * interval
                 */
                while (i2 < data.length && data[i2].time <= end)
                    i2++;
                
                var lookup = this.store.pointLookup;
                var item = [];
                
                while (i1 < i2) {
                    item.push(lookup[i1++]);
                }
                
                return item;
            },
            /**
             * Creates and returns a list of sequences of data points, each
             * sequence representing a data set for an animation frame.
             * 
             * @param dataSet
             * @returns {Array}
             */
            prepareFrameData: function(dataSet) {
                this.frames = [];
                var frameData = new Array(this.numFrames);
                
                if (dataSet.data.length == 0) {
                    log.info("heatmap has no data, there won't be any animation");
                    return frameData;
                }
                
                var timeWindow = this.timeWindow;
                var timeStep = this.timeStep;
                var timeEnd = dataSet.data[dataSet.data.length - 1].time;
                var d = dataSet.data;
                var start = d[0].time;
                var end = start + timeWindow;
                
                var i = 0;
                do {
                    frameData[i++] = this.prepareFrameDataItem(d, start, end);
                    start += timeStep;
                    end += timeStep;
                } while (end < timeEnd);
                
                this.frameData = frameData;
                
                return frameData;
            },
            setWindowPosition: function(frameIndex) {
                var offset = (frameIndex * this.timeStep) / 3600000.0;
                this.currentWindowPos = this.horizPos + offset * this.hourWidth;
            },
            maxCount: function(data) {
                var max = -1000;
                var i = data.length;
                while (i--) {
                    var point = data[i];
                    if (point.count > max)
                        max = point.count;
                }
                return max;
            },
            minCount: function(data) {
                var min = 1000;
                var i = data.length;
                while (i--) {
                    var point = data[i];
                    if (point.count < min)
                        min = point.count;
                }
                return min;
            },
            getNextFrameIndex: function(frameIndex) {
                return frameIndex == (this.numFrames - 1) ? 0 : frameIndex + 1;
            },
            getPreviousFrameIndex: function(frameIndex) {
                return frameIndex == 0 ? this.numFrames - 1 : frameIndex - 1;
            },
            seekNextFrame: function() {
                var index = this.getNextFrameIndex(this.currentFrameIdx);
                while (!this.frameData[index])
                    index = this.getNextFrameIndex(index);
                
                this.currentFrameIdx = index;
                this.setWindowPosition(index);
            },
            seekPreviousFrame: function() {
                var index = this.getPreviousFrameIndex(this.currentFrameIdx);
                while (!this.frameData[index])
                    index = this.getPreviousFrameIndex(index);
                
                this.currentFrameIdx = index;
                this.setWindowPosition(index);
            },
            drawNextFrame: function() {
                this.seekNextFrame();
                this.drawCurrentFrame();
            },
            drawPreviousFrame: function() {
                this.seekPreviousFrame();
                this.drawCurrentFrame();
            },
            getTimeLabels: function() {
                var labels = [];
                
                for ( var i = 0; i <= 24; i++) {
                    var label;
                    if (i == 24)
                        label = "00:00";
                    if (i > 9)
                        label = i + ":00";
                    label = "0" + i + ":00";
                    
                    labels[i] = label;
                }
                
                return labels;
            },
            indexOfInSortedArray: function(array, value) {
                var i1 = 0;
                var i2 = array.length - 1;
                var half = Math.floor((i2 + i1) / 2);
                while (i1 < i2) {
                    if (array[half].time < value)
                        i1 = half + 1;
                    else
                        i2 = half - 1;
                    half = Math.floor((i2 + i1) / 2);
                }
                return i1;
            },
            /**
             * Tries to create a new <code>ImageData</code> object from HTML5
             * canvas context object. This doesn't work in Opera since it
             * doesn't support <code>createImageData</code> function.
             * 
             * @param context
             * @returns
             */
            createImageData: function(context) {
                var w = this.width;
                var h = this.height;
                if (context.createImageData) {
                    try {
                        return context.createImageData(w, h);
                    } catch (error) {
                        // bad luck, e.g. Opera doesn't support this
                    }
                }
                
                if (context.getImageData) {
                    return context.getImageData(0, 0, w, h);
                } else {
                    return {
                        width: w,
                        height: h,
                        data: new Array(w * h * 4)
                    };
                }
            },
            
            storeLocalizedMidnightTime: function() {
                var time0 = new Date(this.store.pointLookup[0].time);
                this.clearTime(time0);
                var utcMidnightTime = time0.getTime();
                var aDay = 1000 * 60 * 60 * 24;
                this.localizedMidnightTime = utcMidnightTime - this.timezoneOffsetMillis
                    + aDay;
            },
            
            getTimeWindowEndTime: function() {
                return this.localizedMidnightTime + this.timeStep * this.currentFrameIdx
                    + this.timeWindow;
            },
            
            clearTime: function(date) {
                var year = date.getUTCFullYear();
                var month = date.getUTCMonth();
                var day = date.getUTCDate();
                var newDate = Date.UTC(year, month, day);
                return date.setTime(newDate);
            }
        };
        
        return {
            create: function(config) {
                return new heatmap(config);
            }
        };
    })();
    w.heatmapFactory = heatmapFactory;
})(window);

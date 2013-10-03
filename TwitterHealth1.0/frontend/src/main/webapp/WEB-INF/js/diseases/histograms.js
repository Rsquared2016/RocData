
var diseases=new Array();
diseases["Anthrax"]="#0000FE";
diseases["Cholera"]="#FC0008";
diseases["Common Cold"]="#1EFF09";
diseases["Dengue"]="#FC00A9";
diseases["Diphtheria"]="#FECC0B";
diseases["Gastroenteritis"]="#084702";
diseases["Influenza"]="#7068FE";
diseases["Legionnaires' Disease"]="#8B3C35";
diseases["Malaria"]="#1EFFB4";
diseases["Measles"]="#0D7083";
diseases["Meningitis"]="#000067";
diseases["Mosquito Borne Disease"]="#85CE3F";
diseases["Mumps"]="#F287D2";
diseases["Pertussis"]="#C600FE";
diseases["Pneumonia"]="#670656";
diseases["Polio"]="#F1004E";
diseases["STD"]="#FEB470";
diseases["Rabies"]="#7A9868";
diseases["Tuberculosis"]="#F16E0C";
diseases["Tetanus"]="#706005";
diseases["Typhoid"]="#0FA6C5";
diseases["Smallpox"]="#8DB1FF";
diseases["Tick Borne Disease"]="#5E4C68";
diseases["Varicella"]="#0949FE";

function getColorByDisease(disease){
	try{return diseases[disease];}catch(err){return "#999900";}
}

function fullyReduce(stats) {
    var sums = {};
    var values = [];
    // calculate sums
    $.each(stats, function(i, stat) {
        if(!sums[stat.key.join(';')]) sums[stat.key.join(';')] = 0;
        sums[stat.key.join(';')] += stat.value;
    });
    // readd as list
    $.each(sums, function(key, count) {
        values.push({ key: key.split(';'), value: count });
    });
    
    return values;
}

function processCounts(data) {
    // clear out ul
    $("ul#histogram").empty();
    // adds panels for each disease at the bottom of the page
    $.each(data, function(i, info) {
        // add appropriate panels
        var day = info.key[0];
        var disease = info.key[1] ? info.key[1] : "";
        var key = info.key[2] ? info.key[2] : (info.key[1] ? info.key[1] : "");
        var count = info.value;
        var url = isDiseasePage() ? getDiseasePageName() + "/" + key : getUrl(false, null, key);
        var template = '<li>\n' +
    	    '<div class="histogram">\n' +
    		    '<a class="' + key.replace(/\'/g, "").replace(/\W/g, "-") +
    		        '" href="' + url + '">\n' +
    				key + ' [' + count + ']\n' +
    		    '</a>\n' +
    		    '<a href="' + url + '">\n' +
    		        '<span id="' + key.replace(/[^A-Za-z]/g, "") + '"></span>\n' +
    		    '</a>\n' +
    		'</div>\n' +
    		'<div id="' + key.replace(/[^A-Za-z]/g, "") + '" class="snippets">\n' +
    		    '<div id="0"></div><div id="1"></div><div id="2"></div><div id="3"></div>\n' +
    		'</div>\n' +
    	'</li>\n';
    	$("ul#histogram").append(template);
    });
    // try to add snippets
    countsLoaded = true;
    $(document).trigger('addSnippets');
}

function processHistograms(dataJSON) {
    
	var data = [];
	var byDisease = new Object();
	byDisease['Anthrax'] = [];
	byDisease['Cholera'] = [];
	byDisease['CommonCold'] = [];
	byDisease['Dengue'] = [];
	byDisease['Diphtheria'] = [];
	byDisease['Gastroenteritis'] = [];
	byDisease['Influenza'] = [];
	byDisease['LegionnairesDisease'] = [];
	byDisease['Malaria'] = [];
	byDisease['Measles'] = [];
	byDisease['Meningitis'] = [];
	byDisease['MosquitoBorneDisease'] = [];
	byDisease['Mumps'] = [];
	byDisease['Pertussis'] = [];
	byDisease['Pneumonia'] = [];
	byDisease['Polio'] = [];
	byDisease['Rabies'] = [];
	byDisease['Smallpox'] = [];
	byDisease['STD'] = [];
	byDisease['Tetanus'] = [];
	byDisease['TickBorneDisease'] = [];
	byDisease['Tuberculosis'] = [];
	byDisease['Typhoid'] = [];
	byDisease['Varicella'] = [];
	var byTerm = {}; 
	var epochMap = {};
	var termTaxonomy = {};
	
	var root = new Date(2012, 4, 1,0,0,0,0).getTime();
	var diseaseEnum = {
	    Anthrax: 0,
	    Cholera: 1,
	    CommonCold: 2,
	    Dengue: 3,
	    Diphtheria: 4,
	    Gastroenteritis: 5,
	    Influenza: 6,
	    LegionnairesDisease: 7,
	    Malaria: 8,
	    Measles: 9,
	    Meningitis: 10,
	    MosquitoBorneDisease: 11,
	    Mumps: 12,
	    Pertussis: 13,
	    Pneumonia: 14,
	    Polio: 15,
	    Rabies: 16,
	    Smallpox: 17,
	    STD: 18,
	    Tetanus: 19,
	    TickBorneDisease: 20,
	    Tuberculosis: 21,
	    Typhoid: 22,
	    Varicella: 23
	};
    var months = { Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5,
                     Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11 };
	// Convert strings to numbers.
	$.each(dataJSON, function(){
				var date = this.key.toString().split(',')[1];
				var epochDate = new Date(date.split(' ')[3], months[date.split(' ')[2]], date.split(' ')[1],date.split(' ')[4],0,0,0);
				// we need to offset by 4 hours to sync it back with universal time
				// (no idea why it isn't in universal in the first place...)
				var fourHrsMs = 4 * 60 * 60 * 1000;
				var epoch = (epochDate.getTime() - fourHrsMs - root) / 100000;
				var dis = this.key.toString().split(',')[2];
				var term = isDiseasePage() ? this.key.toString().split(',')[3] : "";
				// add disease-based offset
				var index = dis.replace(/[^A-Za-z]/g, '');
				var offset = isDiseasePage() ? 0 : diseaseEnum[index];
				epoch += offset;
				var realDate = new Date(date.split(' ')[3], months[date.split(' ')[2]], date.split(' ')[1],
				    date.split(' ')[4], 0, 0, 0);
                  
                  //log.info(this.key.toString());
                  //log.info(this.key.toString().split(',')[0]);
				  data.push({
					disease:dis,
					date:epoch,
					realDate: realDate,
					term: term,
					value:this.value
				});
				  
				  try{
					  byDisease[index].push({
							disease:this.key.toString().split(',')[2],
							date:epoch,
        					realDate: realDate,
        					term: term,
							value:this.value
						});
					if(!byTerm[term])
					    byTerm[term] = [];
					byTerm[term].push({
					    disease:this.key.toString().split(',')[2],
						date:epoch,
    					realDate: realDate,
    					term: term,
						value:this.value
					});
				  }catch(err){}
				  
				  epochMap[epoch] = realDate;
				  if(!termTaxonomy[dis.replace(/[^A-Za-z]/g, '')])
				    termTaxonomy[dis.replace(/[^A-Za-z]/g, '')] = [];
				  if($.inArray(term, termTaxonomy[dis.replace(/[^A-Za-z]/g, '')]) == -1)
				    termTaxonomy[dis.replace(/[^A-Za-z]/g, '')].push(term);
				  
				//alert(this.key.toString().split(',')[3]+"|"+this.value);
	});
	
	var barWidth = 2;
	var width = $('#chart').width();
	var height = 100;
	var x = d3.scale.linear().domain([d3.min(data, function(datum) { return datum.date; }), d3.max(data, function(datum) { return datum.date; })]).range([0, width]);
	var y = d3.scale.linear().domain([0, d3.max(data, function(datum) { return datum.value; })]).
	  rangeRound([0, height]);
	
	// add the canvas to the DOM
	// for now, no large histogram, but maybe we'll revisit this later
	/*$("#chart").empty();
	var barDemo = d3.select("#chart").
	  append("svg:svg").
	  attr("width", width).
	  attr("height", height);
	
	barDemo.selectAll("rect").
	  data(data).
	  enter().
	  append("svg:rect").
	  attr("x", function(datum, index) { return x(datum.date); }).
	  attr("y", function(datum) { return height - y(datum.value); }).
	  attr("height", function(datum) { return y(datum.value); }).
	  attr("width", barWidth).
	  attr("fill", function(datum){ return getColorByDisease(datum.disease)});*/
	var histoJson = isDiseasePage() ? byTerm : byDisease;
	var thisDisease = isDiseasePage() ? getDiseasePageName().replace(/[^A-Za-z]/g, '') : "";
	
	$.each(histoJson, function(index, data){
	    // skip nonpertinent terms
	    if(isDiseasePage() && $.inArray(index, termTaxonomy[thisDisease]) == -1)
	        return true;
        var w = ($("#chart").width() * 0.3).toFixed() - 40;
        var h = height/2;
        // get proper start and end of day
        //var xmin = d3.min(data, function(datum) { return datum.date; });
        //var xmax = d3.max(data, function(datum) { return datum.date; });
        var today = new Date(getDayPageName());
        var offset = !!diseaseEnum[index] ? diseaseEnum[index] : 0;
        var xmin = (today.getTime() - root) / 100000 + offset;
        var xmax = (today.getTime() - root) / 100000 + offset + 864;
        var x = d3.scale.linear().domain([xmin, xmax]).range([0, w]);
        var ymin = 0;
        var ymax = d3.max(data, function(datum) { return datum.value; });
        var y = d3.scale.linear().domain([0, ymax]).rangeRound([0, h]);
        var xpadding = 20;
        var ypaddingTop = 10;
        var ypaddingBottom = 75;
        
        // add the canvas to the DOM
        $("#" + index).empty()
        var barDemo = d3.select("#"+index).
          append("svg:svg").
          attr("width", w + xpadding * 2).
          attr("height", h + ypaddingBottom + ypaddingTop);
        
        // add axes and labels
        var xAxis = [], dis = isDiseasePage() ? thisDisease : index;
        for(var i = xmin; i < xmax; i += 36) {
            /*// start
            if(i == xmin)
                xAxis.push([i, epochMap[i]]);
            // every day
            else if((i - diseaseEnum[dis]) % 864 == 0) {
                if(!!epochMap[i])
                    xAxis.push([i, epochMap[i]]);
                else {
                    var msDiff = (i - xmin) * 100000;
                    epochMap[i] = new Date(epochMap[xmin].getTime() + msDiff);
                    xAxis.push([i, epochMap[i]]);
                }
            }*/
            var offset = isDiseasePage() ? 0 : diseaseEnum[index];
            xAxis.push([i, new Date((i - offset) * 100000 + root)]);
            //log.info(xAxis[xAxis.length-1][0], xAxis[xAxis.length-1][1].toUTCString());
        }
        
        var yAxis = [];
        for(var i = 0; i < ymax; i += 250)
            yAxis.push(i);
        yAxis[yAxis.length-1] = ymax;
        
        var axes = barDemo.append("svg:g");
        
        // add tick marks
        axes.selectAll(".xTicks").
            data(xAxis).
            enter().
            append("svg:line").
            attr("x1", function(datum) { return x(datum[0]) + xpadding; }).
            attr("x2", function(datum) { return x(datum[0]) + xpadding; }).
            attr("y1", h + ypaddingTop).
            attr("y2", h + ypaddingTop + 4).
            attr("stroke", "white");
            
        axes.selectAll(".yTicks").
            data(yAxis).
            enter().
            append("svg:line").
            attr("x1", xpadding - 4).
            attr("x2", xpadding).
            attr("y1", function(datum) { return h - y(datum) + ypaddingTop; }).
            attr("y2", function(datum) { return h - y(datum) + ypaddingTop; }).
            attr("stroke", "white");
        
        axes.selectAll(".yTicks").
            data(yAxis).
            enter().
            append("svg:line").
            attr("x1", xpadding).
            attr("x2", xpadding + w).
            attr("y1", function(datum) { return h - y(datum) + ypaddingTop; }).
            attr("y2", function(datum) { return h - y(datum) + ypaddingTop; }).
            attr("stroke", "#999999");
        
        // add labels
        axes.selectAll("text.xAxisBottom").
            data(xAxis).
            enter().
            append("svg:text").
            text(function(datum) {
                // format date string
                var day = datum[1];
                if(day.getUTCHours() % 6 == 0) {
                    var mo = day.getUTCMonth() < 9 ? "0" + (day.getUTCMonth() + 1) : "" + (day.getUTCMonth() + 1);
                    var date = day.getUTCDate() < 10 ? "0" + day.getUTCDate() : "" + day.getUTCDate();
                    var dayStr = mo + "/" + date + " " + day.getUTCHours() + ":00:00";
                    return dayStr;
                }
                else {
                    return "";
                }
            }).
            attr("x", function(datum) { return x(datum[0]) + xpadding; }).
            attr("y", h + ypaddingTop + 10).
            attr("text-anchor", "start").
            attr("style", "fill:white; font-size:9px").
            each(function(d, i) {
                var x = d3.select(this).attr("x");
                var y = d3.select(this).attr("y");
                d3.select(this).attr("transform", "rotate(45 " + x + "," + y + ")");
            });

        axes.selectAll("text.yAxisLeft").
            data(yAxis).
            enter().
            append("svg:text").
            text(function(datum) { return datum; }).
            attr("x", xpadding - 10).
            attr("y", function(datum) { return h - y(datum) + ypaddingTop; }).
            attr("text-anchor", "end").
            attr("style", "fill:white; font-size:9px");
        
        // draw rects
        barDemo.selectAll("rect").
          data(data).
          enter().
          append("svg:rect").
          attr("x", function(datum) { return x(datum.date) + xpadding; }).
          attr("y", function(datum) { return h - y(datum.value) + ypaddingTop; }).
          attr("height", function(datum) { return y(datum.value); }).
          attr("width", barWidth).
          attr("fill", function(datum){
              return getColorByDisease(datum.disease);
          });
	});
    
}
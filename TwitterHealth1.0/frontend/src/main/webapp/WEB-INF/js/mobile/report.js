// Map
// ----------------
// model and logic for the map

define(
    ["text!/resources/templates/mobile/report-modal.html"],
    function(reportModal) {
        // Constructor
        report = function(jElem, user, options) {
            this.jElem = jElem;
            this.user = user;
            this.symptom_count = 0;
            this.options = options || {};
            this.options.slider = { value: 98,
                                      min: 0,
                                      max: 103 };
        };
        
        // Instance Methods
        report.prototype = {
            // init: asynchronous initialization (i.e. we had to wait on
            // some event to get certain data)
            init: function() {
                var self = this;
                self.jElem.click(function(){
                    self.openReportModal();
                });
            },

            openReportModal: function() {
                var self = this;
                $('.modal').html(_.template(reportModal)).modal();
                $('.modal-report-symptom').each(function(){
                    $(this).click(function(){
                        self.markSymptom($(this).children('span'))
                    });
                });
                $('#modal_report_slider').slider(self.options.slider);
                $('#modal_report_slider').bind( "slide", function(event, ui) {
                  if (ui.value > (self.options.slider.max - 5)) {
                    return false;
                  }

                  self.toggleSymptomsSelection(ui.value);

                });
                $('#modal_report_submit').click(function() {
                    self.submitReport();
                });
                $('.modal-report-symptoms').hide() && $('.modal-report-hr').hide()
            },

            markSymptom: function(jElem) {
                var self = this;
                // Check if the button is the no symptoms button
                if (jElem.parent().attr('id') === 'modal_report_no_symptoms') {
                    // if it was and the button wasn't active, make it active, otherwise leave it alone;
                    if (!jElem.hasClass('active')) {
                        jElem.addClass('active');
                        self.symptom_count = 0;
                    }
                } else {
                    self.toggleSymptom(jElem)
                }

                if (self.symptom_count == 0) {
                    self.resetSymptoms();
                } else {// Clear the no symptoms button since at least one symptom has been marked
                    $('#modal_report_no_symptoms span').removeClass('active');
                }

            },

            toggleSymptomsSelection: function(val) {
                if (val < 93) {
                    $('.modal-report-symptoms').show() && $('.modal-report-hr').show()
                } else {
                    this.resetSymptoms();
                    $('.modal-report-symptoms').hide() && $('.modal-report-hr').hide()
                }
                
            },

            toggleSymptom: function(jElem) {
                var self = this;
                if (jElem.hasClass('active')) {
                    jElem.removeClass('active');
                    self.symptom_count -= 1;
                } else {
                    jElem.addClass('active');
                    self.symptom_count += 1;
                }
            },
            
            getSymptoms: function() {
                symptoms = [];
                $(".modal-report-symptom").has(".active").each(function(index) {
                    symptoms.push($(this).text());
                });
                return symptoms;
            },

            resetSymptoms: function(){
                $('.modal-report-symptom span').each(function(){
                    $(this).removeClass('active');
                });
                $('#modal_report_no_symptoms span').addClass('active');
            },

            submitReport: function(){
                // hack up a health rating (-1.0 to 1.0)
                var value = $('#modal_report_slider').slider("value");
                var min = this.options.slider.min;
                var max = this.options.slider.max;
                var rating = (value - min) / (max - min) * 2.0 - 1.0;
                
                // model to send to endpoint
                var submission = {
                    'geo': _.latLngToCoordinates(this.user.location),
                    'health': rating,
                    'symptoms': this.getSymptoms(),
                    'twitter_id': "", // we can fill this in if/when we include twitter syncing
                    'user_id': this.user._id,
                    'created_at': _.currentTimeAsTwitterFormat()
                };
                console.log(submission);
                
                // submit data
                $.ajax({
                    url: '/m/report',
                    type: "POST",
                    data: JSON.stringify(submission),
                    contentType: "application/json",
                    dataType: "text/plain",
                    async: true,
                    success: function() {
                        console.log('success');
                    }
                });
                $('.modal').modal('hide');
            }
        };
        
        return report;
    });


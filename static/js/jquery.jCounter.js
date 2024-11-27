;(function($,document,window,undefined) {
	$.fn.jCounter = function(options, callback) {
		var jCounterDirection = 'down'; // Points out whether it should count down or up | handled via customRange setting
		var customRangeDownCount; // If true, it will tell countdown_proc() it's a down count and not an up count
		var days, hours, minutes, seconds;
		var endCounter = false; // Stops jCounter if true
		var eventDate; // Time target (holds a number of seconds)
		var pausedTime; // Stores the time (in seconds) when pausing
		var thisEl = this; // Custom 'this' selector
		var thisLength = this.length; // Number of multiple elements per selector

		var pluralLabels = ['DAYS', 'HOURS', 'MINUTES', 'SECONDS']; // Plural labels
		var singularLabels = ['DAY', 'HOUR', 'MINUTE', 'SECOND']; // Singular labels

		this.options = options; // Stores jCounter's options parameter to verify against specified methods
		this.version = '0.1.4';

		// Default settings
		var settings = {
			animation: null,
			callback: null,
			customDuration: null,
			customRange: null,
			date: null,
			debugLog: false,
			serverDateSource: 'dateandtime.php',
			format: 'dd:hh:mm:ss',
			timezone: 'Europe/London',
			twoDigits: 'on'
		};

		// Merge the settings with the options values
		if (typeof options === 'object') {
			$.extend(settings, options);
			thisEl.data("userOptions", settings); // Push the settings to applied elements (they're used by methods)
		}

		if (thisEl.data('userOptions').debugLog == true && window['console'] !== undefined) {
			var consoleLog = true; // Shows debug messages via console.log() if true
		}

		// METHODS
		var jC_methods = {
			init: function() {
				thisEl.each(function(i, el) {
					initCounter(el);
				});
			},
			pause: function() {
				if (consoleLog) { console.log("(jC) Activity: Counter paused."); }
				endCounter = true;
				return thisEl.each(function(i, el) {
					clearInterval($(el).data("jC_interval"));
				});
			},
			stop: function() {
				if (consoleLog) { console.log("(jC) Activity: Counter stopped."); }
				endCounter = true;
				return thisEl.each(function(i, el) {
					clearInterval($(el).data("jC_interval"));
					$(el).removeData("jC_pausedTime");
					resetHTMLCounter(el);
				});
			},
			reset: function() {
				if (consoleLog) { console.log("(jC) Activity: Counter reset."); }
				return thisEl.each(function(i, el) {
					clearInterval($(el).data("jC_interval"));
					resetHTMLCounter(el);
					initCounter(el);
				});
			},
			start: function() {
				if (consoleLog) { console.log("(jC) Activity: Counter started."); }
				return thisEl.each(function(i, el) {
					pausedTime = $(el).data("jC_pausedTime");
					endCounter = false;
					clearInterval($(el).data("jC_interval"));
					initCounter(el);
				});
			}
		};

		// Initialize Counter
		function initCounter(el) {
			if (settings.customDuration) {
				// If custom duration is set
				if (pausedTime) {
					if (!isNaN(pausedTime)) {
						eventDate = Math.round(pausedTime);
					}
				} else {
					eventDate = Math.round($(el).data("userOptions").customDuration);
				}
				currentTime = 0;
				countdown_proc(currentTime, el);
				$(el).data("jC_interval", setInterval(function() {
					if (endCounter == false) {
						currentTime = parseInt(currentTime) + 1;
						countdown_proc(currentTime, el);
					}
				}, 1000));
			} else if (settings.customRange) {
				// If custom range is set
				var customRangeValues = settings.customRange.split(":");
				var rangeVal0 = parseInt(customRangeValues[0]);
				var rangeVal1 = parseInt(customRangeValues[1]);
				eventDate = rangeVal1;
				var currentTime = rangeVal0;
				countdown_proc(currentTime, el);
				$(el).data("jC_interval", setInterval(function() {
					if (endCounter == false) {
						var ifRangeDownCount = (customRangeDownCount) ? currentTime = parseInt(currentTime) - 1 : currentTime = parseInt(currentTime) + 1;
						countdown_proc(currentTime, el);
					}
				}, 1000));
			} else {
				// If date is set
				eventDate = Date.parse(settings.date) / 1000;
				var currentDate = Math.floor($.now() / 1000);
				startCounter(currentDate, el);
			}
		}

		function startCounter(currentDate, el) {
			countdown_proc(currentDate, el);
			if (eventDate > currentDate) {
				$(el).data("jC_interval", setInterval(function() {
					if (endCounter == false) {
						currentDate = parseInt(currentDate) + 1;
						countdown_proc(currentDate, el);
					}
				}, 1000));
			} else {
				resetHTMLCounter(el);
			}
		}

		function countdown_proc(duration, el) {
			// Check if the counter needs to count down or up
			if (eventDate <= duration) {
				clearInterval($(el).data("jC_interval"));
				if (settings.callback) {
					settings.callback.call(this);
				}
			}

			// Calculate the remaining time (days, hours, minutes, seconds)
			var seconds = eventDate - duration;
			var days = Math.floor(seconds / (60 * 60 * 24));
			seconds -= days * 60 * 60 * 24;
			var hours = Math.floor(seconds / (60 * 60));
			seconds -= hours * 60 * 60;
			var minutes = Math.floor(seconds / 60);
			seconds -= minutes * 60;

			// If the twoDigits setting is on, ensure each value is two digits
			if (settings.twoDigits == 'on') {
				days = String(days).padStart(2, '0');
				hours = String(hours).padStart(2, '0');
				minutes = String(minutes).padStart(2, '0');
				seconds = String(seconds).padStart(2, '0');
			}

			// Update the HTML elements
			$(el).find(".days").text(days);
			$(el).find(".hours").text(hours);
			$(el).find(".minutes").text(minutes);
			$(el).find(".seconds").text(seconds);

			// Stores the remaining time when pausing jCounter
			$(el).data("jC_pausedTime", eventDate - duration);
		}

		// Reset the HTML counter to zero or two digits
		function resetHTMLCounter(el) {
			$(el).find(".days,.hours,.minutes,.seconds").text('00');
		}

		// Method calling logic
		if (jC_methods[this.options]) {
			return jC_methods[this.options].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof this.options === 'object' || !this.options) {
			return jC_methods.init.apply(this, arguments);
		} else {
			console.log('(jC) Error: Method >>> ' + this.options + ' <<< does not exist.');
		}
	}
})(jQuery, document, window);

// --- Match timing ---
//
// Durations of the different match periods, in seconds.
// AUTO_LENGTH: Duration of autonomous.
// PAUSE_LENGTH: Duration of the pause between auto and teleop.
// TELEOP_LENGTH: The duration of teleop, including the endgame time.
// WARNING_LENGTH: The duration of the warning period or endgame. This is considered part of teleop.

var AUTO_LENGTH = 15;
var PAUSE_LENGTH = 5;
var TELEOP_LENGTH = 135;
var WARNING_LENGTH = 30;

var MATCH_LENGTH = AUTO_LENGTH + TELEOP_LENGTH;

var theMatch;

function readFile(filename, responder) {
	var oReq = new XMLHttpRequest();
	oReq.onload = responder;
	oReq.open("get", filename, true);
	oReq.send();
}

function matchResponder() {
	theMatch = $.parseJSON(this.responseText);

	$('#red').text(theMatch.alliances.red.score);
	$('#blue').text(theMatch.alliances.blue.score);

	if (theMatch.coopertition_achieved)
		$('#coop').show();
	else
		$('#coop').hide();

	$('#red-teams .team-number').each(function(i) {
		var team = theMatch.alliances.red.teams[i];
		$(this).text(team.substring(3, team.length));
	});
	$('#blue-teams .team-number').each(function(i) {
		var team = theMatch.alliances.blue.teams[i];
		$(this).text(team.substring(3, team.length));
	});

	$('#match_number').text(theMatch.match_number);
}

function showView(view) {
	if ( $(view).hasClass('hidden') )
		$(view).removeClass('hidden').transition({ x: '0%' });
}

function hideView(view) {
	if ( !$(view).hasClass('hidden') )
		$(view).addClass('hidden').transition({ x: '100%' });
}

function viewResponder() {
	var view = $.parseJSON(this.responseText).view;
	$( '.view' ).not( '#' + view ).each(function() { hideView(this) });
	$( '#' + view ).each(function() { showView(this) });
}

function updateTimer() {
	if (theMatch.match_running) {
		var elapsedSeconds = Math.floor((Date.now() - parseInt(theMatch.start_time)) / 1000);

		var output;
		if (elapsedSeconds < AUTO_LENGTH) {
			output = MATCH_LENGTH - elapsedSeconds;
		}
		else if (elapsedSeconds < AUTO_LENGTH + PAUSE_LENGTH) {
			output = MATCH_LENGTH - AUTO_LENGTH;
		}
		else {
			output = MATCH_LENGTH - (elapsedSeconds - PAUSE_LENGTH);
		}

		if (output < 0)
			output = 0;
		
		$('#timer').text(output);
		
		$('.timer-fill').css('width', ((MATCH_LENGTH - output) / MATCH_LENGTH) * 100 + "%");
		if (output == 0)
			$('.timer-fill').addClass('red');
		else if (output <= WARNING_LENGTH)
			$('.timer-fill').addClass('yellow');
		else
			$('.timer-fill').removeClass('red yellow');
	}
}

$(document).ready(function() {
	setInterval(function() { readFile("match.json", matchResponder); }, 1000);
	setInterval(function() { readFile("view.json", viewResponder); }, 1000)
	setInterval(function() { updateTimer(); }, 50);
});

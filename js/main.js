var MATCH_LENGTH = 150;

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
		var secondsLeft = MATCH_LENGTH - elapsedSeconds;
		if (secondsLeft < 0)
			secondsLeft = 0;

		var output;
		if (secondsLeft >= MATCH_LENGTH - 15)
			output = secondsLeft - (MATCH_LENGTH - 15);
		else
			output = secondsLeft;

		$('#timer').text(output);

		$('.timer-fill').css('width', ((MATCH_LENGTH - secondsLeft) / MATCH_LENGTH) * 100 + "%");
		if (secondsLeft == 0)
			$('.timer-fill').addClass('red');
		else if (secondsLeft <= 30)
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

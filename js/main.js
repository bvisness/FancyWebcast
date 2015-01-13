var theMatch;

function matchResponder() {
	var matches = $.csv.toObjects(this.responseText);
	theMatch = matches[0]
	$('#red').text(theMatch.redscore);
	$('#blue').text(theMatch.bluescore);
}

function updateTimer() {
	var elapsedSeconds = Math.floor((Date.now() - parseInt(theMatch.starttime)) / 1000);
	var secondsLeft = 150 - elapsedSeconds;
	var output;
	if (secondsLeft >= 135)
		output = secondsLeft - 135;
	else if (secondsLeft < 0)
		output = 0;
	else
		output = secondsLeft;
	$('#timer').text(output);
}

function readFile(filename, responder) {
	var oReq = new XMLHttpRequest();
	oReq.onload = responder;
	oReq.open("get", filename, true);
	oReq.send();
}

$(document).ready(function() {
	setInterval(function() { readFile("match.csv",matchResponder); }, 1000);
	setInterval(function() { updateTimer(); }, 50);
});
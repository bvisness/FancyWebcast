// --- Match timing ---
//
// Durations of the different match periods, in seconds.
// AUTO_LENGTH: Duration of autonomous.
// PAUSE_LENGTH: Duration of the pause between auto and teleop.
// TELEOP_LENGTH: The duration of teleop, including the endgame time.
// WARNING_LENGTH: The duration of the warning period or endgame. This is considered part of teleop.

var AUTO_LENGTH = 15;
var TELEOP_LENGTH = 135;
var WARNING_LENGTH = 30;

var MATCH_LENGTH = AUTO_LENGTH + TELEOP_LENGTH;

var theMatch;

$(document).ready(function() {
	setInterval(function() { readFile("match.json", matchResponder); }, 1000);
	setInterval(function() { readFile("view.json", viewResponder); }, 1000)
	setInterval(function() { readFile("rankings.json", rankingsResponder); }, 1000);
	setInterval(function() { updateTimer(); }, 50);
});

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

	if (theMatch.alliances.red.score_breakdown) {
		var r = theMatch.alliances.red.score_breakdown;
		$('#red-results .auto').text(r.auto);
		$('#red-results .tote').text(r.tote);
		$('#red-results .container').text(r.container);
		$('#red-results .litter').text(r.litter);
		$('#red-results .foul').text(r.foul);

		var b = theMatch.alliances.blue.score_breakdown;
		$('#blue-results .auto').text(b.auto);
		$('#blue-results .tote').text(b.tote);
		$('#blue-results .container').text(b.container);
		$('#blue-results .litter').text(b.litter);
		$('#blue-results .foul').text(b.foul);
	}
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

function rankingsResponder() {
	var rankings = $.parseJSON(this.responseText);
	updateRankings(rankings);
}

function updateTimer() {
	if (theMatch.match_running) {
		var secondsFromStart = Math.floor((Date.now() - parseInt(theMatch.start_time)) / 1000);
		var secondsFromTeleop = Math.floor((Date.now() - parseInt(theMatch.teleop_time)) / 1000);

		var output;
		if ( isNaN(secondsFromTeleop) ) {
			if (secondsFromStart >= AUTO_LENGTH)
				output = MATCH_LENGTH - AUTO_LENGTH;
			else
				output = MATCH_LENGTH - secondsFromStart;
		}
		else {
			output = MATCH_LENGTH - AUTO_LENGTH - secondsFromTeleop;
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
	else if (!theMatch.start_time) {
		$('#timer').text(150);
		$('.timer-fill').css('width', 0);
		$('.timer-fill').removeClass('red yellow');
	}
}

var delayTimer;
var scrollTimer;

function updateRankings(rankings) {
	if ( $('#rankings').hasClass('hidden') ) {
		$('#rankings').removeClass('scrolling');
		resetScroll();
	}
	if ( !($('#rankings').hasClass('scrolling')) ) {
		$( '#rankings tbody tr' ).not( '.prototype' ).remove();
		var prototype = $( '#rankings .ranking.prototype' );
		for (var i = 1; i < rankings.length; i++) {
			var newRanking = $( prototype ).clone();
			// var newRankings = $( prototype ).clone().append( prototype );

			var rank = i;
			var teamNumber = rankings[i].number;
			// var niceTeamNumber = teamNumber.substring(3, teamNumber.length);
			var qualAvg = rankings[i].qualification_average;
			var coop = rankings[i].coopertition_sum;
			var auto = rankings[i].auto_sum;
			var container = rankings[i].container_sum;
			var tote = rankings[i].tote_sum;
			var litter = rankings[i].litter_sum;
			var played = rankings[i].played;

			$( newRanking ).find( '.rank' ).text(rank);
			$( newRanking ).find( '.team' ).text(teamNumber);
			$( newRanking ).find( '.qualification-average' ).text(qualAvg);
			$( newRanking ).find( '.coopertition-sum' ).text(coop);
			$( newRanking ).find( '.auto-sum' ).text(auto);
			$( newRanking ).find( '.container-sum' ).text(container);
			$( newRanking ).find( '.tote-sum' ).text(tote);
			$( newRanking ).find( '.litter-sum' ).text(litter);
			$( newRanking ).find( '.played' ).text(played);

			$( newRanking ).removeClass('prototype');

			$( '#rankings tbody' ).append( newRanking );
		}
		scrollRankings();
	}

	function getRule() {
		var ss = document.styleSheets[0];
		var rules = ss.cssRules || ss.rules;
		var tdRule = null;
		for (var i = 0; i < rules.length; i++)
		{
			var rule = rules[i];
			if (/\.scrolling.*\.rankcell$/.test(rule.selectorText))
			{
				tdRule = rule;
				break;
			}
		}
		return tdRule;
	}

	function resetScroll() {
		var rule = getRule();
		rule.style.transition = "";
		rule.style.transform = "";
		clearTimeout(delayTimer);
		clearTimeout(scrollTimer);
	}

	function scrollRankings() {
		// Delay before and after scrolling, in seconds
		var SCROLL_DELAY = 4;
		// Scroll speed in seconds per ranking
		var RANKING_SPEED = 1;

		var ss = document.styleSheets[0];
		var rules = ss.cssRules || ss.rules;
		var tdRule = null;
		for (var i = 0; i < rules.length; i++)
		{
			var rule = rules[i];
			if (/\.scrolling.*\.rankcell$/.test(rule.selectorText))
			{
				tdRule = rule;
				break;
			}
		}

		$( '#rankings' ).addClass('scrolling');

		var numRankings = $('.ranking').not('.prototype').length;

		var titleHeight = $('#rankings .header').height();
		var windowHeight = $( '#rankings' ).height();
		var visibleHeight = windowHeight - titleHeight;
		var rankingHeight = $('#rankings tr').height();
		var allHeight = rankingHeight * numRankings;
		var scrollHeight = allHeight - visibleHeight;

		var secondsPerPx = RANKING_SPEED / rankingHeight;
		var scrollTime = secondsPerPx * scrollHeight;

		delayTimer = setTimeout(function() {
			tdRule.style.transition = "transform " + scrollTime + "s linear";
			tdRule.style.transform = "translateY(" + -scrollHeight + "px)";
			scrollTimer = setTimeout(function() {
				$( '#rankings' ).removeClass('scrolling');
				resetScroll();
			}, (scrollTime + SCROLL_DELAY) * 1000);
		}, SCROLL_DELAY * 1000);
	}
}

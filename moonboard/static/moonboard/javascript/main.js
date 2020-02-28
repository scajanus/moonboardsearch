const results_div = $('#replaceable-content')
const selected_problem_name = $('#replaceable-name')
var hold_overlap_slider = document.getElementById("hold-overlap");
const endpoint = '/problems'
const delay_by_in_ms = 1000
let scheduled_function = false
sessionStorage.removeItem('hold')

function filterRoutes(minOverlap){
  // TODO: Call getProblemList with current set of holds & setYear
  var setYear = sessionStorage.getItem('setYear') || '2016';
  var setAngle = sessionStorage.getItem('setAngle') || '40';
  var minGrade = sessionStorage.getItem('minGrade') || '5+';
  var maxGrade = sessionStorage.getItem('maxGrade') || '8B+';

  holdsjson = sessionStorage.getItem('hold')

  if (holdsjson) {
    current_holds = JSON.parse(holdsjson)
  } else {
    current_holds = []
  }
  console.log('min' + minGrade);
  getProblemList(current_holds, setYear, setAngle, minOverlap, minGrade, maxGrade)
}

function changeSetYear() {
  // Get the checkbox
  var checkBox = document.getElementById("setYearCheckbox");

  // If the checkbox is checked, display the output text
  if (document.getElementById('set2017').checked){
    sessionStorage.setItem('setYear', 2017)
    document.getElementById("search-board").style.backgroundImage = "url('/static/moonboard/mbsetup-mbm2017-min.jpg')"
    document.getElementById("result-board").style.backgroundImage = "url('/static/moonboard/mbsetup-mbm2017-min.jpg')"
  } else if (document.getElementById('set2019').checked) {
    sessionStorage.setItem('setYear', 2019)
    document.getElementById("search-board").style.backgroundImage = "url('/static/moonboard/mbsetup-mbm2019-min.jpg')"
    document.getElementById("result-board").style.backgroundImage = "url('/static/moonboard/mbsetup-mbm2019-min.jpg')"
  } else {
    sessionStorage.setItem('setYear', 2016)
    document.getElementById("result-board").style.backgroundImage = "url('/static/moonboard/mbsetup-2016-min.jpg')"
    document.getElementById("search-board").style.backgroundImage = "url('/static/moonboard/mbsetup-2016-min.jpg')"

  }
}

function changeSetAngle() {
  // Get the checkbox
  var checkBox = document.getElementById("setAngleCheckbox");
  //console.log('checkbox' + checkBox.checked)

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    sessionStorage.setItem('setAngle', 25)
  } else {
    sessionStorage.setItem('setAngle', 40)
  }

  holdsjson = sessionStorage.getItem('hold')
  if (holdsjson) {
    current_holds = JSON.parse(holdsjson)
  } else {
    current_holds = []
  }
  sessionStorage.setItem('hold', JSON.stringify(current_holds))
  getProblemList(holds=current_holds)



  console.log('setAngle'+sessionStorage.getItem('setAngle'))
}

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			// fade out the results_div, then:
			results_div.fadeTo('slow', 0).promise().then(() => {
				// replace the HTML contents
				results_div.html(response['html_from_view'])
				// fade-in the div with new contents
				results_div.fadeTo('slow', 1)
			})
		})
}

let problem_ajax_call = function (endpoint, request_parameters) {
  $.getJSON(endpoint, request_parameters)
  .done(response => {
    selected_problem_name.html(response['name'] + ' ' + response['grade'])
    $('.result-board button').fadeTo('fast', 0).promise().then(() => {
    $('.result-board button').removeClass('blue-button red-button green-button')

    response['holds'].forEach(hold => {
      if(hold[1]) {
        classToAdd = 'green-button'
      }
      else if (hold[2]) {
        classToAdd = 'red-button'

      }
      else {
        classToAdd = 'blue-button'
      }
      document.getElementById('result-' + hold[0]).classList = "nonclickable-led-button " + classToAdd;

    });
    $('.result-board button').fadeTo('slow', 1)

  });

  })
}

function toggleButton(buttonId) {
    var classes = document.getElementById(buttonId).classList;

    holdsjson = sessionStorage.getItem('hold')

    if (holdsjson) {
      current_holds = JSON.parse(holdsjson)
    } else {
      current_holds = []
    }

    if(classes.length == 1) {
      //Currently off, turn blue
      classToAdd = "blue-button";
      current_holds.push(buttonId)
    }
    else if(classes.item(1) == "blue-button") {
      //Currently blue, turn off
      classToAdd = ""
      current_holds.splice($.inArray(buttonId, current_holds), 1);
    }
    document.getElementById(buttonId).classList = "led-button " + classToAdd;
    sessionStorage.setItem('hold', JSON.stringify(current_holds))
    getProblemList(holds=current_holds)
}

function toggleProblem(problemId) {
  console.log('toggle' + problemId)

  const request_parameters = {
    problemId: problemId,
    'no-cache': new Date().getTime()
  }

  if (scheduled_function) {
		clearTimeout(scheduled_function)
  }

  scheduled_function = setTimeout(problem_ajax_call, delay_by_in_ms, '/problemjson', request_parameters)

}

function getProblemList(holds, setYear, setAngle, minOverlap, minGrade, maxGrade, minHolds, maxHolds, sortedBy) {
  if(!setYear) {
    var setYear = sessionStorage.getItem('setYear') || '2017';
  }
  if(!setAngle) {
    var setAngle = sessionStorage.getItem('setAngle') || '40';
  }
  const request_parameters = {
    hold: holds,
    min_grade: minGrade,
    max_grade: maxGrade,
    min_overlap: minOverlap,
    set_year: setYear,
    set_angle: setAngle,
    min_holds: minHolds,
    max_holds: maxHolds,
    sortedBy: sortedBy,
    'no-cache': new Date().getTime(),
  }
  if (scheduled_function) {
    clearTimeout(scheduled_function)
  }
  scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
}

const results_div = $('#replaceable-content')
const selected_problem_name = $('#replaceable-name')
var hold_overlap_slider = document.getElementById("hold-overlap");
const endpoint = '/'
const delay_by_in_ms = 1000
let scheduled_function = false
sessionStorage.removeItem('hold')

function filterRoutes(overlap){
  var i;
  for (i = 1; i < 50; i++) {
    $('.match-' + i).removeClass('d-none')
  } 
  for (i = 1; i < overlap; i++) {
    $('.match-' + i).addClass('d-none')
  } 
  
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
      document.getElementById('result-' + hold[0]).classList = "led-button " + classToAdd;

    });
    $('.result-board button').fadeTo('slow', 1)

  });

  })
}

function toggleButton(buttonId) {
    // console.log(buttonId);
    var classes = document.getElementById(buttonId).classList;
  
    var data = {
        color: ""
      };

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

    const request_parameters = {
      hold: current_holds,
      nocache: new Date().getTime()
    }

    	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
}

function toggleProblem(problemId) {
  console.log('toggle' + problemId)

  const request_parameters = {
    problemId: problemId,
    nocache: new Date().getTime()
  }

  if (scheduled_function) {
		clearTimeout(scheduled_function)
  }

  scheduled_function = setTimeout(problem_ajax_call, delay_by_in_ms, '/problemjson', request_parameters)

}

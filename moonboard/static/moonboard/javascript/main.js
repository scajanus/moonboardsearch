// This version is OK Kenny

const results_div = $('#replaceable-content')
const selected_problem_name = $('#replaceable-name')
var hold_overlap_slider = document.getElementById("hold-overlap");
const endpoint = '/problems'
const delay_by_in_ms = 1000
let scheduled_function = false
sessionStorage.removeItem('hold')

function filterRoutes(minOverlap){
  // TODO: Call getProblemList with current set of holds & setYear
  var setYear = sessionStorage.getItem('setYear') || '2017';
  var setAngle = sessionStorage.getItem('setAngle') || '40';
  var minGrade = sessionStorage.getItem('minGrade') || '5+';
  var maxGrade = sessionStorage.getItem('maxGrade') || '8B+';

  holdsjson = sessionStorage.getItem('hold')

  if (holdsjson) {
    current_holds = JSON.parse(holdsjson)
  } else {
    current_holds = []
  }
  holdsjson = sessionStorage.getItem('nothold')

  if (notholdsjson) {
    current_notholds = JSON.parse(notholdsjson)
  } else {
    current_notholds = []
  }
  getProblemList(current_holds, current_notholds, setYear, setAngle, minOverlap, minGrade, maxGrade)
}

function changeSetYear() {
  // Get the checkbox
  var holdsetsSelected = sessionStorage.getItem('holdsetsSelected')
  // If the checkbox is checked, display the output text
  if (document.getElementById('set2017').checked){
    sessionStorage.setItem('setYear', '2017')
    document.getElementById("setangle").style="display:inline";
    var arrayLength = holdsetsSelected.length;
    for (var i = 0; i < arrayLength; i++) {
        holdset = holdsetsSelected[i];
        console.log('i'+i)
    }
  } else if (document.getElementById('set2019').checked) {
    sessionStorage.setItem('setYear', '2019')
    document.getElementById("setangle").style="display:inline";
  } else {
    sessionStorage.setItem('setYear', '2016')
    document.getElementById("setangle").style="display:none";
  }
  setYear = sessionStorage.getItem('setYear')
  if (setYear == '2016') {
    holdsetsSelected = ['A','B','school']
  } else if (setYear == '2017') {
    holdsetsSelected = ['A','B','C','wood','school']
  } else if  (setYear == '2019') {
    holdsetsSelected = ['A','B','wood','woodB','woodC','school']
  }
  sessionStorage.setItem('holdsetsSelected', JSON.stringify(holdsetsSelected));
  $('#replaceable-name').html('Selected route')
  document.getElementById("replaceable-content").scrollTop;
  $('.result-board button').removeClass('blue-button red-button green-button');
  $('#search-board button').removeClass('blue-button red-button green-button');

  sessionStorage.setItem('hold', JSON.stringify([]))
  sessionStorage.setItem('nothold', JSON.stringify([]))
  setYear = sessionStorage.getItem('setYear') || '2017'
  setAngle = sessionStorage.getItem('setAngle') || '40'

  min_overlap = sessionStorage.getItem('min_overlap',0)

  getProblemList(holds=[], notholds=[], setYear, setAngle, min_overlap , '5+','8B+',3,20,'',holdssetSelected=holdsetsSelected)
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
  setYear = sessionStorage.getItem('setYear')
  if (setYear == '2016') {
    holdsetsSelected = ['A','B','school']
  } else if (setYear == '2017') {
    holdsetsSelected = ['A','B','C','wood','school']
  } else if  (setYear == '2019') {
    holdsetsSelected = ['A','B','wood','woodB','woodC','school']
  }
  sessionStorage.setItem('holdsetsSelected', JSON.stringify(holdsetsSelected));

  $('#replaceable-name').html('Selected route')
  document.getElementById("replaceable-content").scrollTop;
  $('.result-board button').removeClass('blue-button red-button green-button');
  $('#search-board button').removeClass('blue-button red-button green-button');

  sessionStorage.setItem('hold', JSON.stringify([]))
  sessionStorage.setItem('nothold', JSON.stringify([]))
  setYear = sessionStorage.getItem('setYear') || '2017'
  setAngle = sessionStorage.getItem('setAngle') || '40'

  min_overlap = sessionStorage.getItem('min_overlap',0)

  getProblemList(holds=[], notholds=[], setYear, setAngle, min_overlap , '5+','8B+',3,20,'',holdssetSelected=holdsetsSelected)




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
    selected_problem_name.html(response['name'] + ' <span style="font-weight: bold">' + response['grade'] + '</span>')
    $('.result-board button').fadeTo('fast', 0).promise().then(() => {
    $('.result-board button').removeClass('blue-button red-button green-button')
    console.log('Response '+response);
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

    setYear = sessionStorage.getItem('setYear') || '2017';
    var holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson === null) {
      if (setYear == '2016') {
        holdsetsSelected = ['A','B','school']
      } else if (setYear == '2017') {
        holdsetsSelected = ['A','B','C','wood','school']
      } else if  (setYear == '2019') {
        holdsetsSelected = ['A','B','C','wood','school']
      }
      sessionStorage.setItem('holdsetsSelected', JSON.stringify(holdsetsSelected));
    }
    $('#btnA').removeClass('selected')
    $('#btnB').removeClass('selected')
    $('#btnC').removeClass('selected')
    $('#btnwood').removeClass('selected')
    $('#btnwoodB').removeClass('selected')
    $('#btnwoodC').removeClass('selected')
    $('#btnschool').removeClass('selected')
    holdsetsSelected =  JSON.parse(holdsetsSelectedjson)
    console.log('in selected setting' +  holdsetsSelected)
    if (holdsetsSelected.includes('A')) { $('#btnA').addClass('selected') }
    if (holdsetsSelected.includes('B')) { $('#btnB').addClass('selected') }
    if (holdsetsSelected.includes('C')) { $('#btnC').addClass('selected') }
    if (holdsetsSelected.includes('wood')) { $('#btnwood').addClass('selected') }
    if (holdsetsSelected.includes('woodB')) { $('#btnwoodB').addClass('selected') }
    if (holdsetsSelected.includes('woodC')) { $('#btnwoodC').addClass('selected') }
    if (holdsetsSelected.includes('school')) { $('#btnschool').addClass('selected') }
    backgroundcss = []
    blendcss =  []

    var arrayLength = holdsetsSelected.length;
    for (var i = 0; i < arrayLength; i++) {
        holdset = holdsetsSelected[i];
        console.log('i'+holdset)
        backgroundcss.push("url(/static/moonboard/" + setYear + "/" +  holdset +  ".png)")
        blendcss.push('darken')
    }
    backgroundcss.push('url(/static/moonboard/moonboard-background.png)')
    blendcss.push('normal')
    $('#search-board').css('background-image', backgroundcss.join(',')).css('background-blend-mode', blendcss.join(','))
    $('#result-board').css('background-image', backgroundcss.join(',')).css('background-blend-mode', blendcss.join(','))

    $('.result-board button').fadeTo('slow', 1)

  });

  })
}

function toggleButton(buttonId) {
    var classes = document.getElementById(buttonId).classList;

    holdsjson = sessionStorage.getItem('hold')
    notholdsjson = sessionStorage.getItem('nothold')

    if (holdsjson) {
      current_holds = JSON.parse(holdsjson)
    } else {
      current_holds = []
    }
    if (notholdsjson) {
      current_notholds = JSON.parse(notholdsjson)
    } else {
      current_notholds = []
    }
    holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson) {
      current_holdsetsSelected = JSON.parse(holdsetsSelectedjson)
    } else {
      current_holdsetsSelected = []
    }

    console.log('1 ' +current_holds)
    console.log('1-not ' +current_notholds)
    if(classes.length == 1) {
      //Currently off, turn blue
      console.log('currently off, pushing'+buttonId)
      classToAdd = "blue-button";
      current_holds.push(buttonId)
    }
    else if(classes.item(1) == "blue-button" || classes.item(1) == "red-button") {
      //Currently blue, turn off
      console.log('currently blue  or red')
      if  (classes.item(1) == "blue-button") {
        console.log('currently blue')
        classToAdd  = "red-button"
        current_holds.splice($.inArray(buttonId, current_holds), 1)
        current_notholds.push(buttonId)
      } else {
        console.log('currently red')
        classToAdd = ""
        current_notholds.splice($.inArray(buttonId, current_holds), 1)
      }
    }
    console.log('2 ' +current_holds)
    console.log('2-not ' +current_notholds)
    document.getElementById(buttonId).classList = "led-button " + classToAdd;
    sessionStorage.setItem('hold', JSON.stringify(current_holds))
    sessionStorage.setItem('nothold', JSON.stringify(current_notholds))
    setYear = sessionStorage.getItem('setYear') || '2017'
    setAngle = sessionStorage.getItem('setAngle') || '40'
    min_overlap = sessionStorage.getItem('min_overlap',current_holds.length)
    getProblemList(holds=current_holds,  notholds=current_notholds, setYear, setAngle, min_overlap, '5+','8B+',3,20,'',current_holdsetsSelected)
}

function toggleProblem(problemId) {
  console.log('pretoggle')
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

function getProblemList(holds, notholds, setYear, setAngle, minOverlap, minGrade, maxGrade, minHolds, maxHolds, sortedBy, holdsetsSelected) {

  console.log('min_overlap in mainjs get Problem List '+ minOverlap)

  if(!setYear) {
    var setYear = sessionStorage.getItem('setYear') || '2017';
  }
  if(!setAngle) {
    var setAngle = sessionStorage.getItem('setAngle') || '40';
  }
  const request_parameters = {
    hold: holds,
    nothold:  notholds,
    min_grade: minGrade,
    max_grade: maxGrade,
    min_overlap: minOverlap,
    set_year: setYear,
    set_angle: setAngle,
    min_holds: minHolds,
    max_holds: maxHolds,
    sortedBy: sortedBy,
    holdsetsSelected: holdsetsSelected,
    'no-cache': new Date().getTime(),
  }
  if (scheduled_function) {
    clearTimeout(scheduled_function)
  }


  scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
}

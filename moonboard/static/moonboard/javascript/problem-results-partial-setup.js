console.log("ProblemResultsPartial-Javascript Start")
setYear = sessionStorage.getItem('setYear') || '2017';
var holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
if (holdsetsSelectedjson === null) {
    if (setYear == '2016') {
        holdsetsSelected = ['A','B','school']
    } else if (setYear == '2017') {
        holdsetsSelected = ['A','B','C','wood','school']
    } else if  (setYear == '2019') {
        holdsetsSelected = ['A','B','wood','woodB','woodC','school']
    }
    sessionStorage.setItem('holdsetsSelected', JSON.stringify(holdsetsSelected));
} else {
    holdsetsSelected = JSON.parse(holdsetsSelectedjson)
}
console.log(' - setYear = '+setYear)
console.log(' - holdsetsSelected = '+holdsetsSelected)
$('#btnA').removeClass('selected')
$('#btnB').removeClass('selected')
$('#btnC').removeClass('selected')
$('#btnwood').removeClass('selected')
$('#btnwoodB').removeClass('selected')
$('#btnwoodC').removeClass('selected')
$('#btnschool').removeClass('selected')
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
    backgroundcss.push("url(/static/moonboard/" + setYear + "/" +  holdset +  ".png)")
    blendcss.push('darken')
}
backgroundcss.push('url(/static/moonboard/moonboard-background.png)')
blendcss.push('normal')
$('#search-board').css('background-image', backgroundcss.join(',')).css('background-blend-mode', blendcss.join(','))
$('#result-board').css('background-image', backgroundcss.join(',')).css('background-blend-mode', blendcss.join(','))

$("#resetSearch").on("click", function () {
   console.log('Normal Reset')
   $('#replaceable-name').html('Selected route')
   document.getElementById("replaceable-content").scrollTop;
   $('.result-board button').removeClass('blue-button red-button green-button');
   $('#search-board button').removeClass('blue-button red-button green-button');
   sessionStorage.setItem('hold', JSON.stringify([]))
   sessionStorage.setItem('nothold', JSON.stringify([]))
   sessionStorage.setItem('min_overlap',0)

   setYear = sessionStorage.getItem('setYear') || '2017';
   setAngle = sessionStorage.getItem('setAngle') || '40';
   if (setYear == '2016') {
     holdsetsSelected = ['A','B','school']
   } else if (setYear == '2017') {
     holdsetsSelected = ['A','B','C','wood','school']
   } else if  (setYear == '2019') {
     holdsetsSelected = ['A','B','wood','woodB','woodC','school']
   }
   sessionStorage.setItem('holdsetsSelected', JSON.stringify(holdsetsSelected));
   getProblemList(holds=[], notholds=[], setYear, setAngle, null, '5+','8B+',3,20,'',holdssetSelected=holdsetsSelected)

})


$("#resetAll").on("click", function () {
 console.log('Full Reset')
 $('#replaceable-name').html('Selected route')
 document.getElementById("replaceable-content").scrollTop;
 $('.result-board button').removeClass('blue-button red-button green-button');
 $('#search-board button').removeClass('blue-button red-button green-button');
 sessionStorage.removeItem('hold')
 sessionStorage.removeItem('nothold')
 sessionStorage.removeItem('holdsetsSelected')
 sessionStorage.removeItem('min_overlap')
 sessionStorage.setItem('setYear','2017')
 sessionStorage.setItem('setAngle','40')
 sessionStorage.setItem('minGrade','5+')
 sessionStorage.setItem('maxGrade', '8B+')
 sessionStorage.setItem('minTick', 1)
 sessionStorage.setItem('maxTick', 17)
 setYear = '2017'
 setAngle = '40'
 if (setYear == '2016') {
   holdsetsSelected = ['A','B','school']
 } else if (setYear == '2017') {
   holdsetsSelected = ['A','B','C','wood','school']
 } else if  (setYear == '2019') {
   holdsetsSelected = ['A','B','wood','woodB','woodC','school']
 }
 sessionStorage.setItem('holdsetsSelected', JSON.stringify(holdsetsSelected));
 getProblemList(holds=[], notholds=[], setYear, setAngle, null, '5+','8B+',3,20,'',holdssetSelected=holdsetsSelected)
})

var holdsetups = JSON.parse('[{"Id":17,"Description":"MoonBoard Masters 2019","AllowClimbMethods":true,"MoonBoardConfigurations":[{"Id":1,"Description":"40° MoonBoard","LowGrade":"6A+","HighGrade":"8B+"},{"Id":2,"Description":"25° MoonBoard","LowGrade":"5+","HighGrade":"8B+"}]},{"Id":15,"Description":"MoonBoard Masters 2017","AllowClimbMethods":true,"MoonBoardConfigurations":[{"Id":1,"Description":"40° MoonBoard","LowGrade":"6A+","HighGrade":"8B+"},{"Id":2,"Description":"25° MoonBoard","LowGrade":"5+","HighGrade":"8B+"}]},{"Id":1,"Description":"MoonBoard 2016","AllowClimbMethods":false,"MoonBoardConfigurations":[]}]');
var ticks_labels = ["5","5+","6A","6A+","6B","6B+","6C","6C+","7A","7A+","7B","7B+","7C","7C+","8A","8A+","8B","8B+","8C"];
var moonSlider = document.getElementById('slider');
var minGrade, maxGrade, minTick, maxTick;
minGrade = sessionStorage.getItem('minGrade') || '5+';
maxGrade = sessionStorage.getItem('maxGrade') || '8B+';
minTick = sessionStorage.getItem('minTick') || 1;
maxTick = sessionStorage.getItem('maxTick') || 17 ;

setYear = sessionStorage.getItem('setYear') || '2017';
setAngle = sessionStorage.getItem('setAngle') || '40';
holdsjson = sessionStorage.getItem('hold')
notholdsjson = sessionStorage.getItem('nothold')

sortedBy = sessionStorage.getItem('sortedBy');
min_overlap = null


noUiSlider.create(moonSlider, {
   start: [minTick, maxTick],
   step: 1,
   connect: true,
   range: {
       'min': [0],
       'max': [18]
   },
   pips: {
       mode: 'values',
       values: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
       density: 19
   }
});

var $sliderMin = $(".noUi-handle-lower");
var $sliderMax = $(".noUi-handle-upper");

function sliderValueChanged(values, handle, unencoded, tap, positions) {
    console.log('sliderValueChanged')
    var tMin = ticks_labels[parseInt(values[0])];
    var tMax = ticks_labels[parseInt(values[1])];

    if (minGrade != tMin || maxGrade != tMax) {
        minGrade = tMin;
        maxGrade = tMax;
        sessionStorage.setItem('minTick', parseInt(values[0]));
        sessionStorage.setItem('maxTick', parseInt(values[1]));

        sessionStorage.setItem('minGrade', minGrade);
        sessionStorage.setItem('maxGrade', maxGrade);
    }
    var setYear = sessionStorage.getItem('setYear') || '2017';
    var setAngle = sessionStorage.getItem('setAngle') || '40';
    var sortedBy = sessionStorage.getItem('sortedBy');

    holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson) {
        current_holdsetsSelected = JSON.parse(holdsetsSelectedjson)
    } else {
        current_holdsetsSelected = []
    }
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
    min_overlap = null
    console.log(current_holds,current_notholds, setYear, setAngle, min_overlap,minGrade,maxGrade,3,20, sortedBy, current_holdsetsSelected);
    getProblemList(current_holds, current_notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, 3,20, sortedBy,current_holdsetsSelected)
}

function sliderIsSliding(values, handle, unencoded, tap, positions) {
    if ($sliderMin.position().left === $sliderMax.position().left) {
        if (handle == 0) {
            $sliderMax.css("z-index", 4);
        } else {
            $sliderMax.css("z-index", 5);
        }
    }

}

moonSlider.noUiSlider.on('slide', sliderIsSliding);
moonSlider.noUiSlider.on('change', sliderValueChanged);

function minOverlapSliderValueChanged(values, handle, unencoded, tap, positions) {
    console.log('minOverlapSliderValueChanged')
    min_overlap = parseInt(values[0])
    sessionStorage.setItem('min_overlap', min_overlap)
    var setYear = sessionStorage.getItem('setYear') || '2017';
    var setAngle = sessionStorage.getItem('setAngle') || '40';
    var sortedBy = sessionStorage.getItem('sortedBy');
    holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson) {
       current_holdsetsSelected = JSON.parse(holdsetsSelectedjson)
    } else {
       current_holdsetsSelected = []
    }
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
    var min_overlap = sessionStorage.getItem('min_overlap',current_holds.length)
    console.log(current_holds,current_notholds, setYear, setAngle, min_overlap,minGrade,maxGrade,3,20, sortedBy, current_holdsetsSelected)
    getProblemList(current_holds,  current_notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, 3,20, sortedBy,current_holdsetsSelected)
}



function updateSliderTicks() {
    var $nodes = $("#slider .noUi-value-large");
    $nodes.each( function (index, e) {
        if (index % 2 === 0) {
            e.innerHTML = ticks_labels[index];
        } else {
            e.innerHTML = " ";
        }
    })
}

updateSliderTicks();

$("button.btnGrade").on("click", function () {
    var $button = $(this);
    $button.toggleClass("unselected");
    var grades = $("button.btnGrade:not('.unselected')")
       .map( function () {
           return this.innerText;
       })
       .get()
       .join(",");
});


$("button.tabButton").on("click", function () {
    var $tabButton = $(this);
    $("button.tabButton").removeClass("selected");
    $("div.moon-tab").removeClass("active");
    var id = $tabButton.data("id");
    $tabButton.addClass('selected');
    $('div.moon-tab[data-id="' + id + '"]').addClass('active');
});

var selectedIndex = -1;
var currentProblem;

$(function () {
    Array.prototype.remove = function() {
        var what, a = arguments, L = a.length, ax;
        while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
             this.splice(ax, 1);
        }
     }
     return this;
}

$("#usetheseholdstosearch").click(function () {
    problem_holds = JSON.parse(sessionStorage.getItem('current_problem_holds'))

    console.log('problem_holds in use these holds' + problem_holds)
    var setYear = sessionStorage.getItem('setYear') || '2017';
    var setAngle = sessionStorage.getItem('setAngle') || '40';
    var minGrade = sessionStorage.getItem('minGrade') ||  '5+';
    var maxGrade = sessionStorage.getItem('maxGrade') || '8B+';
    var sortedBy = sessionStorage.getItem('sortedBy') || '';
    notholdsjson = sessionStorage.getItem('nothold')
    holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson) {
        current_holdsetsSelected = JSON.parse(holdsetsSelectedjson)
    } else {
        current_holdsetsSelected = []
    }
    if (notholdsjson) {
        current_notholds = JSON.parse(notholdsjson)
    } else {
        current_notholds = []
    }
    $('#replaceable-name').html('Selected route')
    document.getElementById("replaceable-content").scrollTop;
    $('.result-board button').removeClass('blue-button red-button green-button');
    $('#search-board button').removeClass('blue-button red-button green-button');
    for (var hi = 0; hi < problem_holds.length; hi++) {
        document.getElementById(problem_holds[hi]).classList = "led-button blue-button";
    }

    current_holds = problem_holds
    sessionStorage.setItem('hold',JSON.stringify(current_holds))
    getProblemList(problem_holds, current_notholds,  setYear, setAngle, problem_holds.length, minGrade, maxGrade, 3,20,sortedBy,current_holdsetsSelected)
})

$(".holdsetBtn").click(function () {
    console.log('holdsetBtnClick')
    holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson) {
        current_holdsetsSelected = JSON.parse(holdsetsSelectedjson)
    } else {
        current_holdsetsSelected = []
    }
    var $btn = $(this);
    $btn.toggleClass('selected');
    var holdsetSelected = $btn.val();
    if ($btn.hasClass('selected')) {
        current_holdsetsSelected.push(holdsetSelected)
    } else {
        current_holdsetsSelected.remove(holdsetSelected)
    }
    sessionStorage.setItem('holdsetsSelected',JSON.stringify(current_holdsetsSelected))
    holdsetsSelectedjson = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson) {
        current_holdsetsSelected = JSON.parse(holdsetsSelectedjson)
    } else {
        current_holdsetsSelected = []
    }
    var setYear = sessionStorage.getItem('setYear') || '2017';
    var setAngle = sessionStorage.getItem('setAngle') || '40';
    var minGrade = sessionStorage.getItem('minGrade') ||  '5+';
    var maxGrade = sessionStorage.getItem('maxGrade') || '8B+';
    var sortedBy = sessionStorage.getItem('sortedBy') || '';
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
    filtered_current_holds = current_holds.slice(0)
    filtered_current_notholds = current_notholds.slice(0)

    current_holds.forEach( function(hold) {
      if (!current_holdsetsSelected.includes(holdsetmapping[setYear][hold])) {
          filtered_current_holds.splice( filtered_current_holds.indexOf(hold), 1 )
          document.getElementById(hold).classList = "led-button"
      }
    })
    current_notholds.forEach( function(hold) {
      if (!current_holdsetsSelected.includes(holdsetmapping[setYear][hold])) {
          filtered_current_notholds.splice( filtered_current_notholds.indexOf(hold), 1 )
          document.getElementById(hold).classList = "led-button"
      }
    })

    current_holds = filtered_current_holds
    current_notholds = filtered_current_notholds
    sessionStorage.setItem('hold',JSON.stringify(current_holds))
    min_overlap = current_holds.length
    sessionStorage.setItem('min_overlap',min_overlap)
    getProblemList(current_holds, current_notholds,  setYear, setAngle, min_overlap, minGrade, maxGrade, 3,20,sortedBy,current_holdsetsSelected)
});

$(".sortBtn").click(function () {
    console.log('sortBtnClick')

    var $btn = $(this);

    $(".sortBtn").removeClass('selected');

    $btn.addClass('selected');
    var sortedBy = $btn.val();
    var setYear = sessionStorage.getItem('setYear') || '2017';
    var setAngle = sessionStorage.getItem('setAngle') || '40';
    var minGrade = sessionStorage.getItem('minGrade') ||  '5+';
    var maxGrade = sessionStorage.getItem('maxGrade') || '8B+';
    var dsSort = [];
    $("#sortedBy").text("Sorted by: " + sortedBy);
    sessionStorage.setItem('sortedBy', sortedBy);
    current_holdsetsSelected = sessionStorage.getItem('holdsetsSelected')
    if (holdsetsSelectedjson) {
        current_holdsetsSelected = JSON.parse(holdsetsSelectedjson)
    } else {
        current_holdsetsSelected = []
    }
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
    var min_overlap = sessionStorage.getItem('min_overlap',current_holds.length)
    getProblemList(current_holds, current_notholds,  setYear, setAngle, min_overlap, minGrade, maxGrade, 3,20,sortedBy,current_holdsetsSelected)
});
});
document.getElementById("replaceable-content").scrollTop = 0;

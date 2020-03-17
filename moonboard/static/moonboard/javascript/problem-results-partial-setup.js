console.log("ProblemResultsPartial-Javascript Start")
setYear = (typeof setYear === 'undefined') ? '2017' : setYear
setAngle = (typeof setAngle === 'undefined') ? '40' : setAngle
minGrade = (typeof minGrade === 'undefined') ? '5+' : minGrade
maxGrade = (typeof maxGrade === 'undefined') ? '8B+' : maxGrade
minTick = (typeof minTick === 'undefined') ? 1 : minTick
maxTick = (typeof maxTick === 'undefined') ? 17 : maxTick
sortedBy = (typeof sortedBy === 'undefined') ? null : sortedBy
holds = (typeof holds === 'undefined') ? [] : holds
notholds = (typeof notholds === 'undefined') ? [] : notholds
holdRangeMin = (typeof holdRangeMin === 'undefined') ? 4 : holdRangeMin
holdRangeMax = (typeof holdRangeMax === 'undefined') ? 20 : holdRangeMax
min_overlap = (typeof min_overlap === 'undefined') ? 0 : min_overlap
min_overlap_from_slider = (typeof min_overlap_from_slider === 'undefined') ? null : min_overlap_from_slider

if (typeof holdsetsSelected === 'undefined') {
    if (setYear == '2016') {
        holdsetsSelected = ['A','B','school']
    } else if (setYear == '2017') {
        holdsetsSelected = ['A','B','C','wood','school']
    } else if  (setYear == '2019') {
        holdsetsSelected = ['A','B','wood','woodB','woodC','school']
    }
}
console.log(' - setYear = '+setYear)
console.log(' - setAngle = '+setAngle)
console.log(' - holdsetsSelected = '+holdsetsSelected)
console.log(' - holds = '+holds)
console.log(' - notholds = '+notholds)
console.log(' - holdRangeMin = '+holdRangeMin)
console.log(' - holdRangeMax = '+holdRangeMax)


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

var arrayLength = holdsetsSelected.length
for (var i = 0; i < arrayLength; i++) {
    holdset = holdsetsSelected[i]
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
   document.getElementById("replaceable-content").scrollTop
   $('.result-board button').removeClass('blue-button red-button green-button')
   $('#search-board button').removeClass('blue-button red-button green-button')

   holds = []
   notholds = []
   min_overlap = 0
   min_overlap_from_slider = null


   if (setYear == '2016') {
      holdsetsSelected = ['A','B','school']
   } else if (setYear == '2017') {
      holdsetsSelected = ['A','B','C','wood','school']
   } else if  (setYear == '2019') {
      holdsetsSelected = ['A','B','wood','woodB','woodC','school']
   }
   getProblemList(holds=holds, notholds=notholds, setYear, setAngle, null, '5+','8B+',holdRangeMin, holdRangeMax,'',holdssetSelected=holdsetsSelected)

})

$("#resetAll").on("click", function () {
    console.log('Full Reset')
    $('#replaceable-name').html('Selected route')
    document.getElementById("replaceable-content").scrollTop
    $('.result-board button').removeClass('blue-button red-button green-button')
    $('#search-board button').removeClass('blue-button red-button green-button')
    holds = []
    notholds = []
    min_overlap = 0
    min_overlap_from_slider = null
    setYear = '2017'
    setAngle = '40'
    if (setYear == '2016') {
        holdsetsSelected = ['A','B','school']
    } else if (setYear == '2017') {
        holdsetsSelected = ['A','B','C','wood','school']
    } else if  (setYear == '2019') {
        holdsetsSelected = ['A','B','wood','woodB','woodC','school']
    }
    getProblemList(holds=holds, notholds=notholds, setYear, setAngle, null, '5+','8B+', holdRangeMin, holdRangeMax,'',holdssetSelected=holdsetsSelected)
})

holdsetups = JSON.parse('[{"Id":17,"Description":"MoonBoard Masters 2019","AllowClimbMethods":true,"MoonBoardConfigurations":[{"Id":1,"Description":"40° MoonBoard","LowGrade":"6A+","HighGrade":"8B+"},{"Id":2,"Description":"25° MoonBoard","LowGrade":"5+","HighGrade":"8B+"}]},{"Id":15,"Description":"MoonBoard Masters 2017","AllowClimbMethods":true,"MoonBoardConfigurations":[{"Id":1,"Description":"40° MoonBoard","LowGrade":"6A+","HighGrade":"8B+"},{"Id":2,"Description":"25° MoonBoard","LowGrade":"5+","HighGrade":"8B+"}]},{"Id":1,"Description":"MoonBoard 2016","AllowClimbMethods":false,"MoonBoardConfigurations":[]}]')
ticks_labels = ["5","5+","6A","6A+","6B","6B+","6C","6C+","7A","7A+","7B","7B+","7C","7C+","8A","8A+","8B","8B+","8C"]


//Grade Slider
var $sliderMin = $(".grade-slider .noUi-handle-lower")
var $sliderMax = $(".grade-slider .noUi-handle-upper")

function sliderValueChanged(values, handle, unencoded, tap, positions) {
    console.log('gradeSliderValueChanged')
    tMin = ticks_labels[parseInt(values[0])]
    tMax = ticks_labels[parseInt(values[1])]

    if (minGrade != tMin || maxGrade != tMax) {
        minGrade = tMin
        maxGrade = tMax
        minTick = values[0]
        maxTick = values[1]
    }
    if (min_overlap_from_slider == null) {
        min_overlap = holds.length
    } else {
        min_overlap = min_overlap_from_slider
    }
    console.log(holds, notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
    getProblemList(holds, notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
}

function sliderIsSliding(values, handle, unencoded, tap, positions) {
    if ($sliderMin.position().left === $sliderMax.position().left) {
        if (handle == 0) {
            $sliderMax.css("z-index", 4)
        } else {
            $sliderMax.css("z-index", 5)
        }
    }

}

if  ($('#slider').length) {
  moonSlider = document.getElementById('slider')
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
  })
  moonSlider.noUiSlider.on('slide', sliderIsSliding)
  moonSlider.noUiSlider.on('change', sliderValueChanged)
}


function updateSliderTicks() {
    var $nodes = $("#slider .noUi-value-large")
    $nodes.each( function (index, e) {
        if (index % 2 === 0) {
            e.innerHTML = ticks_labels[index]
        } else {
            e.innerHTML = " "
        }
    })
}

updateSliderTicks()



// holdRangeSlider
holdRangeSliderMin = $("#holdRangeSlider .noUi-handle-lower")
holdRangeSliderMax = $("#holdRangeSlider .noUi-handle-upper")

function holdRangeSliderValueChanged(values, handle, unencoded, tap, positions) {
    console.log('holdRangeSliderValueChanged')
    holdRangeMin = parseInt(values[0])
    holdRangeMax = parseInt(values[1])

    if (min_overlap_from_slider == null) {
        min_overlap = holds.length
    } else {
        min_overlap = min_overlap_from_slider
    }
    console.log(holds, notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
    getProblemList(holds, notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
}

function holdRangeSliderIsSliding(values, handle, unencoded, tap, positions) {
    holdRangeSliderMin = $("#holdRangeSlider .noUi-handle-lower")
    holdRangeSliderMax = $("#holdRangeSlider .noUi-handle-upper")

    if (holdRangeSliderMin.position().left === holdRangeSliderMax.position().left) {
        if (handle == 0) {
            holdRangeSliderMax.css("z-index", 4)
        } else {
            holdRangeSliderMax.css("z-index", 5)
        }
    }

}

if  ($('#holdRangeSlider').length) {
  holdRangeSlider = document.getElementById('holdRangeSlider');
  noUiSlider.create(holdRangeSlider, {
     start: [holdRangeMin, holdRangeMax],
     step: 1,
     connect: true,
     range: {
         'min': [4],
         'max': [14]
     },
     pips: {
      mode: 'steps',
      density: 100
  }
  });
  holdRangeSlider.noUiSlider.on('change', holdRangeSliderValueChanged);
  holdRangeSlider.noUiSlider.on('slide', holdRangeSliderIsSliding)
}


// minOverlapSlider

function minOverlapSliderValueChanged(values, handle, unencoded, tap, positions) {
    min_overlap_from_slider = parseInt(values[0])
    min_overlap = min_overlap_from_slider
    console.log(holds,notholds, setYear, setAngle, min_overlap,minGrade,maxGrade,holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
    getProblemList(holds, notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
}

$("button.btnGrade").on("click", function () {
    var $button = $(this)
    $button.toggleClass("unselected")
    var grades = $("button.btnGrade:not('.unselected')")
       .map( function () {
           return this.innerText
       })
       .get()
       .join(",")
})


$("button.tabButton").on("click", function () {
    var $tabButton = $(this)
    $("button.tabButton").removeClass("selected")
    $("div.moon-tab").removeClass("active")
    var id = $tabButton.data("id")
    $tabButton.addClass('selected')
    $('div.moon-tab[data-id="' + id + '"]').addClass('active')
})

selectedIndex = -1


$(function () {
    Array.prototype.remove = function() {
        var what, a = arguments, L = a.length, ax
        while (L && this.length) {
        what = a[--L]
        while ((ax = this.indexOf(what)) !== -1) {
             this.splice(ax, 1)
        }
     }
     return this
}

$("#usetheseholdstosearch").click(function () {
    $('#replaceable-name').html('Selected route')
    document.getElementById("replaceable-content").scrollTop
    $('.result-board button').removeClass('blue-button red-button green-button')
    $('#search-board button').removeClass('blue-button red-button green-button')
    for (var hi = 0; hi < problem_holds.length; hi++) {
        document.getElementById(problem_holds[hi]).classList = "led-button blue-button"
    }
    holds = problem_holds
    getProblemList(problem_holds, notholds,  setYear, setAngle, problem_holds.length, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
})

$(".holdsetBtn").click(function () {
    console.log('holdsetBtnClick')
    var $btn = $(this)
    $btn.toggleClass('selected')
    holdsetSelected = $btn.val()
    if ($btn.hasClass('selected')) {
        holdsetsSelected.push(holdsetSelected)
    } else {
        holdsetsSelected.remove(holdsetSelected)
    }
    filtered_holds = holds.slice(0)
    filtered_notholds = notholds.slice(0)
    holds.forEach( function(hold) {
      if (!holdsetsSelected.includes(holdsetmapping[setYear][hold])) {
          filtered_holds.splice( filtered_holds.indexOf(hold), 1 )
          document.getElementById(hold).classList = "led-button"
      }
    })
    notholds.forEach( function(hold) {
      if (!holdsetsSelected.includes(holdsetmapping[setYear][hold])) {
          filtered_notholds.splice(filtered_notholds.indexOf(hold), 1 )
          document.getElementById(hold).classList = "led-button"
      }
    })
    holds = filtered_holds
    notholds = filtered_notholds
    if (min_overlap_from_slider == null) {
        min_overlap = holds.length
    } else {
        min_overlap = min_overlap_from_slider
    }
    getProblemList(holds, notholds,  setYear, setAngle, min_overlap, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
})

$(".sortBtn").click(function () {
    console.log('sortBtnClick')
    var $btn = $(this)
    $(".sortBtn").removeClass('selected')
    $btn.addClass('selected')
    sortedBy = $btn.val()
    var dsSort = []
    $("#sortedBy").text("Sorted by: " + sortedBy)
    sessionStorage.setItem('sortedBy', sortedBy)
    if (min_overlap_from_slider == null) {
        min_overlap = holds.length
    } else {
        min_overlap = min_overlap_from_slider
    }
    getProblemList(holds, notholds, setYear, setAngle, min_overlap, minGrade, maxGrade, holdRangeMin, holdRangeMax, sortedBy, holdsetsSelected)
})
})
document.getElementById("replaceable-content").scrollTop = 0

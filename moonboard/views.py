from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Case, When

from .models import Problem, ProblemMove
from django.template.loader import render_to_string
from pprint import pprint as pp
from datetime import datetime
import logging
from .holdmappinginclude import holdmapping

logging.basicConfig(level=logging.DEBUG)

def helloView(request):
    return HttpResponse('Hello World!')


def homePageView(request):

    holds = request.GET.getlist('hold[]')
    set_year = request.GET.get('set_year', 2017)
    if holds:
        problems = None
    else:
        problems = None

    if request.is_ajax():
        html = render_to_string(
            template_name="problem-results-partial.html",
            context={"problems": problems, "max_holds": len(holds),"set_year": set_year}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'home.html')

def problemListView(request):
    logging.debug(request.GET.get('min_overlap'))
    set_year = request.GET.get('set_year', '2017')
    defaultHoldsets = {'2016': ['A','B','school'], '2017':['A','B','C','wood','school'], '2019': ['A','B','wood','woodB','woodC','school'] }
    holdsetsSelected = request.GET.getlist('holdsetsSelected[]')
    if not holdsetsSelected:
        holdsetsSelected = defaultHoldsets[set_year]

    holds = request.GET.getlist('hold[]')
    notholds = request.GET.getlist('nothold[]')

    min_grade = request.GET.get('min_grade', '5')
    max_grade = request.GET.get('max_grade', '8C')
    sorted_by = request.GET.get('sortedBy','')
    gradelist = ["5", "5+", "6A", "6A+", "6B", "6B+", "6C", "6C+", "7A", "7A+", "7B", "7B+", "7C", "7C+", "8A", "8A+", "8B", "8B+", "8C"]
    filtered_gradelist =  []
    record=False
    for grade in gradelist:
        if grade == min_grade:
            record=True
            filtered_gradelist.append(grade)

        if grade == max_grade:
            record=False
            if grade != min_grade:
                 filtered_gradelist.append(grade)
        else:
            if record:
                filtered_gradelist.append(grade)

    min_overlap = request.GET.get('min_overlap')
    if not min_overlap:
        min_overlap = len(holds)
    set_year = request.GET.get('set_year', '2017')
    set_angle = request.GET.get('set_angle', '40')

    min_holds = 3
    max_holds = 20

    if len(holds)>0:
        problems = Problem.objects.prefetch_related('problemmove_set')\
        .annotate(hold_count=Count(Case(When(problemmove__position__in=holds, then=1))), total_holds=Count('*'))\
        .annotate(nothold_count=Count(Case(When(problemmove__position__in=notholds, then=1))), total_notholds=Count('*'))\
        .filter(hold_count__gte=min_overlap, setyear=set_year, setangle=set_angle, grade__in=filtered_gradelist)
    else:
        problems = None

    filtered_problems = []
    if problems:
        for problem in problems:
            outsideCurrentHoldset = False
            pholds = problem.problemmove_set.all()
            for h in pholds:
                if holdmapping[set_year][h.position][0] not in holdsetsSelected:
                    outsideCurrentHoldset = True


            if not outsideCurrentHoldset:
                nothold_count = problem.nothold_count
                problem.numholds = len(pholds)

                dateinserted_timestamp = float(problem.dateinserted[6:-2])/1000
                problem.datetimestamp = dateinserted_timestamp
                problem.date = datetime.utcfromtimestamp(dateinserted_timestamp).strftime('%b %Y')

                problem.gradenum = gradelist.index(problem.grade)
                problem.screwons = ['Feet follow hands + screw ons', 'Screw ons only', 'Footless + kickboard','Feet follow hands'].index(problem.method)
                filtered_problems.append(problem)

    else:
        filtered_problems=[]

    if sorted_by != '':
        filtered_problems = filter_problems(sorted_by, filtered_problems)

    min_for_min_overlap_slider = max(3,len(holds)-6)
    html = render_to_string(template_name="problem-results-partial.html",
            context={"problems": filtered_problems, "min_overlap": min_overlap, "max_holds": len(holds),"min_for_min_overlap_slider": min_for_min_overlap_slider, "sortedBy":sorted_by,  "set_year": set_year, "holdsetsSelected": holdsetsSelected}
        )
    data_dict = {"html_from_view": html}

    return JsonResponse(data=data_dict, safe=False)

def filter_problems(by, problems):
    filter_options = {
            'Repeats': {'field_name': 'repeats', 'reverse': True},
            'New': {'field_name': 'dateinserted', 'reverse': True},
            'Method': {'field_name': 'screwons', 'reverse': False},
            'Rating': {'field_name': 'rating', 'reverse': True},
            'Holds': {'field_name': 'numholds', 'reverse': False},
            'Easy': {'field_name': 'gradenum', 'reverse': False},
            }
    return sorted(problems, key=lambda i: getattr(i, filter_options[by]['field_name']), reverse=filter_options[by]['reverse'])


def problemView(request):
    # parameters: holds, grade, overlap, # of holds used
    holds = request.GET.getlist('hold')
    min_grade = request.GET['min_grade']
    max_grade = request.GET['max_grade']


    qs  = ProblemMove.objects.prefetch_related('problem_set')\
        .filter(position__in=holds).distinct()\
        .values('problem_id', 'problem__name').annotate(move_count=Count('*'))\
        .filter(move_count__gte=len(holds))
    ctx = {'problems': qs}
    return render(request, 'problems.html', context=ctx)

    #return Response('Holds:' + request.GET.getlist('hold'))

def problemView(request):

    problem_id = request.GET['problemId']
    problem = Problem.objects.get(id=problem_id)
    holds = problem.problemmove_set.all()
    holdstr = ''
    for hold in holds:
        holdstr = holdstr + hold.position + ', '
    return HttpResponse('Problem fetched ' + problem.name + holdstr)

def problemAsJsonView(request):

    problem_id = request.GET['problemId']
    problem = Problem.objects.get(id=problem_id)
    holds = problem.problemmove_set.values_list('position','isstart','isend')

    problem_dict = {
        'id': problem_id,
        'name': problem.name,
        'grade': problem.grade,
        'method': problem.method,
        'setyear': problem.setyear,
        'holds': holds[::1]
        }

    return JsonResponse(data=problem_dict)

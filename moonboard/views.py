from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Case, When

from .models import Problem, Move
from django.template.loader import render_to_string
from pprint import pprint as pp
import datetime
import logging
from .holdmappinginclude import holdmapping
import string
import numpy as np
from numpy.core.umath_tests import inner1d
from django.views.decorators.cache import never_cache

set_angle_lookup = {'40':1, '25':2, '0':0}
set_year_lookup = {'2020':1,'2019':2,'2017':3,'2016':4}

logging.basicConfig(level=logging.DEBUG)

def convertPositionToCoord(pos):
    col = string.ascii_uppercase.index(pos[:1])*2
    row = int(pos[1:])
    return (col, row)

def HausdorffDist(A,B):
    D_mat = np.sqrt(inner1d(A,A)[np.newaxis].T + inner1d(B,B)-2*(np.dot(A,B.T)))
    # Find DH
    dH = np.max(np.array([np.max(np.min(D_mat,axis=0)),np.max(np.min(D_mat,axis=1))]))
    return(dH)

def ModHausdorffDist(A,B):
    # Find pairwise distance
    D_mat = np.sqrt(inner1d(A,A)[np.newaxis].T + inner1d(B,B)-2*(np.dot(A,B.T)))
    # Calculating the forward HD: mean(min(each col))
    FHD = np.mean(np.min(D_mat,axis=1))
    # Calculating the reverse HD: mean(min(each row))
    RHD = np.mean(np.min(D_mat,axis=0))
    # Calculating mhd
    MHD = np.max(np.array([FHD, RHD]))
    return(MHD, FHD, RHD)

@never_cache
def helloView(request):
    return HttpResponse('Hello World!')

@never_cache
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

@never_cache
def problemListView(request):
    set_year = request.GET.get('set_year', '2017')
    set_angle = request.GET.get('set_angle', '40')
    holds = request.GET.getlist('hold[]')
    notholds = request.GET.getlist('nothold[]')
    min_grade = request.GET.get('min_grade', '5')
    max_grade = request.GET.get('max_grade', '8C')
    holdRangeMin = int(request.GET.get('holdRangeMin', 4))
    holdRangeMax = int(request.GET.get('holdRangeMax', 20))
    sorted_by = request.GET.get('sortedBy','')
    min_overlap = request.GET.get('min_overlap',0)

    defaultHoldsets = {'2016': ['A','B','school'], '2017':['A','B','C','wood','school'], '2019': ['A','B','wood','woodB','woodC','school'] }
    holdsetsSelected = request.GET.getlist('holdsetsSelected[]')
    if not holdsetsSelected:
        holdsetsSelected = defaultHoldsets[set_year]
    if not min_overlap or min_overlap == 0:
        min_overlap = len(holds)
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

    if set_year == '2016':
        set_angle = '0'
    logging.debug(('holds',holds))
    logging.debug(('notholds',notholds))
    logging.debug(('set_year',set_year))
    logging.debug(('set_angle',set_angle))
    logging.debug(('filtered_gradelist',filtered_gradelist))
    logging.debug(('min_overlap',min_overlap))
    logging.debug(('holdRangeMin',holdRangeMin))
    logging.debug(('holdRangeMax',holdRangeMax))

    if len(holds)>0:
        problems = Problem.objects.prefetch_related('move_set')\
        .annotate(hold_count=Count(Case(When(move__description__in=holds, then=1))), total_holds=Count('*'))\
        .annotate(nothold_count=Count(Case(When(move__description__in=notholds, then=1))), total_notholds=Count('*'))\
        .filter(hold_count__gte=min_overlap, setupid=set_year_lookup[set_year], moonboardconfigurationid=set_angle_lookup[set_angle], grade__in=filtered_gradelist)
    else:
        problems = None

    filtered_problems = []
    max_difference  = 0
    if problems:
        for problem in problems:
            logging.debug(('problem',problem))
            outsideCurrentHoldset = False
            pholds = problem.move_set.all()
            for h in pholds:
                if h.description in holdmapping[set_year] and holdmapping[set_year][h.description][0] not in holdsetsSelected:
                    outsideCurrentHoldset = True

            if not outsideCurrentHoldset:
                if len(pholds)>=holdRangeMin and len(pholds)<=holdRangeMax:
                    nothold_count = problem.nothold_count
                    problem.numholds = len(pholds)

                    #dateinserted_timestamp = float(problem.dateinserted[6:-2])/1000
                    dateinserted_timestamp = datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds = problem.dateinserted//10)
                    problem.datetimestamp = dateinserted_timestamp
                    problem.date = dateinserted_timestamp.strftime('%b %Y')

                    problem.gradenum = gradelist.index(problem.grade)
                    problem.screwons = ['Feet follow hands + screw ons', 'Screw ons only', 'Footless + kickboard','Feet follow hands'].index(problem.method)

                    search_holds = np.array([convertPositionToCoord(h) for h in holds])
                    found_problem_holds = np.array([convertPositionToCoord(h.description) for h in pholds])
                    problem.distance, problem.fhd, problem.rhd = ModHausdorffDist(search_holds, found_problem_holds)
                    problem.hd = problem.distance*10
                    problem.fhd = problem.fhd*10
                    problem.rhd = problem.rhd*10
                    if problem.distance > max_difference:
                        max_difference = problem.distance

                    filtered_problems.append(problem)

        for problem in filtered_problems:
            problem.distance = (100 - problem.distance).round()
            problem.newdistance = (float(problem.hold_count)/float(problem.total_holds))*50+(42-problem.hd)*50/42

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
            'Benchmark': {'field_name': 'isbenchmark', 'reverse': True},
            'Repeats': {'field_name': 'repeats', 'reverse': True},
            'New': {'field_name': 'dateinserted', 'reverse': True},
            'Method': {'field_name': 'screwons', 'reverse': False},
            'Rating': {'field_name': 'userrating', 'reverse': True},
            'Similar': {'field_name': 'newdistance', 'reverse': True},
            'Easy': {'field_name': 'gradenum', 'reverse': False},
            }
    return sorted(problems, key=lambda i: getattr(i, filter_options[by]['field_name']), reverse=filter_options[by]['reverse'])


def problemView(request):
    # parameters: holds, grade, overlap, # of holds used
    holds = request.GET.getlist('hold')
    min_grade = request.GET['min_grade']
    max_grade = request.GET['max_grade']


    qs  = Move.objects.prefetch_related('problem_set')\
        .filter(description__in=holds).distinct()\
        .values('problem_id', 'problem__name').annotate(move_count=Count('*'))\
        .filter(move_count__gte=len(holds))
    ctx = {'problems': qs}
    return render(request, 'problems.html', context=ctx)

    #return Response('Holds:' + request.GET.getlist('hold'))

@never_cache
def problemView(request):

    problem_id = request.GET['problemId']
    problem = Problem.objects.get(id=problem_id)
    holds = problem.move_set.all()
    holdstr = ''
    for hold in holds:
        holdstr = holdstr + hold.description + ', '
    return HttpResponse('Problem fetched ' + problem.name + holdstr)

@never_cache
def problemAsJsonView(request):

    problem_id = request.GET['problemId']
    problem = Problem.objects.get(id=problem_id)
    holds = problem.move_set.values_list('description','isstart','isend')

    problem_dict = {
        'id': problem_id,
        'name': problem.name,
        'grade': problem.grade,
        'method': problem.method,
        'isbenchmark': problem.isbenchmark,
        'setyear': problem.setupid,
        'holds': holds[::1]
        }

    return JsonResponse(data=problem_dict)

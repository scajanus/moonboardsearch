from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Case, When

from .models import Problem, ProblemMove
from django.template.loader import render_to_string
from pprint import pprint as pp
from datetime import datetime
import logging
logging.basicConfig(level=logging.ERROR)
def helloView(request):
    return HttpResponse('Hello World!')


def homePageView(request):

    holds = request.GET.getlist('hold[]')
    set_year = request.GET.get('set_year', 2016)
    if holds:
        # problems = ProblemMove.objects.prefetch_related('problem_set')\
        # .filter(position__in=holds).distinct()\
        # .values('problem_id', 'problem__name', 'problem__grade').annotate(move_count=Count('*'))\
        # .filter(move_count__gte=len(holds))
        problems = ProblemMove.objects.prefetch_related('problem_set').distinct().values('problem_id', 'problem__name', 'problem__grade', 'problem__repeats').annotate(hold_count=Count(Case(When(position__in=holds, then=1))), total_holds=Count('*'))\
            .filter(hold_count__gte=len(holds))
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
    holds = request.GET.getlist('hold[]')
    notholds = request.GET.getlist('nothold[]')

    min_grade = request.GET.get('min_grade', '5+')
    max_grade = request.GET.get('max_grade', '8B+')
    sortedBy = request.GET.get('sortedBy','')
    logging.debug((holds,notholds,min_grade,max_grade,sortedBy))
    gradelist = ["5+", "6A", "6A+", "6B", "6B+", "6C", "6C+", "7A", "7A+", "7B", "7B+", "7C", "7C+", "8A", "8A+", "8B", "8B+"]
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


    min_overlap = max(
                    int(request.GET.get('min_overlap', len(holds))), len(holds)-4
                    )
    # For some reason  min_overlap was coming back from  a request as len(holds)+1
    min_overlap = min(min_overlap,len(holds))
    set_year = request.GET.get('set_year', 2017)
    set_angle = request.GET.get('set_angle', 40)
    logging.debug((set_year, set_angle, min_overlap))

    min_holds = 3
    max_holds = 20
    #print(holds)

    logging.debug('holdinfo')
    logging.debug(holds)
    logging.debug(notholds)
    if holds and notholds:
        logging.debug('holds  and notholds')
        logging.debug((holds, notholds,  min_overlap, set_year, set_angle))
        problems = ProblemMove.objects.prefetch_related('problem_set')\
            .distinct()\
            .values('problem_id', 'problem__name', 'problem__grade','problem__repeats','problem__setyear','problem__setangle','problem__rating','problem__dateinserted','problem__method')\
            .annotate(hold_count=Count(Case(When(position__in=holds, then=1))), total_holds=Count('*'))\
            .annotate(nothold_count=Count(Case(When(position__in=notholds, then=1))), total_notholds=Count('*'))\
            .filter(hold_count__gte=min_overlap, nothold_count__lte=0, problem__setyear=set_year, problem__setangle=set_angle)
    elif holds and not notholds:
        logging.debug('holds  and not notholds')
        logging.debug((holds, min_overlap, set_year, set_angle))
        problems = ProblemMove.objects.prefetch_related('problem_set')\
            .distinct()\
            .values('problem_id', 'problem__name', 'problem__grade','problem__repeats','problem__setyear','problem__setangle','problem__rating','problem__dateinserted','problem__method')\
            .annotate(hold_count=Count(Case(When(position__in=holds, then=1))), total_holds=Count('*'))\
            .filter(hold_count__gte=min_overlap, problem__setyear=set_year, problem__setangle=set_angle)
        logging.debug(('len(problems)',len(problems)))
    else:
        logging.debug('none')
        problems = None

    filtered_problems = []
    if problems:
        for problem in problems:
            nothold_count = problem.get('nothold_count',0)
            if problem['problem__grade'] in filtered_gradelist:
                dateinserted_timestamp = float(problem['problem__dateinserted'][6:-2])/1000
                problem['datetimestamp'] = dateinserted_timestamp
                problem['date'] = datetime.utcfromtimestamp(dateinserted_timestamp).strftime('%b %Y')
                problem['problem__gradenum'] = gradelist.index(problem['problem__grade'])
                problem['screwons'] = ['Feet follow hands + screw ons', 'Screw ons only', 'Footless + kickboard','Feet follow hands'].index(problem['problem__method'])
                filtered_problems.append(problem)

    else:
        filtered_problems=[]
    logging.debug(('len(filtered_problems)',len(filtered_problems)))

    if sortedBy == 'Repeats':
        sorted_filtered_problems = sorted(filtered_problems, key = lambda i: i['problem__repeats'], reverse=True)
    elif sortedBy == 'New':
        sorted_filtered_problems = sorted(filtered_problems, key = lambda i: i['datetimestamp'], reverse=True)
    elif sortedBy == 'Screw Ons':
        sorted_filtered_problems = sorted(filtered_problems, key = lambda i: i['screwons'])
    elif sortedBy == 'Rating':
        sorted_filtered_problems = sorted(filtered_problems, key = lambda i: i['problem__rating'], reverse=True)
    elif sortedBy == 'Hard':
        sorted_filtered_problems = sorted(filtered_problems, key = lambda i: i['problem__gradenum'], reverse=True)
    elif sortedBy == 'Easy':
        sorted_filtered_problems = sorted(filtered_problems, key = lambda i: i['problem__gradenum'])
    else:
        sorted_filtered_problems =  filtered_problems

    logging.debug(('min_for_min_overlap_slider',len(holds)-4,max(3,len(holds)-4)))
    min_for_min_overlap_slider = max(3,len(holds)-4)
    html = render_to_string(template_name="problem-results-partial.html",
            context={"problems": sorted_filtered_problems, "min_overlap": min_overlap, "max_holds": len(holds),"min_for_min_overlap_slider": min_for_min_overlap_slider, "sortedBy":sortedBy,  "set_year": set_year}
        )
    data_dict = {"html_from_view": html}

    return JsonResponse(data=data_dict, safe=False)

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
    #import ipdb; ipdb.set_trace()
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

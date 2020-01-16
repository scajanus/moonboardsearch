from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Case, When

from .models import Problem, ProblemMove
from django.template.loader import render_to_string


def helloView(request):
    return HttpResponse('Hello World!')


def homePageView(request):

    holds = request.GET.getlist('hold[]')
    print(holds)

    if holds:
        # problems = ProblemMove.objects.prefetch_related('problem_set')\
        # .filter(position__in=holds).distinct()\
        # .values('problem_id', 'problem__name', 'problem__grade').annotate(move_count=Count('*'))\
        # .filter(move_count__gte=len(holds))
        problems = ProblemMove.objects.prefetch_related('problem_set').distinct().values('problem_id', 'problem__name', 'problem__grade').annotate(hold_count=Count(Case(When(position__in=holds, then=1))), total_holds=Count('*'))\
            .filter(hold_count__gte=len(holds))
    else:
        problems = None

    if request.is_ajax():
        html = render_to_string(
            template_name="problem-results-partial.html",
            context={"problems": problems, "max_holds": len(holds)}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'home.html')

def problemListView(request):
    holds = request.GET.getlist('hold[]')
    min_grade = request.GET.get('minGrade', '6A+')
    max_grade = request.GET.get('maxGrade', '8C+')
    min_overlap = max(int(request.GET.get('minOverlap', len(holds))), len(holds)-3)
    setyear = request.GET.get('setYear', 2016)
    min_holds = 3
    max_holds = 20
    print(holds)

    if holds:
        problems = ProblemMove.objects.prefetch_related('problem_set')\
            .distinct()\
            .values('problem_id', 'problem__name', 'problem__grade','problem__setyear')\
            .annotate(hold_count=Count(Case(When(position__in=holds, then=1))), total_holds=Count('*'))\
            .filter(hold_count__gte=min_overlap, problem__setyear=setyear)
    else:
        problems = None

    html = render_to_string(template_name="problem-results-partial.html",
            context={"problems": problems, "max_holds": len(holds)}
        )
    data_dict = {"html_from_view": html}

    return JsonResponse(data=data_dict, safe=False)

def problemView(request):
    # parameters: holds, grade, overlap, # of holds used
    holds = request.GET.getlist('hold')
    min_grade = request.GET['mingrade']
    max_grade = request.GET['maxgrade']
    print(min_grade)

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
        'holds': holds[::1]
        }

    return JsonResponse(data=problem_dict)

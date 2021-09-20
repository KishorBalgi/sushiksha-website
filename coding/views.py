from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from djangoProject.settings import HCK_SECRET_KEY
import requests, json, os

COMPILE_URL = "https://api.hackerearth.com/v3/code/compile/"
RUN_URL = "https://api.hackerearth.com/v3/code/run/"

CLIENT_SECRET = HCK_SECRET_KEY

headers = {
    'client-secret': CLIENT_SECRET,
    'content-type': 'application/json',
}

permitted_languages = ["C", "CPP", "CSHARP", "GO", "JAVA", "JAVASCRIPT", "PHP",
                       "PYTHON", "PYTHON3", "R", "RUBY"]

"""
Check if source given with the request is empty
"""


def source_empty_check(source):
    if source == "":
        response = {
            "message": "Source can't be empty!",
        }
        return JsonResponse(response, safe=False)


"""
Check if lang given with the request is valid one or not
"""


def lang_valid_check(lang):
    if lang not in permitted_languages:
        response = {
            "message": "Invalid language - not supported!",
        }
        return JsonResponse(response, safe=False)


"""
Handle case when at least one of the keys (lang or source) is absent
"""


def missing_argument_error():
    response = {
        "message": "ArgumentMissingError: insufficient arguments for compilation!",
    }
    return JsonResponse(response, safe=False)


"""
View catering to /ide/ URL,
simply renders the index.html template
"""


def index(request):
    return render(request, 'coding/index.html', {})


"""
Method catering to AJAX call at /ide/compile/ endpoint,
makes call at HackerEarth's /compile/ endpoint and returns the compile result as a JsonResponse object
"""


def compileCode(request):
    if request.is_ajax():
        try:
            source = request.POST['source']
            # Handle Empty Source Case
            source_empty_check(source)

            lang = request.POST['lang']
            # Handle Invalid Language Case
            lang_valid_check(lang)

        except KeyError:
            # Handle case when at least one of the keys (lang or source) is absent
            missing_argument_error()

        else:
            compile_data = {
                'client_secret': CLIENT_SECRET,
                'async': 0,
                'source': source,
                'lang': lang,
            }

            r = requests.post(COMPILE_URL, data=compile_data)
            return JsonResponse(r.json(), safe=False)

    else:
        return HttpResponseForbidden()


"""
Method catering to AJAX call at /ide/run/ endpoint,
makes call at HackerEarth's /run/ endpoint and returns the run result as a JsonResponse object
"""


def runCode(request):
    if request.is_ajax():
        try:
            source = request.POST['source']
            # Handle Empty Source Case
            source_empty_check(source)

            lang = request.POST['lang']
            # Handle Invalid Language Case
            lang_valid_check(lang)

        except KeyError:
            # Handle case when at least one of the keys (lang or source) is absent
            missing_argument_error()

        else:
            # default value of 5 sec, if not set
            time_limit = request.POST.get('time_limit', 5)
            # default value of 262144KB (256MB), if not set
            memory_limit = request.POST.get('memory_limit', 262144)

            run_data = {
                'client_secret': CLIENT_SECRET,
                'async': 0,
                'source': source,
                'lang': lang,
                'time_limit': time_limit,
                'memory_limit': memory_limit,
            }

            # if input is present in the request
            code_input = ""
            if 'input' in request.POST:
                run_data['input'] = request.POST['input']
                code_input = run_data['input']

            """
      Make call to /run/ endpoint of HackerEarth API
      and save code and result in database
      """
            r = requests.post(RUN_URL, data=run_data)
            r = r.json()
            # cs = ""
            # rss = ""
            # rst = ""
            # rsm = ""
            # rso = ""
            # rsstdr = ""
            # try:
            #     cs = r['compile_status']
            # except:
            #     pass
            # try:
            #     rss = r['run_status']['status']
            # except:
            #     pass
            # try:
            #     rst = r['run_status']['time_used']
            # except:
            #     pass
            # try:
            #     rsm = r['run_status']['memory_used']
            # except:
            #     pass
            # try:
            #     rso = r['run_status']['output_html']
            # except:
            #     pass
            # try:
            #     rsstdr = r['run_status']['stderr']
            # except:
            #     pass

            # code_response = codes.objects.create(
            #     code_id=r['code_id'],
            #     code_content=source,
            #     lang=lang,
            #     code_input=code_input,
            #     compile_status=cs,
            #     run_status_status=rss,
            #     run_status_time=rst,
            #     run_status_memory=rsm,
            #     run_status_output=rso,
            #     run_status_stderr=rsstdr
            # )
            # code_response.save()
            return JsonResponse(r, safe=False)
    else:
        return HttpResponseForbidden()

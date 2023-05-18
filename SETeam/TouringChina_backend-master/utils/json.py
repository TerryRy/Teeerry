from django.http import JsonResponse


def response(data):
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def greetings(request):
    result = {"message": "Weclome to Course Management Service"}
    return JsonResponse(result)
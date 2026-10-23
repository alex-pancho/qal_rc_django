from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")
# Create your views here.

def about(request):
    return render(request, "base.html", {
        "title": "Про себе",
    })
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import Template, Context



def inicio (req):
    return render(req, "inicio.html")
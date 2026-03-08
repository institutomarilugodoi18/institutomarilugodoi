from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def lista_animais(request):
    return HttpResponse("Animais OK ✅ (área interna)")
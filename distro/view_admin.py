# -*- coding: utf-8 -*-
'''
Created on 23/02/2014

@author: Carlos Rijo Palma & António Urbano Baião
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import Group, User

# index do administrador
@login_required
def index(request, *args, **kwargs):
    template = "administrador/index.html"

    return render_to_response(template,
        locals(),
        context_instance=RequestContext(request),
        )

# Adicionar Grupo de utilizadores
#def addGrupo(request, *args, **kwargs):
    
    


# Lista de Grupos de utilizadores
@login_required
def listGroup(request):
    print "aaaaaaaaaaa"
    template = "administrador/Groups/listGroup.html"
    
    listGroup = Group.objects.all()

    return render_to_response(template,
        locals(),
        context_instance=RequestContext(request),
        )
    
# Lista de utilizadores
@login_required
def listUser(request):
    print "aaaaaaaaaaa"
    template = "administrador/Users/listUsers.html"
    
    listUser = User.objects.all()

    return render_to_response(template,
        locals(),
        context_instance=RequestContext(request),
        )    
    
    
    
    
    
    
    
    
    
    
    
    
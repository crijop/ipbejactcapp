# -*- coding: utf-8 -*-
'''
Created on 23/02/2014

@author: Carlos Rijo Palma & António Urbano Baião
'''
from distro.Forms.form_admin import AddUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
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



# Adicionar Utilizadores de utilizadores
def addUsers(request, *args, **kwargs):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            tableuser = User(username = form.cleaned_data['username'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        email = form.cleaned_data['email'],
                        password = form.cleaned_data['password1'],
                        )
            
            tableuser.set_password(form.cleaned_data['password1'])
               
            tableuser.save()
            
            
            
            
            
            #===================================================================
            # msg = ugettext('Password changed successfully.')
            # messages.success(request, msg)
            # return HttpResponseRedirect('..')
            #===================================================================
    else:
        form = AddUserForm()
    
    template = "administrador/Users/addUser.html"
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
    
    
    
    
    
    
    
    
    
    
    
    
# -*- coding: utf-8 -*-
'''
Created on 08/03/2014

@author: Carlos Rijo Palma & António Urbano Baião
'''
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from distro.Forms.form_admin import PasswordChangeForm, EditUser_com_login_Form


# Alterar a password de utilizador
@login_required(redirect_field_name = 'login_redirectUsers')
def password_changeUser(request, *args, **kwargs):
    idUser = request.user.id
    userEdit = User.objects.get(id = idUser)
    nomeUser = userEdit.username
    
    grupoUser = request.user.groups.all()
    
    nomeGrupo = grupoUser[0].name
    print nomeGrupo
    
    if nomeGrupo == "RecusosHumanos":
        extentTemplate = "recursosHumanos/index.html"
    elif nomeGrupo == "Cientifico":
        extentTemplate = "cientifico_new/index.html"
    elif nomeGrupo == "Departamento" or nomeGrupo == "Eng":
        extentTemplate = "departamento/index.html"
    elif nomeGrupo == "Docente":
        extentTemplate = "docentes/index.html"
    elif nomeGrupo == "Administrador":
        extentTemplate = "administrador/index.html"
    elif nomeGrupo == "vicP":
        extentTemplate = "cientifico/index.html"
    
    
    
    password_change_form = PasswordChangeForm
    if request.method == "POST":
        form = PasswordChangeForm(user = userEdit, data = request.POST)
        if form.is_valid():
            form.save()
            template = "utilizadores/sucessoAlterPass.html"
            return render_to_response(template,
                locals(),
                context_instance = RequestContext(request),
                )
        
    else:
        form = PasswordChangeForm(user = request.user.id)
        template = "utilizadores/alterarPassword.html"
        
        return render_to_response(template,
            locals(),
            context_instance = RequestContext(request),
            )


# Editar dados do utilizador
@login_required(redirect_field_name = 'login_redirectUsers')
def editUser(request, *args, **kwargs):
    #===========================================================================
    idUser = request.user.id
    userEdit = User.objects.get(id = idUser)
    nomeUser = userEdit.username
    print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAa", userEdit.email
    grupoUser = request.user.groups.all()
     
    nomeGrupo = grupoUser[0].name
    print nomeGrupo
     
    if nomeGrupo == "RecusosHumanos":
        extentTemplate = "recursosHumanos/index.html"
    elif nomeGrupo == "Cientifico":
        extentTemplate = "cientifico_new/index.html"
    elif nomeGrupo == "Departamento" or nomeGrupo == "Eng":
        extentTemplate = "departamento/index.html"
    elif nomeGrupo == "Docente":
        extentTemplate = "docentes/index.html"
    elif nomeGrupo == "Administrador":
        extentTemplate = "administrador/index.html"
    elif nomeGrupo == "vicP":
        extentTemplate = "cientifico/index.html"
    
    
    #===========================================================================
    # varTipoTemplate = "Edit"
    # #idUser = kwargs["idUser"]
    # userEdit = User.objects.get(id = idUser)
    # 
    #===========================================================================
    
    if request.method == 'POST':
        form = EditUser_com_login_Form(userEdit.username, userEdit.email,  request.POST, instance = userEdit)
        
        if form.is_valid():
            User.objects.filter(id = idUser).update(username = form.cleaned_data['username'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        email = form.cleaned_data['email'],
                        )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = EditUser_com_login_Form(userEdit.username, userEdit.email, instance = userEdit)
    
    
    template = "utilizadores/editPerfil.html"
    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )
    
    #===========================================================================
    # password_change_form = PasswordChangeForm
    #===========================================================================
    #if request.method == "POST":
        #=======================================================================
        # form = PasswordChangeForm(user = userEdit, data = request.POST)
        # if form.is_valid():
        #     form.save()
        #     template = "utilizadores/sucessoAlterPass.html"
        #     return render_to_response(template,
        #         locals(),
        #         context_instance = RequestContext(request),
        #         )
        #=======================================================================
        
    #else:
        #=======================================================================
        # form = PasswordChangeForm(user = request.user.id)
        # template = "utilizadores/alterarPassword.html"
        #=======================================================================
        
        

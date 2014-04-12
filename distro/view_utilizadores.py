'''
Created on 08/03/2014

@author: admin1
'''
from distro.Forms.form_admin import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext


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
        extentTemplate = "cientifico/index.html"
    elif nomeGrupo == "Departamento" or nomeGrupo == "Eng":
        extentTemplate = "departamento/index.html"
    elif nomeGrupo == "Docente":
        extentTemplate = "docentes/index.html"
    elif nomeGrupo == "Administrador":
        extentTemplate = "administrador/index.html"
    
    
    print extentTemplate
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

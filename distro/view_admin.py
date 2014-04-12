# -*- coding: utf-8 -*-
'''
Created on 23/02/2014

@author: Carlos Rijo Palma & António Urbano Baião
'''
from distro.Forms.form_admin import AddUserForm, AddGroupForm, EditUserForm, \
    PasswordChangeForm, PasswordChangeFormReset
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User, Permission
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.response import TemplateResponse
from django.utils.translation import ugettext, ugettext_lazy as _
# index do administrador
@login_required
def index(request, *args, **kwargs):
    template = "administrador/index.html"

    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )

# Adicionar Grupo de utilizadores
# def addGrupo(request, *args, **kwargs):
    
    


# Lista de Grupos de utilizadores
@login_required
def listGroup(request):
    print "aaaaaaaaaaa"
    template = "administrador/Groups/listGroup.html"
    
    listGroup = Group.objects.all()

    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )
    
    
# Cria o grupo na tabela Group
@login_required(redirect_field_name = 'login_redirectUsers') 
def addGroup(request, *args, **kwargs):
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
           
        if form.is_valid():
            nomeGroup = form.cleaned_data['name']
            tablegroup = Group(name = nomeGroup,
                        )
               
            tablegroup.save()       
            
            # Relaciona as permissoes com o grupo       
            for p in form.cleaned_data['perm']:
                # relaciona a permissao ao grupo
                g = Permission.objects.get(name = p.name)
                 
                # get last id inserted
                last_id = Group.objects.latest('id')
                # atualiza na db
                g.group_set.add(last_id)   
                        
    else:
        form = AddGroupForm()
    return render_to_response("administrador/Groups/addGroup.html",
        locals(),
        context_instance = RequestContext(request),
        )
     
    pass



# Adicionar Utilizadores de utilizadores
def addUsers(request, *args, **kwargs):
    varTipoTemplate = "Add"
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            tableuser = User(username = form.cleaned_data['username'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        email = form.cleaned_data['email'],
                        password = form.cleaned_data['password1'],
                        is_active = form.cleaned_data['is_active'],
                        )
            tableuser.set_password(form.cleaned_data['password1'])
            tableuser.save()
            
            
            # Verificar o se o grupo vem a null
            print "aswwww", form.cleaned_data['group']
            if form.cleaned_data['group'] != None:
            
                nomeGrupo = form.cleaned_data['group']
                g = Group.objects.get(name = nomeGrupo)
                users = User.objects.filter(username = form.cleaned_data['username'])
                for u in users:
                    g.user_set.add(u)
            
            
            
    else:
        form = AddUserForm()
    
    template = "administrador/Users/add_edit_User.html"
    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )
    
# Adicionar Utilizadores de utilizadores
def editUser(request, *args, **kwargs):
    varTipoTemplate = "Edit"
    idUser = kwargs["idUser"]
    userEdit = User.objects.get(id = idUser)
    if request.method == 'POST':
        form = EditUserForm(userEdit.username, request.POST, instance = userEdit)
        
        if form.is_valid():
            User.objects.filter(id = idUser).update(username = form.cleaned_data['username'],
                        first_name = form.cleaned_data['first_name'],
                        last_name = form.cleaned_data['last_name'],
                        email = form.cleaned_data['email'],
                        is_active = form.cleaned_data['is_active'],
                            )
            
            return HttpResponseRedirect(reverse('listUser'))
    else:
        form = EditUserForm(userEdit.username, instance = userEdit)
    
    template = "administrador/Users/add_edit_User.html"
    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )    

    
    
# Fazer reset a password por parte do administrador
def password_changeReset(request, *args, **kwargs):
    idUser = kwargs["idUser"]
    userEdit = User.objects.get(id = idUser)
    nomeUser = userEdit.username
    
    password_change_form = PasswordChangeFormReset
    if request.method == "POST":
        form = password_change_form(user = userEdit, data = request.POST)
        if form.is_valid():
            form.save()
    else:
        form = password_change_form(user = userEdit)
        
    template = "administrador/Users/changePassword.html"
    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )
    

# Lista de utilizadores
@login_required
def listUser(request):
    print "aaaaaaaaaaa"
    template = "administrador/Users/listUsers.html"
    
    listUser = User.objects.all()

    return render_to_response(template,
        locals(),
        context_instance = RequestContext(request),
        )    
    
    
    
    
    
    
    
    
    
    
    
    

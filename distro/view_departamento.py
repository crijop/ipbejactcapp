'''
Created on 10 de Out de 2012

@author: admin1
'''
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.template.context import RequestContext

'''
Inicio das vistas do Departamento
''' 
@login_required(redirect_field_name='login_redirectUsers')
@user_passes_test(lambda u:u.groups.filter(name='Departamento').count())
def indexDepartamento(request):
    return render_to_response("departamento/index.html",
        locals(),
        context_instance=RequestContext(request),
        )


'''
Fim das vistas do Departamento
''' 

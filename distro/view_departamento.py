'''
Created on 10 de Out de 2012

@author: admin1
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

'''
Inicio das vistas do Departamento
''' 
@login_required(redirect_field_name='Teste_home')
def indexDepartamento(request):
    return render_to_response("departamento/index.html",
        locals(),
        context_instance=RequestContext(request),
        )


'''
Fim das vistas do Departamento
''' 

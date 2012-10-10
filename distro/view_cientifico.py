# -*- coding: utf-8 -*-

'''
Created on 21 de Set de 2012

@author: admin1
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

'''
Inicio das vistas do Ciêntifico
'''

@login_required(redirect_field_name='login_redirectUsers')
def indexCientifico(request):
    return render_to_response("cientifico/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

'''
Fim das vistas do Ciêntifico
'''
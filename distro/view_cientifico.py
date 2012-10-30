# -*- coding: utf-8 -*-

'''
Created on 21 de Set de 2012

@author: admin1
'''
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.template.context import RequestContext



'''
Inicio das vistas do Ciêntifico
'''
cientificoUserTeste = user_passes_test(lambda u:u.groups.filter(name='Cientifico').count(), login_url='')



@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def indexCientifico(request):
    return render_to_response("cientifico/index.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

@login_required(redirect_field_name='login_redirectUsers')
@cientificoUserTeste
def criarXLS(request):
    return render_to_response("cientifico/criar_xls.html",
        locals(),
        context_instance=RequestContext(request),
        )
    pass

'''
Fim das vistas do Ciêntifico
'''
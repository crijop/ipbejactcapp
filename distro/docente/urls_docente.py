# -*- coding: utf-8 -*-
'''
Created on 03/06/2014

@author: Carlos Rijo Palma
@email: carlosrijopalma@hotmail.com
'''

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    ########################################################################################
    # Url's destinados aos templates dos docentes
    ####                   
    # Url Home Docente
    url(r'^$',
        'ipbejactcapp.distro.docente.view_docente.indexDocente',
        name = 'homeDocente'),
    
    # Url Turmas a que os docentes pertence
    url(r'^distro/docente/turmas',
        'ipbejactcapp.distro.docente.view_docente.turmasDocentes',
        name = 'turmasDocentes'),
                    
    # Url horas de serviço distinada a cada docente
    url(r'^distro/docente/horasServico',
        'ipbejactcapp.distro.docente.view_docente.horasServico',
        name = 'horasServico'),
    #####
    # Fim dos Url's destinados aos templates dos docentes
    ########################################################################################
    
    
    ########################################################################################
    # Url's destinados aos pdf's dos docentes
    ####                   
    # Url Home Docente
    url(r'^distro/docente/genpdf/$',
        'ipbejactcapp.distro.docente.pdf_rml_views.generate_pdf',
        name = 'print_pdf'),
    #####
    # Fim dos Url's destinados aos pdf's dos docentes
    ########################################################################################
    
    )
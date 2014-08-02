# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: Carlos Rijo Palma
@email: carlosrijopalma@hotmail.com
@author: António Urbano Baião
@email: baiao@sapo.pt
'''

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    ########################################################################################
    # Url's destinados as estatisticas do VICE PRESIDENCIA
    #####
    url(r'^$',
        'ipbejactcapp.distro.estatistica.vicP.modulo_estatistico.index_estatisticas',
        name = 'index_estatisticas'),
    
    
    url(r'^tipo_estatistica/$',
        'ipbejactcapp.distro.estatistica.vicP.modulo_estatistico.tipo_estatistica',
        name = 'tipo_estatistica'),
                    
    url(r'^tipo_estatistica/tipo_docente/$',
        'ipbejactcapp.distro.estatistica.vicP.modulo_estatistico.tipo_docente',
        name = 'tipo_docente_option'),
    
    url(r'^tipo_estatistica/tipo_docente/docente_hora/$',
        'ipbejactcapp.distro.estatistica.vicP.modulo_estatistico.docente_hora',
        name = 'docente_hora'),
    
    url(r'^tipo_estatistica/tipo_docente/search_data/$',
        'ipbejactcapp.distro.estatistica.vicP.modulo_estatistico.search_data',
        name = 'search_data'),
    
    #===========================================================================
    # # Url Turmas a que os docentes pertence
    # url(r'^distro/docente/turmas',
    #     'ipbejactcapp.distro.docente.view_docente.turmasDocentes',
    #     name = 'turmasDocentes'),
    #===========================================================================
    
    #####
    # Fim dos Url's destinados as estatisticas do VICE PRESIDENCIA
    ########################################################################################
    )
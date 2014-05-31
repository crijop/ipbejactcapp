# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
      
    # Url Home vicP
    url(r'^distro/vicp/$',
        'ipbejactcapp.distro.views.indexVicP',
        name = 'HomeVicP'),
    
    # Url Criar XLS                   
    url(r'^distro/vicp/criarXLS$',
        'ipbejactcapp.distro.view_cientifico.criarXLS',
        name = 'criarXLS'),
                       
     # Url listar modulos                  
    url(r'^distro/vicp/listaDelegados$',
        'ipbejactcapp.distro.view_cientifico.listaDelegacoes',
        name = 'modulosDelegados'),
                       
      url(r'^distro/vicp/listaDelegados/aprovarDelegados/(?P<id_modulo>\d+)$',
        'ipbejactcapp.distro.view_cientifico.aprovarDelegacao',
        name = 'aprovarModulo'),
                       
     url(r'^distro/vicp/listaDelegados/reprovarDelegados/(?P<id_modulo>\d+)$',
        'ipbejactcapp.distro.view_cientifico.reprovarDelegacao',
        name = 'reprovarModulo'),
                       
    #######################
    # Nova etapa do trabalho
    # Data: 14/05/2013
    #######################
    
    #######################Definir Cursos#########################
    url(r'^distro/vicp/cet$',
        'ipbejactcapp.distro.view_cientifico.definirCursosCET',
        name = 'def_Curso_CET'),
                    
    url(r'^distro/vicp/lic$',
        'ipbejactcapp.distro.view_cientifico.definirCursosLic',
        name = 'def_Curso_Lic'),
    
    url(r'^distro/vicp/mest$',
        'ipbejactcapp.distro.view_cientifico.definirCursosMest',
        name = 'def_Curso_Mest'),
                       
   url(r'^distro/vicp/pg$',
        'ipbejactcapp.distro.view_cientifico.definirCursosPG',
        name = 'def_Curso_PG'),
                       
   url(r'^distro/vicp/portle$',
        'ipbejactcapp.distro.view_cientifico.definirCursosPortLE',
        name = 'def_Curso_PortLE'),
   ###############################################################
   
   #######################Adicionar Cursos########################
   url(r'^distro/vicp/addCurso/(?P<id_CET>\d+)/$',
        'ipbejactcapp.distro.view_cientifico.addCursoFormClass',
        name = 'addCursosCET'),
   ###############################################################
   
   #######################Listar Cursos###########################
   url(r'^distro/vicp/listar_cet$',
        'ipbejactcapp.distro.view_cientifico.listarCursosCET',
        name = 'listar_Curso_CET'),
                    
    url(r'^distro/vicp/listar_lic$',
        'ipbejactcapp.distro.view_cientifico.listarCursosLic',
        name = 'listar_Curso_Lic'),
    
    url(r'^distro/vicp/listar_mest$',
        'ipbejactcapp.distro.view_cientifico.listarCursosMest',
        name = 'listar_Curso_Mest'),
                       
   url(r'^distro/vicp/listar_pg$',
        'ipbejactcapp.distro.view_cientifico.listarCursosPG',
        name = 'listar_Curso_PG'),
                       
   url(r'^distro/vicp/listar_portle$',
        'ipbejactcapp.distro.view_cientifico.listarCursosPortLE',
        name = 'listar_Curso_PortLE'),
   ###############################################################
   
   #######################Listar Cursos###########################
   url(r'^distro/vicp/listar_cet/(?P<id_curso>\d+)/$',
        'ipbejactcapp.distro.view_cientifico.verCurso',
        name = 'ver_curso'),
   ##################Definir novo ano###############
       url(r'^distro/vicp/wizard_cna/$',
        'ipbejactcapp.distro.view_cientifico.wizard_cna',
        name = 'wizard_cna'),
                       
   url(r'^distro/vicp/wizard_new_department/$',
    'ipbejactcapp.distro.view_cientifico.wizard_cna_novo_departamento',
    name = 'wizard_cna_n_d'),
                       
    url(r'^distro/vicp/wizard_new_course/$',
        'ipbejactcapp.distro.view_cientifico.wizard_cna_novo_curso',
        name = 'wizard_cna_n_c'),


    url(r'^distro/vicp/ajax_abrir_lista_departamentos/$',
        'ipbejactcapp.distro.view_cientifico.ajax_abrir_lista_departamentos'),

    
    # save departamentos
    url(r'^distro/vicp/ajax_save_lista_departamentos/$',
        'ipbejactcapp.distro.view_cientifico.ajax_save_lista_departamentos', \
        name = "ajax_save_lista_departamentos"),
    
    
)



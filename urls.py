# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ipbejactcapp.views.home', name='home'),
    # url(r'^ipbejactcapp/', include('ipbejactcapp.foo.urls')),

    url(r'^criarturmas/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.views.criar_turmas', 
        name='criar_turmas'),
    url(r'^apagarturmas/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.views.apagar_turmas', 
        name='apagar_turmas'),
    url(r'^criarservico/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.views.criar_servico', 
        name='criar_servico'),
    url(r'^apagarservico/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.views.apagar_servico', 
        name='apagar_servico'),
    url(r'^dispmeta/$', 
        'ipbejactcapp.distro.views.display_meta', 
        name='display_meta'),
    # BEGIN TESTES
    url(r'^search-form/$', 
        'ipbejactcapp.distro.views.search_form', 
        name='search_form'),
    url(r'^search/$', 
        'ipbejactcapp.distro.views.search', 
        name='search'),
                       
    # END TESTES
    # grapelli
    #(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
    #URL LOGIN
    (r'^$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, 'entrar'),
                       
    #URL para a pagina Sair, encaminhando para a pagina de login do sistema
    #(r'^$', 'django.contrib.auth.views.logout',
    #    {'template_name': 'login.html'}, 'sair'),

                    
    #URL para a pagina Home
    url(r'^distro/$', 
        'ipbejactcapp.distro.views.login_redirectUsers', 
        name='home'),
    
    #URL para a pagina Sair
    (r'^distro/sair$', 'django.contrib.auth.views.logout',
        {'template_name': 'sair.html'}, 'sair'),
                       
    
    #ACTORES DO SISTEMA                   
    
    #####
    # Url's destinados aos templates do cientifico
    ####
    #Url Home Ciêntifico
    url(r'^distro/cientifico/$', 
        'ipbejactcapp.distro.views.indexCientifico', 
        name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates do cientifico
    ####
    
    
    #####
    # Url's destinados aos templates do coordenadores de Cursos
    ####
    #Url Home coordenadores de Cursos
    #url(r'^distro/coordCursos/$', 
    #    'ipbejactcapp.distro.views.indexCoordCursos', 
    #    name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates do coordenadores de Cursos
    ####
    
  
    #####
    # Url's destinados aos templates do departamento
    #### 
    #Url Home Departamento
    url(r'^distro/departamento/$', 
        'ipbejactcapp.distro.views.indexDepartamento', 
        name='homeDepartamento'),
                       
    url(r'^distro/departamento/listarTurmas/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.view_departamento.listarTurmasDepart', 
        name='listarTurmas'),                   
                       
    url(r'^distro/departamento/listDocentes/$', 'ipbejactcapp.distro.view_departamento.listDocentes',
        name='listDocentesDep'),
                       
    url(r'^distro/departamento/listDocentes/filter_abc/$', 'ipbejactcapp.distro.view_departamento.filter_abcd'),
                       
    url(r'^distro/departamento/listDocentes/filter_cat/$', 'ipbejactcapp.distro.view_departamento.filter_cat'),
                       
    url(r'^distro/departamento/listDocentes/(?P<id_docente>\d+)/$', 'ipbejactcapp.distro.view_departamento.infoDocenteDep'),        

    #turmas sem serviço docente atribuido
    #template de adicionar docente ao serviço docente
    url(r'^distro/departamento/turmaSemSevicoDocente/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.view_departamento.addServicoDocenteDepart', 
        name='turmaSemServDocente'),
    
    #Url adicionar o docente ao serviço docente
    #mais propriamente para aparecer o formulario.                    
    url(r'^distro/departamento/turmaSemSevicoDocente/addServicoDocente/(?P<id_servico>\d+)/(?P<id_Departamento>\d+)/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.view_departamento.viewFormClass', 
        name='addServicoDocentDepart'),
    
    #Aparece o butão para salvar o formulario quando
    #existe alguma alteração.
    url(r'^distro/departamento/turmaSemSevicoDocente/addServicoDocente/(?P<id_servico>\d+)/(?P<id_Departamento>\d+)/(?P<ano>\d+)/addSaveButton$',
          'ipbejactcapp.distro.view_departamento.showSaveButton'), 
                       
    #Filtro por ordem alfabetica                   
    url(r'^distro/departamento/turmaSemSevicoDocente/(?P<ano>\d+)/filter_abc/$', 'ipbejactcapp.distro.view_departamento.filter_abc'),
    
    #Filtro por curso                  
    url(r'^distro/departamento/turmaSemSevicoDocente/(?P<ano>\d+)/filter_curso/$', 'ipbejactcapp.distro.view_departamento.filter_curso'),
    
    ##TURMAS#########################################################################################################
     url(r'^distro/departamento/listarTurmas/(?P<ano>\d+)/filter_abc/$', 
        'ipbejactcapp.distro.view_departamento.filter_abc'), 
     url(r'^distro/departamento/listarTurmas/(?P<ano>\d+)/filter_curso/$', 
        'ipbejactcapp.distro.view_departamento.filter_curso'),
                       
     ##Lista serviços Docente#########################################################################################################
      url(r'^distro/departamento/listServicoDocente/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.view_departamento.listServicoDocente', 
        name='listarServicoDocente'),
    
    #Filtro por ordem alfabetica                   
    url(r'^distro/departamento/listServicoDocente/(?P<ano>\d+)/filter_abc/$', 'ipbejactcapp.distro.view_departamento.filter_abc'),
    
    #Filtro por curso                  
    url(r'^distro/departamento/listServicoDocente/(?P<ano>\d+)/filter_curso/$', 'ipbejactcapp.distro.view_departamento.filter_curso'),                   
                      
                       
    url(r'^distro/departamento/listServicoDocente/infoModuloDocente/(?P<id_docente>\d+)/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.view_departamento.infoModulosDocente', 
        name='infoModuloDocente'),
                       
    url(r'^distro/departamento/listServicoDocente/infoModuloTurma/(?P<id_servico>\d+)/(?P<ano>\d+)/$', 
        'ipbejactcapp.distro.view_departamento.infoModulosTurma', 
        name='infoModuloTurma'),                   
                        

           
    
    #####
    #Fim Url's destinados aos templates do departamento
    #### 
  
    
    
    #####
    # Url's destinados aos templates dos Directores de Escola
    ####
    #Url Home Directores de Escola
    url(r'^distro/directoresEscola/$', 
        'ipbejactcapp.distro.views.indexDirectoresEscola', 
        name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates dos Directores de Escola
    ####
    
    
    #####
    # Url's destinados aos templates dos docentes
    ####                   
    #Url Home Docente
    url(r'^distro/docente/$', 
        'ipbejactcapp.distro.views.indexDocente', 
        name='homeDocente'),
    
    #Url Turmas a que os docentes pertence
    url(r'^distro/docente/turmas', 
        'ipbejactcapp.distro.views.turmasDocentes', 
        name='turmasDocentes'),
                    
    #Url horas de serviço distinada a cada docente
    url(r'^distro/docente/horasServico', 
        'ipbejactcapp.distro.views.horasServico', 
        name='horasServico'),
    #####
    #Fim dos Url's destinados aos templates dos docentes
    ####
    
    
    #####
    # Url's destinados aos templates dos Recursos Humanos
    ####
    #Url Home Recursos Humanos
    url(r'^distro/recursosHumanos/$', 
        'ipbejactcapp.distro.views.indexRecursosHumanos', 
        name='homeRecursosHumanos'),
         
    url(r'^distro/recursosHumanos/listDocente/(?P<id_docente>\d+)/$', 
        'ipbejactcapp.distro.view_recursos_humanos.indexRHInfoDocentes', 
        name='infoRHDocentes'),

    
    url(r'^distro/recursosHumanos/listDocenteEdit/$', 
        'ipbejactcapp.distro.view_recursos_humanos.listDocenteEdit_RecursosHumanos', 
        name='listDocenteEdit'),
                       
    #url(r'^distro/recursosHumanos/listDocente/edit/(?P<id_docente>\d+)/$', 
    #    'ipbejactcapp.distro.view_recursos_humanos.indexRH_EditarDocente', 
    #    name='RH_EditarDocente'),
                    
    #url(r'^distro/recursosHumanos/addDocente/$', 
    #    'ipbejactcapp.distro.view_recursos_humanos.addDocenteRH', 
    #    name='adicionarDocenteRH'),
     
    
    url(r'^distro/recursosHumanos/addDocente/$',
        'ipbejactcapp.distro.view_recursos_humanos.addDocenteFormClass',
        name='adicionarDocenteRH'),
    
    url(r'^distro/recursosHumanos/addDocente/addSaveButton/$', 'ipbejactcapp.distro.view_recursos_humanos.showSaveButton1'),
                       
    url(r'^distro/recursosHumanos/listDocenteEdit/(?P<id_docente>\d+)/$',
        'ipbejactcapp.distro.view_recursos_humanos.editDocenteFormClass',
        name='RH_EditarDocente'),
    
                       
    url(r'^distro/recursosHumanos/listDocente/$', 
        'ipbejactcapp.distro.view_recursos_humanos.listDocente_RecursosHumanos', 
        name='listDocente'),
        
    url(r'^distro/recursosHumanos/listContratos/$', 
        'ipbejactcapp.distro.view_recursos_humanos.listContracts_RecursosHumanos', 
        name='listContratos'),                   
    
    url(r'^distro/recursosHumanos/ajuda/(?P<nr_video>\d+)$', 
        'ipbejactcapp.distro.view_recursos_humanos.ajudaRH', 
        name='ajudaRH'),
                       
    #(r'^distro/recursosHumanos/teste$', DocenteModelFormPreview(AddDocenteForm)),            
      
                       
    # lista a editar
    url(r'^distro/recursosHumanos/listDocenteEdit/filter_abc/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_abc'),       
    
    url(r'^distro/recursosHumanos/listDocenteEdit/filter_dep/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_dep'),
    
    url(r'^distro/recursosHumanos/listDocenteEdit/filter_cat/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_cat'),
    
    url(r'^distro/recursosHumanos/listDocenteEdit/(?P<id_docente>\d+)/addSaveButton/$', 'ipbejactcapp.distro.view_recursos_humanos.showSaveButton'),
    #lista de docentes                   
    url(r'^distro/recursosHumanos/ajax/$', 'ipbejactcapp.distro.view_recursos_humanos.ajax'),  
    
    url(r'^distro/recursosHumanos/listDocente/filter_abc/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_abc'),       
    
    url(r'^distro/recursosHumanos/listDocente/filter_dep/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_dep'),
    
    url(r'^distro/recursosHumanos/listDocente/filter_cat/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_cat'),
    
    #lista de contractos
    url(r'^distro/recursosHumanos/listContratos/filter_abc/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_abc'),       
    
    url(r'^distro/recursosHumanos/listContratos/filter_dep/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_dep'),
    
    url(r'^distro/recursosHumanos/listContratos/filter_cat/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_cat'),
    
    url(r'^distro/recursosHumanos/listContratos/(?P<id_docente>\d+)/$', 
        'ipbejactcapp.distro.view_recursos_humanos.indexRHInfoDocentesContratos', 
        name='infoRHDocentesContracto'),
    
    
    #por data
    
  

    url(r'^distro/recursosHumanos/listContratos/filter_date_start/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_date_start'),
    #####
    #Fim dos Url's destinados aos templates dos Recursos Humanos
    ####
    
    
    #####
    # Url's destinados aos templates do serviço de Planeamento
    ####
    #Url Home do serviço de Planeamento
    url(r'^distro/servicoPlaneamento/$', 
        'ipbejactcapp.distro.views.indexServicoPlaneamento', 
        name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates do serviço de Planeamento
    ####
    
)



# -*- coding: utf-8 -*-
from distro.forms import EditarDocenteForm, AdicionarDocenteForm
from distro.view_recursos_humanos import EditDocenteModelFormPreview, AddDocenteModelFormPreview
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
    url(r'^Teste_home/$', 
        'ipbejactcapp.distro.views.Teste_home', 
        name='home'),
    
    #URL para a pagina Sair
    (r'^Teste_home/sair$', 'django.contrib.auth.views.logout',
        {'template_name': 'sair.html'}, 'sair'),
                       
    
    #ACTORES DO SISTEMA                   
    
    #####
    # Url's destinados aos templates do cientifico
    ####
    #Url Home Ciêntifico
    url(r'^Teste_home/cientifico/$', 
        'ipbejactcapp.distro.views.indexCientifico', 
        name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates do cientifico
    ####
    
    
    #####
    # Url's destinados aos templates do coordenadores de Cursos
    ####
    #Url Home coordenadores de Cursos
    #url(r'^Teste_home/coordCursos/$', 
    #    'ipbejactcapp.distro.views.indexCoordCursos', 
    #    name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates do coordenadores de Cursos
    ####
    
    
    #####
    # Url's destinados aos templates do departamento
    #### 
    #Url Home Departamento
    url(r'^Teste_home/departamento/$', 
        'ipbejactcapp.distro.views.indexDepartamento', 
        name='homeDepartamento'),
    
    #####
    #Fim Url's destinados aos templates do departamento
    #### 
    
    
    #####
    # Url's destinados aos templates dos Directores de Escola
    ####
    #Url Home Directores de Escola
    url(r'^Teste_home/directoresEscola/$', 
        'ipbejactcapp.distro.views.indexDirectoresEscola', 
        name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates dos Directores de Escola
    ####
    
    
    #####
    # Url's destinados aos templates dos docentes
    ####                   
    #Url Home Docente
    url(r'^Teste_home/docente/$', 
        'ipbejactcapp.distro.views.indexDocente', 
        name='homeDocente'),
    
    #Url Turmas a que os docentes pertence
    url(r'^Teste_home/docente/turmas', 
        'ipbejactcapp.distro.views.turmasDocentes', 
        name='turmasDocentes'),
                    
    #Url horas de serviço distinada a cada docente
    url(r'^Teste_home/docente/horasServico', 
        'ipbejactcapp.distro.views.horasServico', 
        name='horasServico'),
    #####
    #Fim dos Url's destinados aos templates dos docentes
    ####
    
    
    #####
    # Url's destinados aos templates dos Recursos Humanos
    ####
    #Url Home Recursos Humanos
    url(r'^Teste_home/recursosHumanos/$', 
        'ipbejactcapp.distro.views.indexRecursosHumanos', 
        name='homeRecursosHumanos'),
         
    url(r'^Teste_home/recursosHumanos/listDocente/(?P<id_docente>\d+)/$', 
        'ipbejactcapp.distro.view_recursos_humanos.indexRHInfoDocentes', 
        name='infoRHDocentes'),
    
    
    url(r'^Teste_home/recursosHumanos/listDocenteEdit/$', 
        'ipbejactcapp.distro.view_recursos_humanos.listDocenteEdit_RecursosHumanos', 
        name='listDocenteEdit'),
                       
    #url(r'^Teste_home/recursosHumanos/listDocente/edit/(?P<id_docente>\d+)/$', 
    #    'ipbejactcapp.distro.view_recursos_humanos.indexRH_EditarDocente', 
    #    name='RH_EditarDocente'),
                    
    #url(r'^Teste_home/recursosHumanos/addDocente/$', 
    #    'ipbejactcapp.distro.view_recursos_humanos.addDocenteRH', 
    #    name='adicionarDocenteRH'),
     
    
    url(r'^Teste_home/recursosHumanos/addDocente/$', 
        AddDocenteModelFormPreview(AdicionarDocenteForm), 
        name='adicionarDocenteRH'),
                       
    url(r'^Teste_home/recursosHumanos/listDocenteEdit/(?P<id_docente>\d+)/$', 
        EditDocenteModelFormPreview(EditarDocenteForm), 
        name='RH_EditarDocente'),
    
                       
    url(r'^Teste_home/recursosHumanos/listDocente/$', 
        'ipbejactcapp.distro.view_recursos_humanos.listDocente_RecursosHumanos', 
        name='listDocente'),
        
    url(r'^Teste_home/recursosHumanos/listContratos/$', 
        'ipbejactcapp.distro.view_recursos_humanos.listContracts_RecursosHumanos', 
        name='listContratos'),                   
    
    url(r'^Teste_home/recursosHumanos/ajuda/(?P<nr_video>\d+)$', 
        'ipbejactcapp.distro.view_recursos_humanos.ajudaRH', 
        name='ajudaRH'),
                       
    #(r'^Teste_home/recursosHumanos/teste$', DocenteModelFormPreview(AddDocenteForm)),            
      
                       
    # lista a editar
    url(r'^Teste_home/recursosHumanos/listDocenteEdit/filter_abc/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_abc'),       
    
    url(r'^Teste_home/recursosHumanos/listDocenteEdit/filter_dep/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_dep'),
    
    url(r'^Teste_home/recursosHumanos/listDocenteEdit/filter_cat/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_cat'),
    
    url(r'^Teste_home/recursosHumanos/listDocenteEdit/(?P<id_docente>\d+)/addSaveButton/$', 'ipbejactcapp.distro.view_recursos_humanos.showSaveButton'),
    #lista de docentes                   
    url(r'^Teste_home/recursosHumanos/ajax/$', 'ipbejactcapp.distro.view_recursos_humanos.ajax'),  
    
    url(r'^Teste_home/recursosHumanos/listDocente/filter_abc/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_abc'),       
    
    url(r'^Teste_home/recursosHumanos/listDocente/filter_dep/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_dep'),
    
    url(r'^Teste_home/recursosHumanos/listDocente/filter_cat/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_cat'),
    
    #lista de contractos
    url(r'^Teste_home/recursosHumanos/listContratos/filter_abc/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_abc'),       
    
    url(r'^Teste_home/recursosHumanos/listContratos/filter_dep/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_dep'),
    
    url(r'^Teste_home/recursosHumanos/listContratos/filter_cat/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_cat'),
    
    url(r'^Teste_home/recursosHumanos/listContratos/(?P<id_docente>\d+)/$', 
        'ipbejactcapp.distro.view_recursos_humanos.indexRHInfoDocentes', 
        name='infoRHDocentes'),
    
    #por data
    
  

    url(r'^Teste_home/recursosHumanos/listContratos/filter_date_start/$', 'ipbejactcapp.distro.view_recursos_humanos.filter_date_start'),
    #####
    #Fim dos Url's destinados aos templates dos Recursos Humanos
    ####
    
    
    #####
    # Url's destinados aos templates do serviço de Planeamento
    ####
    #Url Home do serviço de Planeamento
    url(r'^Teste_home/servicoPlaneamento/$', 
        'ipbejactcapp.distro.views.indexServicoPlaneamento', 
        name='homeDirectoresEscola'),
    
    #####
    #Fim dos Url's destinados aos templates do serviço de Planeamento
    ####
    
)

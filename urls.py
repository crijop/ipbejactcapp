# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
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
                       
    #Url Home Docente
    url(r'^Teste_home/docente', 
        'ipbejactcapp.distro.views.indexDocente', 
        name='home'),

    #Url Home Departamento
    url(r'^Teste_home/departamento', 
        'ipbejactcapp.distro.views.indexDepartamento', 
        name='home'),
)

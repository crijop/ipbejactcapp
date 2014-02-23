# -*- coding: utf-8 -*-

'''
Created on 23/02/2014

@author: Carlos Rijo Palma & António Urbano Baião
'''

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',        
    # Index
    url(r'^$', 'distro.view_admin.index', 
            name='HomeAdmin'),
    
    ######################## 23/02/2014 ####################################
    # Url's destinados aos Grupos de utilizadores
    ####
    
    # Lista de grupos
    url(r'^lstgroup/$', 'distro.view_admin.listGroup', 
            name='listGroup'),
    
    #####
    #Fim dos Url's destinados aos Grupos de utilizadores
    ########################################################################################
    
    
    ######################## 23/02/2014 ####################################
    # Url's destinados aos utilizadores
    ####
    
    # Lista de utilizadores
    url(r'^lstuser/$', 'distro.view_admin.listUser', 
            name='listUser'),
    
    #####
    #Fim dos Url's destinados utilizadores
    ########################################################################################
    
    )
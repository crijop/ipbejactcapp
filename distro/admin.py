# -* - coding: utf-8 -*-
from django.contrib import admin

# importação dos modelos
from distro.models import Categoria
from distro.models import UnidadeOrganica
from distro.models import Departamento
from distro.models import TipoContrato
from distro.models import TipoCurso
from distro.models import Curso
from distro.models import Cnaef
from distro.models import Epoca
from distro.models import UnidadeCurricular

admin.site.register(Categoria)
admin.site.register(UnidadeOrganica)
admin.site.register(Departamento)
admin.site.register(TipoCurso)
admin.site.register(Curso)
admin.site.register(TipoContrato)
admin.site.register(Cnaef)
admin.site.register(Epoca)
admin.site.register(UnidadeCurricular)

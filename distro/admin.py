# -* - coding: utf-8 -*-
from django.contrib import admin

# importação dos modelos
from distro.models import Categoria
from distro.models import UnidadeOrganica
from distro.models import Departamento
from distro.models import TipoContrato
from distro.models import TipoCurso
from distro.models import Curso


admin.site.register(Categoria)
admin.site.register(UnidadeOrganica)
admin.site.register(Departamento)
admin.site.register(TipoCurso)
admin.site.register(Curso)
admin.site.register(TipoContrato)

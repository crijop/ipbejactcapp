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
from distro.models import Reducao
from distro.models import Titulo
from distro.models import Docente
from distro.models import CursoDocente

admin.site.register(Categoria)
admin.site.register(UnidadeOrganica)
admin.site.register(Departamento)
admin.site.register(TipoCurso)

class CursoAdmin(admin.ModelAdmin):
    list_filter = ('tipo_curso', )
    pass
admin.site.register(Curso, CursoAdmin)

admin.site.register(TipoContrato)
admin.site.register(Cnaef)
admin.site.register(Epoca)

class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'departamento')
    list_filter = ('curso', 'departamento')

    pass

admin.site.register(UnidadeCurricular, UnidadeCurricularAdmin)

admin.site.register(Reducao)
admin.site.register(Titulo)

class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'departamento')
    list_filter = ('departamento', 
                   'categoria', 
                   'tipo_contrato')

    pass
admin.site.register(Docente, DocenteAdmin)

class CursoDocenteAdmin(admin.ModelAdmin):
    list_filter = ('titulo', 'cnaef',)
    pass

admin.site.register(CursoDocente, CursoDocenteAdmin)


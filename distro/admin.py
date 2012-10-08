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
from distro.models import Turma
from distro.models import ServicoDocente
from distro.models import TipoAula
from distro.models import Contrato
from distro.models import ReducaoServicoDocente

admin.site.register(Categoria)

class UnidadeOrganicaAdmin(admin.ModelAdmin):
    list_display = ('abreviatura', 'nome')
    pass

admin.site.register(UnidadeOrganica, UnidadeOrganicaAdmin)

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
    list_filter = ('curso', 'departamento', 'semestre', 'regente')
    search_fields = ['nome', 'regente__nome_completo']

    pass

admin.site.register(UnidadeCurricular, UnidadeCurricularAdmin)

admin.site.register(Reducao)
admin.site.register(Titulo)

class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'departamento')
    list_filter = ('departamento', )
    search_fields = ['nome_completo']

    pass

admin.site.register(Docente, DocenteAdmin)

class CursoDocenteAdmin(admin.ModelAdmin):
    list_filter = ('titulo', 'cnaef',)
    pass

admin.site.register(CursoDocente, CursoDocenteAdmin)

admin.site.register(TipoAula)

class TurmaAdmin(admin.ModelAdmin):
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "curso":
    #         kwargs["queryset"] = UnidadeCurricular.objects.filter(nome=request.curso)
    #         return super(MyModelAdmin, self).formfield_for_foreignkey(db_field,request, **kwargs)
    #     pass
    list_display = ('unidade_curricular', 'tipo_aula', 'turno', 
                    'ano',)
    list_filter = ('ano', 
                   'unidade_curricular__departamento',
                   'unidade_curricular__curso',
                   'tipo_aula', 
                   'turno', 
                   )
    search_fields = ['unidade_curricular__nome']

    raw_id_admin = ('unidadecurricular', )
    pass


admin.site.register(Turma, TurmaAdmin)

class ServicoDocenteAdmin(admin.ModelAdmin):
    list_filter = ('turma__ano', 
                   'turma__unidade_curricular__departamento',
                   'turma__unidade_curricular__curso',
                   'docente', 
                   )
    search_fields = ['docente__nome_completo', 
                     'turma__unidade_curricular__nome']
    raw_id_admin = ('turma', )
    
    pass

admin.site.register(ServicoDocente,ServicoDocenteAdmin)


class ReducaoServicoDocenteAdmin(admin.ModelAdmin):
    list_filter = ('reducao', )
    search_fields = ['docente__nome_completo',]
    list_display = ('docente', 'reducao',)
    pass

admin.site.register(ReducaoServicoDocente,ReducaoServicoDocenteAdmin)

class ContratoAdmin(admin.ModelAdmin):
    search_fields = ['docente__nome_completo', ]
    list_display = ('docente', 'categoria')

    list_filter = ('categoria', 'tipo_contrato',  )
    pass

admin.site.register(Contrato, ContratoAdmin)

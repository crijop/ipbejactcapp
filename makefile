all: 

migration:
	python manage.py schemamigration distro --auto

migrate:
	python manage.py migrate distro

# carregamento de dados iniciais
initial:
	python manage.py loaddata categorias.yaml
	python manage.py loaddata unidadesorganicas.yaml
	python manage.py loaddata departamentos.yaml
	python manage.py loaddata tiposcursos.yaml
	python manage.py loaddata cursos.yaml
	python manage.py loaddata cnaef.yaml
	python manage.py loaddata epocas.yaml
	python manage.py loaddata unidadecurricular.yaml
	python manage.py loaddata reducoes.yaml
	python manage.py loaddata titulos.yaml
	python manage.py loaddata tiposcontrato.yaml
	python manage.py loaddata docentes.yaml
	python manage.py loaddata tipo_aulas.yaml

zero:
	python manage.py schemamigration distro --initial
	python manage.py migrate distro

clean:
	rm ipbeja.sqlite3
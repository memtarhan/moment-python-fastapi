install_db_packages:
	pip install asyncpg psycopg2 psycopg2-binary sqlalchemy

install_config:
	pip install python-decouple

install_database:
	pip install databases

install_alembic:
	pip install alembic

install_jwt:
	pip install pyjwt

install_password_hash:
	pip install passlib

init_alembic:
	alembic init migrations

migrate:
	alembic revision --autogenerate
	alembic upgrade head

pip_install_requirements:
	pip install -r requirements.txt

pip_uninstall_requirements:
	pip uninstall -r requirements.txt

pip_freeze_requirements:
	pip freeze > requirements.txt

pip_install_only_used_requirements:
	pip freeze | grep -v -f requirements.txt - | grep -v '^#' | xargs pip uninstall -y


deploy_heroku_development:
	pip freeze > requirements.txt
	git add .
	git commit -am "<deploy>: v23>"
	git push heroku HEAD:master


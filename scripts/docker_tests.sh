#!/bin/bash

EXCLUDE='*/migrations/*.py,*/__init__.py,*/adapter.py,*/apps.py,*/cron.py,*/permissions.py,*/validators.py,*/tests/*.py,*/admin.py,*/parsing.py,wsgi.py,manage.py,*/utils/*.py,*/settings/*.py'

rm -rf htmlcov/
docker exec -it django_api coverage run --omit=$EXCLUDE --source='.' manage.py test authentication.tests --nocapture

docker exec -it django_api coverage html
docker cp django_api:/opt/proj/api/htmlcov ./htmlcov
docker exec -it django_api coverage erase

cd redis-6.2.6
make
src/redis-server redis.conf &
cd ..
python3 manage.py makemigrations
python3 manage.py migrate
celery -A ai_bodhitree worker --loglevel=debug --pool=solo &
python3 manage.py runserver 0.0.0.0:8000 &

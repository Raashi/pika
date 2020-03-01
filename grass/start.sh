# launch flower
flower -A main --port=5555 &

# launch startups
python -u startup.py

# launch beat worker
celery -A main beat &

# launch workers
celery -A main worker --loglevel=info &
# exit if something fail
#set -e

# launch flower
flower -A main --port=5555 &
echo FLOWER STARTED

# launch beat worker
#celery -A main beat --loglevel=info --pidfile= &
#echo BEAT WORKER STARTED

# launch workers
celery -A main worker --loglevel=info --pidfile= &
echo WORKER STARTED

# launch startups
sleep 2
python -u main.py startup

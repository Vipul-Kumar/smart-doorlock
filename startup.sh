#!/bin/bash
echo "Killing process working on port 8091 "
sudo fuser -k 8091/tcp


sleep 1s
echo "Starting web cam stream "
sudo service motion start


sleep 1s
echo "Restarting nginx server "
sudo service nginx restart


sleep 3s
echo "Activating virtual environment "
source /home/pi/doorlock-python/.env/bin/activate

echo "Starting Gunicorn app "
sleep 1s
GUNICORN_CMD_ARGS="--bind=127.0.0.1:8091 --workers=1" gunicorn  --chdir /home/pi/doorlock-python app:app &





kill -9 $(pgrep -f device_status_update.py)
cd /home/iot/background_server/viyellatex/viyellatex
nohup python3 device_status_update.py>device_status_update.out &

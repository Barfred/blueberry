ssh pi@192.168.88.238 '
sudo killall python3
ps -ef | grep sandbox.py
cd /home/pi/blueberry
. virtual_env/bin/activate
PYTHONPATH=./bluesound ./blueberry.py &
tail -f /var/log/blueberry.log
'

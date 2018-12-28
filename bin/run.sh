ssh pi@192.168.88.238 '
cd /home/pi/blueberry
. virtual_env/bin/activate
PYTHONPATH=./bluesound ./sandbox.py
'

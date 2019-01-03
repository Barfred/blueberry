ssh pi@192.168.88.238 '
cd /home/pi/blueberry
rm -rf virtual_env
python3 -m venv --system-site-packages virtual_env
. virtual_env/bin/activate
pip install -r requirements.txt
'

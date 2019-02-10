ssh pi@192.168.88.238 '
sudo systemctl stop blueberry
ps -ef | grep blueberry.py
sudo systemctl start blueberry
'

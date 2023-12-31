sleep 20  # Warten Sie 20 Sekunden, um sicherzustellen, dass MariaDB bereit ist

source /home/tom/.venv/bin/activate

python3 /home/tom/projekt/importrequests.py > /home/tom/projekt/importrequests.log 2>&1

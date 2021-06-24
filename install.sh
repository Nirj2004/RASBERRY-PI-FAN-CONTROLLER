#! /bin/sh

set -e 

cd "$(dirname "$0")/.."

echo "=> Installing fan controller...\n"
sudo cp fancontol.py /usr/local/bin/
sudo chmod +x /usr/local/bin/fancontroller.py

echo "=> Starting fan controller...\n"
sudo cp fancontrol.sh /usr/local/bin/
sudo chmod +x /etc/init.d/fancontrol.sh

sudo update-rc.d fancontrol.sh defaults
sudo /etc/init.d/fancontrol.sh start 

echo "Fan controller installed."
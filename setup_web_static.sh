#!/usr/bin/env bash
# script to set up clean server
if ! command -v nginx &> /dev/null; then
	sudo apt-get update
	sudo apt-get install -y nginx
fi
	sudo mkdir /data/web_static/releases/
	sudo mkdir /data/web_static/shared/
	sudo mkdir /data/web_static/releases/test/
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    Universal Translation Service
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '/ult_static/ {s@^.*$@        alias /data/web_static/current/;@}' /etc/nginx/sites-available/default
sudo service nginx restart

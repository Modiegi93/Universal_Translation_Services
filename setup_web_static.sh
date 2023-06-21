#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

sudo echo "Testing Nginx configuration" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

location="location /ult_static/ {\n\talias /data/web_static/current/;\n}\n"
sudo sed -i "37i $location" /etc/nginx/sites-enabled/default

sudo service nginx restart

exit 0

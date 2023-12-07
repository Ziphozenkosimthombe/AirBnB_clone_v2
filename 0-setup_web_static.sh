#!/usr/bin/env bash
# prepare server  for deployment of static version of AirBnB clone

sudo mkdir -p "/data"
sudo mkdir -p "/data/web_static"
sudo mkdir -p "/data/web_static/releases"
sudo mkdir -p "/data/web_static/shared"
sudo mkdir -p "/data/web_static/releases/test"

echo '
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>AirBnB clone</title>
	</head>
    <body style="margin:0px;padding:0px;">
		<header style="background-color:#FF0000;height:70px;width:100%;">
		</header>

		<footer style="position:fixed;bottom:0;background-color:#00FF00;height:60px;width:100%;text-align:center;line-height:30px;">
			<p>Holberton School</p>
		</footer>
	</body>
</html>
' | sudo tee "/data/web_static/releases/test/index.html"

# Define paths
# link_path="/data/web_static/current"
# target_path="/data/web_static/releases/test"

# Check if the symbolic link already exists
if [ -L "$link_path" ]; then
    # If it exists, delete it
    sudo rm "$link_path"
fi

# Create the symbolic link
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo echo "
server {
    listen 80;
    server_name _;

    location / {
        add_header X-Served-By 226796-web-01;
        add_header Content-Type text/plain;
        return 200 'Hello World!\n';
    }
    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
}
" | sudo tee '/etc/nginx/sites-available/default'

sudo service nginx restart
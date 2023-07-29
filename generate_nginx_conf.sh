#!/bin/bash

# Fetch the public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Generate the Nginx configuration
cat <<EOF > /etc/nginx/sites-available/indiedrive
server {
    listen 80;
    server_name $PUBLIC_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/indie-drive;
    }
    
    location /media/ {
        root /home/ubuntu/indie-drive/media;    
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

# Enable the file by linking to the sites-enabled dir
sudo ln -s /etc/nginx/sites-available/indiedrive /etc/nginx/sites-enabled

# Restart Nginx to apply the new configuration
sudo service nginx restart

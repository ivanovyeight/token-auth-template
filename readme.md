- mv example.setup.sh setup.sh && nano setup.sh
- . setup.sh

# Gunicorn config [gunicorn.py]
- command="~/projects/token-auth-template/venv/bin/gunicorn"
- pythonpath="~/projects/token-auth-template/config"
- bind="0.0.0.0:8000"
- workers="3"

# Nginx config
sudo nano /etc/nginx/sites-available/token-auth-template

    server {
        listen 80;
        server_name tokenauth.ivanovyeight.club www.tokenauth.ivanovyeight.club;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static {
            alias /home/vm/projects/token-auth-template/static;
        }

        location / {
            include proxy_params;
            proxy_pass http://0.0.0.0:8000;
        }
    }

- cd /etc/nginx/sites-enabled
- sudo ln -s /etc/nginx/sites-available/token-auth-template
- sudo systemctl restart nginx
# Run gunicorn in background
gunicorn --daemon --config gunicorn.py config.wsgi
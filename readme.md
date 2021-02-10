- sudo apt update
- sudo apt install python3-venv
- sudo apt install nginx

- cd ~/projects/token-auth-template
- python3 -m venv venv
- . venv/bin/activate
- pip install -r requirements.txt
- mv example.env.sh && nano env.sh [set smtp settings]
- python manage.py migrate
- python manage.py collectstatic

# Gunicorn config [gunicorn.py]
- command="~/projects/token-auth-template/venv/bin/gunicorn"
- pythonpath="~/projects/token-auth-template/config"
- bind="0.0.0.0:8000"
- workers="3"

# Nginx config
sudo nano /etc/nginx/sites-available/token-auth-template

    server {
        listen 80;
        server_name 168.62.180.202;

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

# Run gunicorn in background
gunicorn --daemon --config gunicorn.py config.wsgi
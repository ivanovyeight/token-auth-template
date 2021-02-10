sudo apt update
sudo apt install python3-venv
sudo apt install nginx

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

export EMAIL_HOST=""
export EMAIL_HOST_USER=""
export EMAIL_HOST_PASSWORD=""
export DEFAULT_FROM_EMAIL=""
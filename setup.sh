sudo apt update
sudo apt install python3-venv
sudo apt install nginx

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

export EMAIL_HOST="smtp.mail.yahoo.com"
export EMAIL_HOST_USER="ivanovymail23@yahoo.com"
export EMAIL_HOST_PASSWORD="znaxkrqkusyafnwc"
export DEFAULT_FROM_EMAIL="ivanovymail23@yahoo.com"

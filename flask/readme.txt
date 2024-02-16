python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 api.py
pip freeze > requirements.txt
gunicorn -w 4 'api:app'
gunicorn --config gunicorn_config.py 'api:app'

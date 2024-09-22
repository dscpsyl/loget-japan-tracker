# loget-japan-tracker
A tracker website for LoGet tourist cards from Japan.

# To Create

- Download the repository
- `python3 -m venv .venv`
- `pip install -r requirements.txt`
- Go into `settings.py` and change the `SECRET_KEY` to a new secret key
- Create postgres db and make it into a service and update the database settings 
- `cd logettracker && python manage.py makemigrations && python manage.py migrate`
- `python manage.py createsuperuser`
- `cd ../logetscraper && python main.py`
- ` cd ../logettracker && python manage.py runserver`
web: gunicorn -w 4 app:app
heroku ps:scale web=1
# Go to the directory where you place bot.py, Dockerfile
heroku login -i

# Make sure docker is running
heroku container:login
heroku container:push --app <HEROKU_APP_NAME> web
heroku container:release --app <HEROKU_APP_NAME> web

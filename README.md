### Run the python flask app locally with gunicorn
```
 docker compose up
```

How to run the database migrations in your compose container
Hello!

In the last video we ran our app and database using Docker Compose.

But our database will be empty because we haven't ran the flask db upgrade command, which creates our tables.

To run the command, you should:

- First run the compose file with 
```
docker compose up -d
```

- Then run the database upgrade command with
```
 docker compose exec web flask db upgrade
```

### Next is how to run this automatically when starting the container


## Connecting to your Docker Compose database with a database client






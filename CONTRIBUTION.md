Connecting to your Docker Compose database with a database client
Hello!

If you are using Docker Compose and you want to connect to the database using a database client such as DBeaver, here's how to do it. It's straightforward!


Open the port in your docker-compose.yml file
First, in your db service, add the following two lines:

    ports:
      - "5432:5432"
This will make it so accessing port 5432 in your local machine will access port 5432 in your db container.



Re-create the image
Then, re-create the db image with:

docker compose up --build --force-recreate --no-deps db


Connect with the database client
Finally, using your database client, create a new connection to the following URL:

postgresql://postgres:postgres@localhost:5432/myapp
Note the details used are:

Database user: postgres

Database password: postgres

Database host: localhost

Database port: 5432 (this is the port in your local machine)

Database name: myapp



If you have used different details, adjust the URL accordingly.

That's it! Now you'll have a connection with a database client to your Docker Compose database!
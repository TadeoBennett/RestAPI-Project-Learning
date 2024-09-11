### run flask api on local machine
```
flask run
```

### reading a txt file that with libraries to install ( done for flask_jwt_extended)
```
pip install -r requirements.txt
```

### setup python project in virtual environment
```
python -m venv .venv
```

### re-build docker image from Dockerfile(don't forget the last dot)[CREATES NEW IMAGE]
```
docker build -t <custom_image_name> .
```
### then start a container using volumes


### start up a container specifying an image and the ports to use[CREATES A NEW CONTAINER USING THE EXISTING IMAGE]
```
docker run -d  -p 5000:5000 <custom_image_name>
```

### start up an existing container
```
docker start <container_name_or_id>
```

### rebuild container from Dockerfile(done due to config changes)[CREATES A NEW, REBUILT CONTAINER USING THE IMAGE IT WAS ORIGINALLY BUILT FROM]
```
docker run -dp 5005:5000 <container_name>
```

### Using the docker-compose.yml file, run the containers specified
```
docker compose up
```
### Bring down the container specified in the .yml file
```
docker compose down
```

------------------------

### startup a container that maps its workdir with local files(volumes) so updates are automatic[CREATES A NEW CONTAINER USING THE EXISTING IMAGE]
```
docker run -dp 5005:5000  -w /app -v "$(pwd):/app" <custom_image_name>
```
### for running the Dockerfile locally
```
docker run -dp 5005:5000  -w /app -v "$(pwd):/app" <custom_image_name> sh -c "flask run"
```
### the above code runs "flask run" instead of the "CMD" line in the DockerFile


### Recreate the container, reinstalling the requirements
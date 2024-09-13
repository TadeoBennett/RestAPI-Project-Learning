

----------------------------------------------
## RUNNING THE REDIS BACKGROUND WORKER AND APPLICATION LOCALLY IN DOCKER 

*You will need to have migrated and upgraded the database*

### build the application [CREATES AN IMAGE]
```
docker run -p 5000:80 <custom-image-name> .
```


### run the redis background worker(an image needs to have already been created) [CREATES A CONTAINER USING THE EXISTING IMAGE FOR THE REDIS BG WORKER]
```
docker run -w /app <custom-image-name> sh -c "rq worker -u <redis_url> emails"
```


### run the application in a docker container(using image that was used for the background worker) [CREATES A CONTAINER FOR THE WEB APPLICATION]
```
docker run -p 5000:80 rest-api-recording-email
```
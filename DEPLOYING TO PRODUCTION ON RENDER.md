# DEPLOYING TO PRODUCTION ON RENDER.COM



## Python-flask-api-learning PostgreSQL connection strings

### for render.com DB (expires oct 11, 2024):
```
psql postgresql://python_api_db_user:8Q1p3fFTz0y0wpG00DVHIirr5vMkMlr7@dpg-crh06r08fa8c738qctd0-a.virginia-postgres.render.com/python_api_db
```

### for tembo.io (expiration unknown):
```
psql 'postgresql://postgres:SCE28PIs4fAQTarI@horrifyingly-driving-parrot.data-1.use1.tembo.io:5432/postgres'
```



### Build web app image
```
docker build -t rest-api-recording-email . 
```  


### Run web app image (creates a container)
```
docker run -p 5000:80 rest-api-recording-email
```


### Deployment of redis background worker and web app
```
docker run -w /app <webapp_docker_image> sh -c "rq worker -u <external_redis_url> emails"
```


### Deployment of web app
```
docker run -w /app <web_app_docker_image> sh -c "rq worker -u <redis_url> emails"
```



# NOTE: ADD ENVIRONMENT VARIABLES IN RENDER.COM 
-> use the internal redis url here
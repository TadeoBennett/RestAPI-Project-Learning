FROM python
# EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN flask db upgrade
CMD ["/bin/bash", "docker-entrypoint.sh"] 
#the above is the container running, not the image being built
# so when the container starts it will run the migrations(flask db upgrade was ran previously)


# To run this file use the command
# docker build -t rest-apis-flask-python .







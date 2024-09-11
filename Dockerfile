FROM python
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN flask db upgrade
CMD ["flask", "run", "--host", "0.0.0.0"]

# To run this file use the command
# docker build -t rest-apis-flask-python .







FROM python
EXPOSE 5000
WORKDIR /app
RUN pip install flask
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# To run this file use the command
# docker build -t rest-apis-flask-python .







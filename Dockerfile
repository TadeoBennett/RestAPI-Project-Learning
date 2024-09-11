FROM python
# EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN flask db upgrade
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

# To run this file use the command
# docker build -t rest-apis-flask-python .







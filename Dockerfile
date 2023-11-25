ARG PYTHON_VERSION=3.11.0

FROM python:$PYTHON_VERSION

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code
ENV PYTHONPATH="$PYTHONPATH:/code/messager:"

## Run migrations
RUN #python messager/manage.py migrate
#EXPOSE 8000
# runs the production server
#ENTRYPOINT ["python", "messager/manage.py"]
#CMD ["runserver", "0.0.0.0:8000"]


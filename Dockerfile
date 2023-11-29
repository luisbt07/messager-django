ARG PYTHON_VERSION=3.11.0
# Pull and install python image
FROM python:$PYTHON_VERSION
## Used to generate the Django Relational Diagram
#RUN apt-get update \
#    && apt-get install -y graphviz libgraphviz-dev pkg-config \
#    && pip install pygraphviz \
#    && apt-get install -y graphviz \
#    && pip install pydotplus
# Allows docker to cache installed dependencies between builds

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code
ENV PYTHONPATH="$PYTHONPATH:/code/messager:"

## Run migrations
#RUN python messager/manage.py migrate
#EXPOSE 8000
# runs the production server
#ENTRYPOINT ["python", "messager/manage.py"]
#CMD ["runserver", "0.0.0.0:8000"]


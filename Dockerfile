# pull official base image
FROM python:3.12.4-slim

# set working directory
WORKDIR /usr/src/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update

# install python dependencies
ARG PIP_INDEX_URL
RUN echo "PIP_INDEX_URL is: $PIP_INDEX_URL"
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .
#EXPOSE 8000
EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host","0.0.0.0","--port","8000","--workers","4"]

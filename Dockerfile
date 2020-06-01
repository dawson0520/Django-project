FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
# RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install  -i  https://pypi.doubanio.com/simple/ -r requirements.txt
COPY . /code/

FROM python:3.6
MAINTAINER Pierre-Elouan Rethore <pe@retho.re>

RUN mkdir /app
RUN mkdir /install
WORKDIR /app
COPY requirements.txt /install
RUN pip install -r /install/requirements.txt

COPY scripts/* /app/

EXPOSE 6001

CMD python /app/rest.py

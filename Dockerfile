FROM python:3.6
ADD . /server
WORKDIR /server
EXPOSE 8080
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "server:app"]
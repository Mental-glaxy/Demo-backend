FROM python:alpine3.7
WORKDIR /app

EXPOSE 5000
ENV FLASK_APP=main.py

COPY . /app
#RUN pip install cython
#RUN pip install libffi
RUN apk add --no-cache libffi-dev build-base py2-pip python2-dev && pip install cffi
RUN pip install -r requirements.txt
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]
FROM python:alpine3.7
COPY . /app
WORKDIR /app
#RUN pip install cython
#RUN pip install libffi
RUN apk add --no-cache libffi-dev build-base py2-pip python2-dev && pip install cffi
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
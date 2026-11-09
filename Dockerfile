FROM python:3.14-alpine

RUN apk update \
 && apk upgrade \
 && apk add pango harfbuzz-subset libjpeg-turbo-dev openjpeg-dev libffi-dev font-dejavu \
 && apk cache clean \
 && rm -rf /var/cache/apk/* /lib/apk/db/*
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /tour2pdf
RUN which fastapi
WORKDIR /tour2pdf
EXPOSE 8000
CMD [ "/usr/local/bin/fastapi", "run", "/tour2pdf/tour2pdf.py" ]

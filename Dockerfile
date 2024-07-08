FROM python:3.11-slim-bookworm

RUN apt update
RUN apt upgrade --yes
RUN apt install --yes python3-pip libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 libjpeg-dev libopenjp2-7-dev libffi-dev
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /tour2pdf
RUN which fastapi
WORKDIR /tour2pdf
EXPOSE 8000
CMD [ "/usr/local/bin/fastapi", "run", "/tour2pdf/tour2pdf.py" ]

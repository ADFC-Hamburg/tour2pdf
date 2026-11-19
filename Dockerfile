FROM python:3.14-slim-trixie

RUN apt-get update && apt-get upgrade --yes \
    && apt-get install --yes --no-install-recommends libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 libjpeg62-turbo libopenjp2-7 libffi8 locales \
    && sed -i "s/^# de_DE.UTF-8/de_DE.UTF-8/" /etc/locale.gen && locale-gen \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /tour2pdf
WORKDIR /tour2pdf
EXPOSE 8000
CMD [ "fastapi", "run", "/tour2pdf/tour2pdf.py" ]

#!/usr/bin/python3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import urllib.parse
import urllib.request
import json
from jinja2 import Template

app = FastAPI()


def process_item(event_guid: str):
    url = f'https://dev-api-touren-termine.adfc.de/api/eventItems/{event_guid}'
    raw_data = urllib.request.urlopen(url)
    data = json.loads(raw_data.read().decode('utf-8'))
    return data


def get_adfc_events(request_dict):
    urlquery = urllib.parse.urlencode(request_dict)
    url = f"https://dev-api-touren-termine.adfc.de/api/eventItems/search?{urlquery}"
    raw_data = urllib.request.urlopen(url)

    data = json.loads(raw_data.read().decode('utf-8'))
    events = []
    for ele in data['items']:
        events.append(process_item(ele['eventItemId']))
    return events


def get_request_dict(lat: float = None, lng: float = None, distance: int = 20, beginning: str = None, end: str = None, unitKey: str = None, unitKeys=[], limit=10):
    request_dict = {}
    loc = False
    if lat is not None:
        request_dict['lat'] = lat
        loc = True
    if lng is not None:
        request_dict['lng'] = lng
        loc = True
    if loc:
        request_dict['distance'] = distance
    if beginning is not None:
        request_dict['beginning'] = beginning
    if end is not None:
        request_dict['end'] = end
    if unitKey is not None:
        request_dict['unitKey'] = unitKey
    if len(unitKeys):
        request_dict['unitKeys'] = ",".join(unitKeys)
    request_dict['limit'] = limit
    return request_dict


def get_html(events: list):
    with open('templates/page.html.j2') as f:
        tmpl = Template(f.read())

    mystr = json.dumps(events[0], indent=3)
    return tmpl.render(mystr=mystr, events=events)


def get_css():
    return '''
        h1 { font-family: Arial }'''


@app.get("/api/html",
         responses={
             200: {
                 "content": {"text/html": {}}
             }
         }, response_class=Response
         )
def root(lat: float = None, lng: float = None, distance: int = 20, beginning: str = None, end: str = None, unitKey: str = None, unitKeys=[], limit=10):
    request_dict = get_request_dict(
        lat, lng, distance, beginning, end, unitKey, unitKeys, limit)
    events = get_adfc_events(request_dict)
    html_bytes = get_html(events)
    return Response(content=html_bytes, media_type="text/html")


@app.get("/api/pdf",
         responses={
             200: {
                 "content": {"application/pdf": {}}
             }
         }, response_class=Response
         )
def root(lat: float = None, lng: float = None, distance: int = 20, beginning: str = None, end: str = None, unitKey: str = None, unitKeys=[], limit=10):
    request_dict = get_request_dict(
        lat, lng, distance, beginning, end, unitKey, unitKeys, limit)
    events = get_adfc_events(request_dict)
    # logging.info(data)
    # req = urllib.request.Request(url, data, method='GET')
    # with urllib.request.urlopen(req) as response:
    #    the_page = response.read()
    font_config = FontConfiguration()
    html = HTML(string=get_html(events))
    css = CSS(string=get_css(), font_config=font_config)
    pdf_bytes = html.write_pdf(
        stylesheets=[css], font_config=font_config)
    return Response(content=pdf_bytes, media_type="application/pdf")


app.mount("/", StaticFiles(directory="static", html=True), name="static")

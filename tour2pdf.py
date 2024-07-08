#!/usr/bin/python3

"""
Tour2pdf a script to convert ADFC Tour entrys to a printable PDF.

"""
import urllib.parse
import urllib.request
import json

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response

from tour2pdf_mod import get_jinja_venv, get_html, html_to_pdf, AppConst

app = FastAPI()
jinja_env = get_jinja_venv()
print(AppConst.API_BASE_URL)


def process_item(event_guid: str):
    "Get one Item from API and read json data"
    url = f'{AppConst.API_BASE_URL}/eventItems/{event_guid}'
    with urllib.request.urlopen(url) as raw_data:
        data = json.loads(raw_data.read().decode('utf-8'))
        return data


def get_adfc_events(request_dict):
    "Search for ADFC events with some criteria"
    urlquery = urllib.parse.urlencode(request_dict)
    url = f"{AppConst.API_BASE_URL}/eventItems/search?{urlquery}"
    data = {'items': []}
    with urllib.request.urlopen(url) as raw_data:
        data = json.loads(raw_data.read().decode('utf-8'))
    events = []
    for ele in data['items']:
        events.append(process_item(ele['eventItemId']))
    return events


def get_request_dict(lat: float = None, lng: float = None,
                     distance: int = 20,
                     beginning: str = None, end: str = None,
                     unitKey: str = None, unitKeys: list = None,
                     limit=10):
    "convert params to dict"
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
    if unitKeys:
        request_dict['unitKeys'] = ",".join(unitKeys)
    request_dict['limit'] = limit
    request_dict['eventType'] = 'Radtour'
    return request_dict


@app.get("/api/html",
         responses={
             200: {
                 "content": {"text/html": {}}
             }
         }, response_class=Response
         )
def root_html(lat: float = None, lng: float = None,
              distance: int = 20,
              beginning: str = None, end: str = None,
              unitKey: str = None, unitKeys: list = None,
              limit=10):
    "Query ADFC Api and return in html"
    request_dict = get_request_dict(
        lat, lng, distance, beginning, end, unitKey, unitKeys, limit)
    events = get_adfc_events(request_dict)
    html_bytes = get_html(jinja_env, events, False)
    return Response(content=html_bytes, media_type="text/html", )


@app.get("/api/pdf",
         responses={
             200: {
                 "content": {"application/pdf": {}}
             }
         }, response_class=Response
         )
def root_pdf(lat: float = None, lng: float = None,
             distance: int = 20,
             beginning: str = None, end: str = None,
             unitKey: str = None, unitKeys: list = None,
             limit=10):
    "Query ADFC Api and return as pdf"
    request_dict = get_request_dict(
        lat, lng, distance, beginning, end, unitKey, unitKeys, limit)
    events = get_adfc_events(request_dict)
    html_bytes = get_html(jinja_env, events, True)
    pdf_bytes = html_to_pdf(html_bytes)
    return Response(content=pdf_bytes, media_type="application/pdf")


app.mount("/html_root", StaticFiles(directory="html_root",
          html=True), name="html_root")
app.mount("/", StaticFiles(directory="static", html=True), name="static")

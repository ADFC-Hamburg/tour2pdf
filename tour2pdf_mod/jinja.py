
from jinja2 import Environment, PackageLoader, select_autoescape
import qrcode
import io
from base64 import b64encode
import json
from datetime import datetime
import locale
from markdown import markdown
RADTOUR_URL = "https://touren-termine.adfc.de/suche?eventType=Radtour&unitKey=158"
TOUR_URL_PREFIX = "https://touren-termine.adfc.de/radveranstaltung/"


def qrcode_filter(input):
    """QR Code filter"""
    qr = qrcode.QRCode()
    qr.add_data(input)
    m = qr.make_image()
    img_byte_arr = io.BytesIO()
    m.save(img_byte_arr, format="PNG")
    b64str = b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return f'data:image/png;base64, {b64str}'


def to_json_filter(input):
    return json.dumps(input, indent=2)


def date_format_filter(input: str, format: str):
    date_obj = datetime.fromisoformat(input)
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    return date_obj.strftime(format)


def markdown2html_filter(input: str):
    return markdown(input)


def get_jinja_venv():
    jinja_env = Environment(
        loader=PackageLoader("tour2pdf", "templates"),
        autoescape=select_autoescape()
    )
    jinja_env.filters['qrcode'] = qrcode_filter
    jinja_env.filters['to_json'] = to_json_filter
    jinja_env.filters['from_json'] = json.loads
    jinja_env.filters['date_format'] = date_format_filter
    jinja_env.filters['markdown_to_html'] = markdown2html_filter
    return jinja_env


def get_html(jinja_env, events: list, pdf_view: bool):
    tmpl = jinja_env.get_template('page.html.j2')
    mystr = json.dumps(events[0], indent=3)
    return tmpl.render(events=events, pdf_view=pdf_view, RADTOUR_URL=RADTOUR_URL, TOUR_URL_PREFIX=TOUR_URL_PREFIX)

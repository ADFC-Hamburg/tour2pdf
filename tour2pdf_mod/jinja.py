""" Jinja 2 Environment Part
"""
import io
import json
from base64 import b64encode
from datetime import datetime
import locale

from jinja2 import Environment, PackageLoader, select_autoescape
import qrcode
from markdown import markdown
from .const import AppConst


def qrcode_filter(qrinput):
    """QR Code filter"""
    qr = qrcode.QRCode()
    qr.add_data(qrinput)
    m = qr.make_image()
    img_byte_arr = io.BytesIO()
    m.save(img_byte_arr, format="PNG")
    b64str = b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return f'data:image/png;base64, {b64str}'


def to_json_filter(jinput):
    """ Converst a datastructure to json"""
    return json.dumps(jinput, indent=2)


def date_format_filter(dinput: str, dateformat: str):
    """ Converts an ISO Datestring to a german Datestr with format"""
    date_obj = datetime.fromisoformat(dinput)
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    return date_obj.strftime(dateformat)


def markdown2html_filter(mdinput: str):
    """ Convert markdown to html"""
    return markdown(mdinput)


def get_jinja_venv():
    """ Get an jinja2 Environment """
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
    """ get html output"""
    tmpl = jinja_env.get_template('page.html.j2')
    from_date = None
    to_date = None
    for e in events:
        if e['eventItem']['beginning'] is not None:
            datum = datetime.fromisoformat(e['eventItem']['beginning'])
            if from_date is None or datum < from_date:
                from_date = datum
            if to_date is None or datum > to_date:
                to_date = datum
    return tmpl.render(events=events,
                       pdf_view=pdf_view,
                       RADTOUR_URL=AppConst.RADTOUR_URL,
                       TOUR_URL_PREFIX=AppConst.TOUR_URL_PREFIX,
                       VERSION=AppConst.VERSION,
                       SHOW_API_LINK=AppConst.SHOW_API_LINK,
                       today=datetime.now().isoformat(),
                       from_date=from_date.isoformat(),
                       to_date=to_date.isoformat())

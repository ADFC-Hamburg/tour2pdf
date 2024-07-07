from weasyprint import HTML


def html_to_pdf(html_bytes: str):
    html = HTML(string=html_bytes,
                base_url='./html_root/')
    pdf_bytes = html.write_pdf()
    return pdf_bytes

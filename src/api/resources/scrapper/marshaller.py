from flask_restx import fields

from src.api.namespaces import NAMESPACES

scrapper_ns = NAMESPACES["Scrapper"]

scrapper_standard_serializer = scrapper_ns.model(
    "ScrapperStandard",
    {
        "message": fields.String(),
        "url_status": fields.String(),
        "url_html_size": fields.String(),
    },
)

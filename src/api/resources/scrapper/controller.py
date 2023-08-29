from flask_restx import Resource
from src.api import exceptions

from src.api.namespaces import NAMESPACES
from src.api.resources.scrapper.marshaller import scrapper_standard_serializer
from src.api.resources.scrapper.parser import scrapper_parser
from src.api.resources.scrapper.service import ScrapperService

scrapper_ns = NAMESPACES["Scrapper"]


@scrapper_ns.route("/")
class SnapshotUrl(Resource):
    """Resource to handle all scrapper operations"""

    @scrapper_ns.marshal_with(scrapper_standard_serializer, skip_none=True)
    @scrapper_ns.expect(scrapper_parser, validate=True)
    @scrapper_ns.response(200, "Success")
    @scrapper_ns.response(201, "Created")
    @scrapper_ns.response(400, "Bad request")
    @scrapper_ns.response(500, "Internal Server Error")
    def put(self):
        """snapshot url"""
        args = scrapper_parser.parse_args(strict=True)
        try:
            status, html = ScrapperService.scrap_url(args)
            http_response = {
                "message": "URL_SNAPSHOT_CREATED",
                "url_status": status,
                "url_html_size": len(html),
            }
            return http_response, 201
        except (
            exceptions.ScrappingPNGError,
            exceptions.ScrappingHTMLError,
        ):
            http_response = {
                "message": "URL_SNAPSHOT_FAILED",
            }
            return http_response, 200

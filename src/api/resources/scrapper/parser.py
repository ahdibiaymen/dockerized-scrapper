from flask_restx import reqparse, inputs

scrapper_parser = reqparse.RequestParser()

scrapper_parser.add_argument(
    "url",
    type=inputs.URL(),
    location="json",
    required=True,
    nullable=False,
)

scrapper_parser.add_argument(
    "png_path",
    type=str,
    location="json",
    required=True,
    nullable=False,
)

scrapper_parser.add_argument(
    "html_path",
    type=str,
    location="json",
    required=True,
    nullable=False,
)

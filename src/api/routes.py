from src.api.resources.scrapper.controller import scrapper_ns


def register_endpoints_routes(api):
    """Routes "namespaces" Registration"""
    api.add_namespace(scrapper_ns)

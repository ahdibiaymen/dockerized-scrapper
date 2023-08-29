import sys

from src.app import create_app

app = create_app()

sys.stdout = sys.stderr

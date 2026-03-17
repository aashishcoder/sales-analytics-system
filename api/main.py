# Compatibility file to redirect to tableau_main
from api.tableau_main import app

# This redirects any imports from api.main to the tableau_main module
__all__ = ['app']

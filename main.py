from database import setup_tables,insert_default_categories
from gui import start_app
setup_tables()
insert_default_categories()
start_app()
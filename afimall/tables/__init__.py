import os
from afimall.sql_utils import run_sql_script


def create_tables(sql_scripts_path: str, connection) -> None:
    """Create tables"""
    with open(os.path.join(sql_scripts_path, 'create_tables.sql'), 'r') as f:
        run_sql_script(f, connection)

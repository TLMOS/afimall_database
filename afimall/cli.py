"Command Line Interface for Afimall DataBase"


import os
import click
import json
import configparser
from afimall import sql_utils
from afimall import tables
from afimall.tables import store_category, store_to_category
from afimall import connection


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')

SAMPLES_PATH = config['PATH']['SAMPLES']
SQL_SCRIPTS_PATH = config['PATH']['SQL_SCRIPTS']

TABLES = json.loads(config['TABLES']['TABLES'])

STORE_SIZE = int(config['SCRIPTS']['STORE_SIZE'])
STORE_MAX_CATEGORIES = int(config['SCRIPTS']['STORE_MAX_CATEGORIES'])
STORE_CATEGORY_SIZE = int(config['SCRIPTS']['STORE_CATEGORY_SIZE'])
STORE_CATEGORY_MAX_DEPTH = int(config['SCRIPTS']['STORE_CATEGORY_MAX_DEPTH'])
STORE_CATEGORY_SPLIT_CHANCE = float(config['SCRIPTS']['STORE_CATEGORY_SPLIT_CHANCE'])


@click.group()
def cli():
    """Afimall DataBase CLI"""


@cli.command()
def create_tables():
    """Create tables"""
    tables.create_tables(SQL_SCRIPTS_PATH, connection)


@cli.command()
def create_sql_scripts():
    """Create SQL scripts"""
    parent_id = store_category.create_parent_id(
        STORE_CATEGORY_SIZE,
        STORE_CATEGORY_MAX_DEPTH,
        STORE_CATEGORY_SPLIT_CHANCE
    )
    store_category.create_script(
        SQL_SCRIPTS_PATH,
        SAMPLES_PATH,
        STORE_CATEGORY_SIZE,
        parent_id
    )
    store_to_category.create_script(
        SQL_SCRIPTS_PATH,
        STORE_SIZE,
        STORE_CATEGORY_SIZE,
        parent_id,
        STORE_MAX_CATEGORIES
    )


@cli.command()
def fill_tables():
    """Fill tables"""
    for table in TABLES:
        script = os.path.join(SQL_SCRIPTS_PATH, f'fill_{table}.sql')
        if not os.path.exists(script):
            print('Script not found:', script)
            return
    for table in TABLES:
        script = os.path.join(SQL_SCRIPTS_PATH, f'fill_{table}.sql')
        with open(script, 'r') as f:
            sql_utils.run_sql_script(f, connection)


@cli.command()
def clear_database():
    """Clear database"""
    sql_utils.clear_database(connection, TABLES)

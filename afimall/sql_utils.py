"""SQL utility functions for the afimall package."""


import pandas as pd
from typing import IO


def df_to_sql(df: pd.DataFrame, table_name: str, file: IO):
    """Transforms a pandas DataFrame into a SQL insert script."""
    commands = []
    cols = df.columns
    template = f'insert into {table_name} ({", ".join(cols)}) values '
    for row in df.values:
        commands.append(template + f'({", ".join(list(map(str, row)))});\n')
    file.writelines(commands)


def run_sql_script(file, connection):
    """Runs a SQL script from a file-like object."""
    cursor = connection.cursor()
    try:
        command = file.read()
        cursor.execute(command)
        connection.commit()
    except Exception as e:
        print('ERROR: ', e)
    finally:
        cursor.close()


def clear_database(connection, tables):
    """Clears the database by cascade dropping all tables"""
    for table in tables:
        cursor = connection.cursor()
        try:
            command = f'DROP TABLE public.{table} CASCADE;'
            cursor.execute(command)
            connection.commit()
        except Exception as e:
            print('ERROR: ', e)
        finally:
            cursor.close()

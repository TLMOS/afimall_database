# Afimall DataBase
Course project for Database course in MEPHI 2022.

## CLI Interface
You can access cli by running afimall module:

```console
$ python -m afimall --help
Usage: python -m afimall [OPTIONS] COMMAND [ARGS]...

  Afimall DataBase CLI

Options:
  --help  Show this message and exit.

Commands:
  clear-database      Clear database
  create-sql-scripts  Create SQL scripts
  create-tables       Create tables
  fill-tables         Fill tables
```

## Configuration
You can configure database connection by creating `.env` file.
```
DB_USER=postgres
DB_PASSWORD=[Your password]
DB_HOST=localhost
DB_PORT=5432
DB_NAME=afimall
```
Other options can be found in `config.ini`.

To install all required packages run:
```console
$ pip install -r requirements.txt
```
## How to run tests

This folder includes an example model, including:

* Topic
* Country
* Topic-Country for a many-to-many relationship

Dev dependencies are required to run the tests. Running the following command
with `alembic`:

```bash
alembic upgrade head
```

Will cause the creation of an `example.db` SQLite database (as per `alembic.ini`
configuration, containing the structure defined in the `structure` migration).

The structure migration has been generated automatically from the model defined
in `env.py`, using the following command:

```bash
alembic revision -m "structure" --autogenerate
```


Quickstart
----------

First, clone the project on your local machine: ::

git clone https://github.com/zaid-zubi/Storehouse_project.git

Then activate poetry by typing: ::

    poetry shell
If the poetry not installed, install it before implementing the previous command: ::

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
    export PATH="$HOME/.poetry/bin:$PATH"
    poetry install
    poetry shell

Then create ``.env`` file and fill it by the following variables ::

    DB_ENGINE=postgresql
    DB_NAME=#DON'T Forget to set this value
    DB_USERNAME=#DON'T Forget to set this value
    DB_PASSWORD=#DON'T Forget to set this value
    DB_HOST=localhost
    DB_PORT=5432
    ENVIRONMENT=local
Then run the migration files use::

    alembic upgrade head
Finally to run the app::

    uvicorn app.main:app --reload
    or

    uvicorn app.main:app --reload --port {PORT_NUMBER}
API documentation
----------

All APIs are available on ``{{base_url}}/users/docs`` or ``{{base_url}}/users/redoc`` paths with Swagger or ReDoc.




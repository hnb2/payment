This is the auth application responsible for signin and signup.

## Installation

This project requires pip and virtualenv.

 * `virtualenv env`
 * `source env/bin/activate`
 * `cd app`
 * `pip install -r requirements.txt`
 * `pip install -r tests/requirements.txt`
 * `python manage.py runserver`

## Environment variables

 * `DEBUG: boolean` True will enable debug mode, and display full stack trace and an interactive shell in the browser
 * `SECRET_KEY: String` Secret key of the application, make sure to change it every time you make a new project
 * `LOGENTRIES_TOKEN: String` Token for logentries service, can be left empty when developing locally

## Curl examples

TODO

## Documentation

Endpoints are documented using flask-swagger, each individuals endpoint must have swagger doc in YML format.
The final json document can be reached at: http://localhost:5000/spec

## Tests

 Nose documentation: http://nose.readthedocs.io/en/latest/plugins/cover.html

 * Simple unit tests run: `nosetests`
 * Need to display stdout (print/logging/...): `nosetests --nocapture`
 * Need a code coverage report: `nosetests --with-coverage --cover-package=app`
 * Need a code coverage HTML report: add the flag `--cover-html` to the command above, a directory `cover` will be created in the current directory with an index.html

## Code style

 * PEP-8 is followed and asserted using flake8 linter. There is a .flake8 file at the root of app, most IDEs/text editors can use it to determine the preferences.
 * Currently, the setting E501 for the max length of lines is disabled, it can be customized using: `max-line-length = 120` in the configuration file.
 * If you need to disable a specific setting on a specific line, you can add an inline comment like: `example = lambda: 'example'  # noqa: E731`
 * But it is also possible to run this tool in command line, just go inside app and type: `flake8`

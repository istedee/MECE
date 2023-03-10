# MECE [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
Distributed systems project 2023

### Docker deployment

Have both

[Docker](https://www.docker.com/) and [Docker compose](https://docs.docker.com/compose/install/linux/) installed

Run command:

```bash
$ docker-compose up --build
```
in the /server directory

You can see the docs at:
http://127.0.0.1:8000/docs

### Manual deployment

Start the server by:

```bash
$ python3 server/app/main.py
```

Running the manual command will cause the FastAPI server to create/use database file found from the current directory where the run command was issued from.

This does not cause any issues, but some data might not be present during development if multiple locations are used. So, in order to use constant environment, using Docker compose is encouraged.

### Using the client

python3 client.py --localhost=True

you can substitute localhost with the external IP of your FastAPI deployment if one is available.
If localhost is not set, it defaults to our rahtiapp-deployment which may or may not be available.

### Testing

You can manually test the application with Pytest

Run command:

```bash
$ ./test.sh
```

or

```bash
$ python3 -m pytest
```

From the app folder to execute tests.

To get coverage of test use command:

```bash
$ ./test-with-coverage.sh
```

or

```bash
$ python3 -m pytest --cov=. --cov-report term-missing tests/
```

This will output the test results as collection.
Run above command from the app directory as well.

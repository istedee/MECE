# MECE [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
Distributed systems project 2023

## Docker deployment

Have both

[Docker](https://www.docker.com/) and [Docker compose](https://docs.docker.com/compose/install/linux/) installed

### Server deployment

Run command:

```bash
$ docker-compose up --build
```
in the ```/server``` directory

You can see the docs at:
http://127.0.0.1:8000/docs

### Client deployment

Run the following command from the ```/client``` folder:

```bash
sudo ./start_client.sh
```
This will spin up a docker container for easy use of the client. <br>

```NOTE!``` <b> the script requires root to work </b>, always check the contents of script running as root before execution!

Usage of Docker is heavily advised, since this way you do not have to manually setup the environment. <br> Please find the guide for manual installation below.

## Manual deployment

Required pip packages are found from the respective requirements.txt files from each of the repository folders.
Please use pythons provided virtual environment package for easier deployment and avoiding global conflicts on your machine.


Following commands are tested for Unix environments.

Spawn ```python3 venv``` with command:

```bash
python3 -m venv env
```

Activate the new virtual environment:


```bash
source env/bin/activate
```

And install the requirements by:

```bash
pip install -r requirements.txt
```


Start the server by:

```bash
$ python3 server/app/main.py
```

Running the manual command will cause the FastAPI server to create/use database file found from the current directory where the run command was issued from.

This does not cause any issues, but some data might not be present during development if multiple locations are used. So, in order to use constant environment, using Docker compose is encouraged.

You can also use an external database for the application via adding a .env file to the server folder with the EXTERNAL-IP value set.

### Using the client

For the localhost usage:

```bash
python3 client.py
```

This defaults to the localhost version of the application, which requires the environment to be deployed before usage.
For the remote server usage with the client please use the following command:

```bash
python3 client.py --rahtiapp RAHTIAPP
```

If rahtiapp is set, the client tries to connect to our cloud-deployment. which may or may not be available.
DISCLAIMER: your mileage may vary

### Testing

You can manually test the application with Pytest
Run testing commands in the server directory.

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

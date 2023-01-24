### Docker deployment

Have both

[Docker](https://www.docker.com/) and [Docker compose](https://docs.docker.com/compose/install/linux/) installed

Run command:

```bash
$ docker-compose up --build
```

You can see the docs at: 
http://127.0.0.1:8000/docs

### Manual deployment

Start the server by:

```bash
$ python3 app/main.py
```

Running the manual command will cause the FastAPI server to create/use database file found from the current directory where the run command was issued from.

This does not cause any issues, but some data might not be present during development if multiple locations are used. So, in order to use constant environment, using Docker compose is encouraged.


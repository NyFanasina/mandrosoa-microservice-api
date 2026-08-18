# Mandrosoa API Backend Microservice

A brief description of how to lauch this Microservice API.
Each request should pass through the gateway API at **http://localhost:8000/api/**

## Run Locally For Developpment

Clone the project

```bash
  git https://gitlab.com/immobiliers/mandrosoa-backend/ <project-name>
```

Go to the project directory

```bash
  cd <project-name>
```

Create the docker image

```bash
  docker compose build
```

Start the server

```bash
  docker compose up
```

## Documentation

Here are the services availables

- [http://localhost:8000/docs#/](http://localhost:8000/docs#/) (Gateway API)
- [http://localhost:8001/docs#/](http://localhost:8001/docs#/) (User service)
- [http://localhost:8002/docs#/](http://localhost:8002/docs#/) (Listing service)
- [http://localhost:8003/docs#/](http://localhost:8003/docs#/) (Booking service)

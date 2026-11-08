# chatgpt-clone

## Backend

#### How to build and run the docker backend app
```shell
docker build -t fastapi-backend-app .
docker run -d -p 8000:8000 fastapi-backend-app:latest
```

## Alembic initialization
```shell
alembic init alembic
```

### Generate initial table
```shell
alembic revision --autogenerate -m "initial schema"
```
### Create new migration file
```shell
alembic revision -m "message"
```
### Apply migraiton
```shell
alembic upgrade head
```

## Ollama

#### Model
```shell
docker compose exec ollama ollama pull llama3.2:3b
```

# chatgpt-clone

## Backend

#### How to build and run the docker backend app
```shell
docker build -t fastapi-backend-app .
docker run -d -p 8000:8000 fastapi-backend-app:latest
```

### Alembic initialization
```shell
alembic init alembic
```

### Generate initial table
```shell
alembic revision --autogenerate -m "initial schema"
```

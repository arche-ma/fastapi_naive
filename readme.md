# FASTAPI_NAIVE: FASTAPI-BASED GRAPHQL BACKEND FOR E-COMMERCE

Backend for online naive art store powered by FastApi and Strawberry.
At the moment application is ready to perform essential tasks related to data manipulation:
- adding and editing artists and their artworks
- creating and editing customers orders
- adding and editing customers carts
- providing artists and artworks data for clients using highly customizable graphql requests

## Used libraries
- FastApi backend framework which does all the heavy lifting
- Strawberry for defining graphql-schemas and data validation
- PyJWT responsible for jwt-authentication
- SqlAlchemy for database manipulations.

## Database
PostgreSQl

## Infra
Docker, docker-compose

## Launching project locally
1. Clone project on your local computer:
```console
git clone https://github.com/arche-ma/fastapi_naive
```
2. Launch docker containers
```console
docker-compose up -d

```
3. Populate database with test data. Use command 
```console
docker ps
```
to see actual title of the backend container. Then launch the python script in the backend container to populate the database with test data

```console
docker exec fastapi_naive_backend_1 python populate.py
```

After performing these three steps application should be available locally via http://127.0.0.1/graphql.
All accessible graphql schemas and mutations are described in docs section.


## Operations with carts
Current project doesn't imply user registration. User cart uuid is set in cookies so one should fetch it from there for further manipulations.

## Images
Artists and artworks images should be passed to the backend using base-64 image encoding format. 

## TODO
- Data validation for orders
- Custom exceptions for error handling
- Graphql error types for expected exceptions
- New order handlings for admins and clients: notifications via email and telegram
- Test data loading automation
- Test coverage
- Pagination and filters



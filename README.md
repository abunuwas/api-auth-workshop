# Building API applications with FastAPI [Workshop]

Code for the workshop Working with SQLAlchemy and Alembic.

In this workshop, we add the database layer for the Job Portal API.

## Instructor: Jose Haro Peralta

[![image](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jose-haro-peralta/) [![image](	https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/JoseHaroPeralta)

### Full stack consultant and founder of [microapis.io](https://microapis.io)

### Author of [Microservice APIs](https://www.manning.com/books/microservice-apis)


## What are SQLAlchemy and Alembic?

**SQLAlchemy** is Python's most popular Object Relational Mapper (ORM). 
ORMs are frameworks that offer an object-oriented interface to your 
database tables. ORMs give you a layer of abstraction on top of SQL, 
so you don't have to write SQL queries by hand - instead, you just write
code. ORMs also abstract away the differences between SQL engines, such
as PostgreSQL and MySQL, so you can switch between one and the other 
without having to change your code. You can learn more about SQLAlchemy
with its official documentation: https://www.sqlalchemy.org/.

**Alembic** is a database migrations management framework. Alembic ensures
that your database schemas accurately reflect the data models that you 
define with SQLAlchemy. You can learn more about Alembic with its official
documentation: https://alembic.sqlalchemy.org/en/latest/.

## Agenda for the workshop

1. Understand API implementation requirements for our [database models](models_diagram.png)
2. Set up the environment and install dependencies.
3. Initialise and configure Alembic.
4. Add SQLAlchemy models.
   1. Basic models
   2. Relationships
   3. Constraints
5. Generate and apply migrations.
6. Learn about batch operations in Alembic.
7. Learn to perform queries and writes.
8. Add database operations to API.
9. Dataclasses for SQLAlchemy models.
10. Asynchronous SQLAlchemy.

## Free ebook copy of Microservice APIs raffle

At the end of the workshop, I'll raffle a free ebook copy of my book 
Microservice APIs.

Enter your details [here](https://woorise.com/miocroapis/microservice-apis-ebook-sqla)
to participate in the raffle.

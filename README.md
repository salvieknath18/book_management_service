# book_management_service

This is service for book management system. creating CRUD APIs for Books and User.


### Setup Environment
There are two ways to setup the environment on local
#### Using Docker
This is simplest way to setup environment on local
   - Download Docker and start docker engine
   - Clone the code from repository to local
   - Open CMD go to root directory of project
   - Run command `docker-compose up`
   - It will up service for backend on port 5000 (http://localhost:5000

### Using Local Python Setup
   - download python with version 3.7 or greater
   - clone the project on local repository
   - create file .env on root location (ref .env template))
   - setup environment variable `ENV_FILE_LOCATION=./.env`
   - in file .env we can give the required configurations for db setup"
   - run command `pip install -r requirement.txt` on root directory to install dependencies
   - run command `python app.py`
   - application will start on port 5000(http://localhost:5000)

### To run tests
   - create file .env.test on root location (ref .env template))
   - setup environment variable `ENV_FILE_LOCATION=./.env.test`
   - run command "unittest book_management_service/tests"
   - test case will run and show success and failure tests

### Assumptions made
While developing the assignment I have made few assumptions
   - ISBN number is the International Standard Book Number which is a numeric commercial book identifier that is intended to be unique. so, I used that as a unique constraint for book model
   - As admin can only create user so there is no signup page in front end so first admin user has to be created manually using register API.

### Project Structure
Project structure diagram 
![Project structure diagram](https://github.com/salvieknath18/book_management_service/blob/main/BookManagementService.png?raw=true)

#### Project is structured in to following Layers:
1. Application : Starting point of project, all configurations, initialization and setups are done here
2. Router : Here End points are mentioned, For which client request which logic is to implement is the main purpose of the router.
3. Controllers:
   Controllers get the request formulate the request data and call appropriate service to build the response
   1. Auth Controller : Responsible Authentication and Authorization.
   2. User Controller : Responsible Create, Read, Update, Delete operations for User
   3. Book Controller : Responsible Create, Read, Update, Delete operations for Book
   4. Borrow Controller : Controls the entries of borrow and return books
   5. Analytics Controller : Responsible to serve analytical requests
4. Services: Services communicate with model and build logic to serve request
   1. User Service: logical blocks to serve user related request
   2. Book Service: logical blocks to serve user related request
   3. Borrow Service: Written functions to borrow and return book, and add entry in DB
   4. Analytics Service: This service builds logic to get some analysis on data, and for data it will ask for other service
5. Models:
    It is responsible to persist structured data in collections.
   1. User : Maintain User data
   2. Book : Maintain Book data
   3. Borrow : Maintain Borrow and Return entries.
   DB Model Diagram
   ![Project structure diagram](https://github.com/salvieknath18/book_management_service/blob/main/db_model.png?raw=true)
   

### API Design:

Followed REST API Design Principals for designing the API
   - Platform independent, Any client can request for data
   - GET method typically returns HTTP status code 200 (OK). If the resource cannot be found, the method should return 404 (Not Found).
   - POST method creates a new resource, it returns HTTP status code 201 (Created). The URI of the new resource is included in the Location header of the response. The response body contains a representation of the resource.
   - PUT method update resource by getting id of resource and all updated data
   - delete method delete the resource
The details of API is mentioned in the API documentation created using swagger.
Swagger URL: http://host:port/swagger(http://localhost:5000/swagger)


### Code Implementation:

Used Flask framework for the development of the REST APIs.
Followed best practices and standards that can be implemented in given time.
   - PEP 8 standard
   - model-service-controller architecture
   - written sample testcases (actually we suppose to write testcases first as per acceptance criteria provided by BA and then start development, but due to time constraint only written few test for as sample we can extend those)
   - extensive exception handling
   - containerise application
   - API documentation

### Scalability of Project:

We can extend this project to next level. here are some future scopes.
   - To address requirement where Local book identity number or local book with no ISBN
   - Once admin create user he will share creds with respective user via any channel(password email to member or create password link for member)
   - We can give provision for member to register and admin can approve the request and user is created.
   - History of borrower can be leveraged more by adding entry_id in bookEntry for future analytics, we can get analytics like most borrowed book, most likely read genre etc. so that we can enhance collection 
   - If we have to track copies of book we can implement following APIs with few modifications in model
   - filter, sorting can also be handled in backend

### Improvements

There are few things which I suppose to be implemented as a part of standard practice, but due to time constraint I didn't got time to implement those 
   - validation to post request incoming data
   - unit tests for all scenarios (only written few sample test)
   - extensive and detailed documentation for API (used swagger but need to add more details)
   - use of dataclasses/named tuples for the model data.

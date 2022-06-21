# book_management_service

This is a service for book management systems.


### Setup Environment
There are two methods for configuring the local environment.

#### Using Docker
This is the most basic method for creating a local environment.

* Download Docker and start the Docker engine.
* Clone the code from the repository to your local machine.
* Open CMD navigate to the project's root directory.
* Run the command `docker-compose up`
* It will provide service for the backend on port 5000 (http://localhost:5000).

### Using the Local Python Setup
* Python 3.7 or later must be downloaded.
* Clone the project to your local repository.
* file.env in the root directory (ref.env template)
* setup environment variable `ENV_FILE_LOCATION=./.env`
* In file .env we can give the required configurations for DB setup.
* run the command `pip install -r requirement.txt` in the root directory to install dependencies.
* run command: `python app.py`
* The application will start on port 5000 (http://localhost:5000).

Note: Added one additional end point (http://localhost:5000/loadData) to load dummy data.

### To carry out tests
* make a file.env.test in the root directory (ref.env template))
* environment variable configuration `ENV_FILE_LOCATION=./.env.test`
* run command `unittest book_management_service/tests`
* Test cases will be run and show success and failure tests.

### Assumptions made
While developing the assignment, I made a few assumptions.
* ISBN number is the International Standard Book Number, which is a numeric commercial book identifier that is intended to be unique. so, I used that as a unique constraint for book model.
* As admin can only create users, there is no signup page in the front end, so the first admin user has to be created manually using the register API.
* Added one additional end point (http://localhost:5000/loadData) to load dummy data.
### Project Structure
Project structure diagram 

![Project structure diagram](https://github.com/salvieknath18/book_management_service/blob/main/BookManagementService.png?raw=true)

#### Project is structured in to following Layers:
1. Application : The project's starting point, where all configurations, initialization, and setups are completed.
2. Router : Here end points are mentioned for which client request which logic is to be implemented is the main purpose of the router.
3. Controllers:
   Controllers get the request, formulate the request data, and call the appropriate service to build the response.
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
   1. User : Keep User Data
   2. Book : Maintain Book data
   3. Borrow : Maintain Borrow and Return entries.
   DB Model Diagram
   ![Project structure diagram](https://github.com/salvieknath18/book_management_service/blob/main/db_model.png?raw=true)
   

### API Design:

The API was designed using REST API Design Principles.

* Any client, regardless of platform, can request data.
* The GET method typically returns an HTTP status code of 200 (OK). If the resource cannot be found, the method should return 404 (Not Found).
* POST creates a new resource and returns the HTTP status code 201 (Created).The URI of the new resource is included in the Location header of the response. The response body contains a representation of the resource.
* The PUT method updates a resource by retrieving the resource's id and all updated data.
* The DELETE method deletes the resource. The details of the API are mentioned in the API documentation created using swagger. Swagger URL: http://host:port/swagger (http://localhost:5000/swagger)


### Code Implementation:

used the Flask framework for the development of the REST APIs. Followed the best practises and standards that can be implemented at any given time.
* PEP 8 is a standard.
* model-service-controller architecture
* According to the acceptance criteria provided by BA, we are supposed to write test cases first and then begin development, but due to time constraints, I have only written a few tests as a sample, which we can extend.
* containerise application.
* API documentation

### Scalability of Project:

We can extend this project to the next level. Here are some future scopes.

* To meet requirements where there is no local book identity number or a local book with no ISBN
* Once admin create user he will share creds with respective user via any channel(password email to member or create password link for member)
* We can give provision for members to register and an admin can approve the request and the user is created.
* History of borrower can be leveraged more by adding entry_id in bookEntry for future analytics, we can get analytics like most borrowed book, most likely read genre etc. so that we can enhance collection
* If we have to track copies of a book, we can implement the following APIs with a few modifications in the model.
* filter, sorting can also be handled in the backend.

### Improvements

There are few things which I suppose to be implemented as a part of standard practice, but due to time constraint I didn't got time to implement those 
   - validation to post request incoming data
   - unit tests for all scenarios (only written few sample test)
   - extensive and detailed documentation for API (used swagger but need to add more details)
   - use of dataclasses/named tuples for the model data.

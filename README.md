# book_management_service

This is service for book management system. creating CRUD APIs for Books and User.


Project Structure
Project is structure in to following Layers:
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

Project structure diagram 
![Project structure diagram](https://github.com/salvieknath18/book_management_service/blob/main/BookManagementService.png?raw=true)
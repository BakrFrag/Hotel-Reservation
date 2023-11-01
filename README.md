# Hotel Reservation System 
users can register , login view rooms do reservation , get list of all reservations 

### Database & Schema Design 
there are 3 entities  `User` `Reservation` and `Room`
for Relations 
- `user` has one to many to `Reservation` 
- `Room` has one to many to `Reservation` 
- `Reservation` act as cross table or join table 

- Schema Design Draw : https://drawsql.app/teams/development-9/diagrams/room-reservations

### API Documenting 
- for various request & response in different testcases thank to check attached postman collection , organized by folders and each folder have many requests on it , each request have a lot of responses examples in different testcases
- you can load directly in postman app 
- Link: https://api.postman.com/collections/6749950-5a30b2af-1fb3-419c-980c-278b54bfec24?access_key=PMAT-01HE4YZSZ8KE262RBS4J0W8HKE

### Assumptions

- for simplicity `authentication` applied only on `reservation` 
- in `reservation` the minimum time unit is `one day`	 

### Tech Stack 
- `FastAPI` as backend framework over `python`
- `uvicorn` as `asgi server` 
- `sqlalchemy` as ORM
- `sqlite3` as RDMS
### API END Points 
| URL |Methods  |Description|
|--|--|--|
| /user/login/| POST |user login using `username` and `password`|
|/user/register/|POST|user register with `username` , `password` and `confirm` , confirm must match `password` value |
|/user/all/| GET|list of all users|
|/room/add/ | POST | add new room to system , room `code` must be unique , `price` must be greater than 0 |
|/room/{ID}/| GET| get specific room details |
|/room/all/| GET| list of all rooms| 
|room/{ID}/|PUT| update room `code` must be unique , `price` must be greater than 0|
|/room/{ID}/|DELETE| delete room by `ID`|
|/reservation/{ID}/GET| get reservation by `id` , current user must be owner of reservation|
|/reservation/all/|GET|list of all reservation for current logged in user|
|/reservation/add/|POST| create new reservations , `user_id` by default take current logged in user , `room_id` must be exists , reservation `room` mustn't be overlapped with other reservations , `room` for reservation must be in service , `from_date` and `to_date` must be in today and future , `to_date` must be greater than `from_date` |
|/reservation/{ID}/|DELETE|reservation current user must be owner for reservation , reservation can only cancel before `from_date` with 2 days at least |

### Build Locally 

- machine with `python >3.5` and `pip` as package manager 
- git clone url on github `git clone {URL}` 
- install `pipenv` as package manager `pip install pipenv` 
- move to cloned project folder `cd {project folder}`
- run `pipenv shell` to create & activate virtual env 
- run 	`pipenv install -r requirements.txt` to install dependencies  
- run `uvicorn app.main:app --reload` to start application locally 
- no start play with `API End Points`
 
# Maintenance-Tracker-Application 
[![Build Status](https://travis-ci.com/RuthNjeri/Maintenance-Tracker-Application.svg?branch=develop)](https://travis-ci.com/RuthNjeri/Maintenance-Tracker-Application)

[![Coverage Status](https://coveralls.io/repos/github/RuthNjeri/Maintenance-Tracker-Application/badge.svg?branch=develop)](https://coveralls.io/github/RuthNjeri/Maintenance-Tracker-Application?branch=develop)

[![Maintainability](https://api.codeclimate.com/v1/badges/2f140a8751ec676cd7d1/maintainability)](https://codeclimate.com/github/RuthNjeri/Maintenance-Tracker-Application/maintainability)

## PROJECT FEATURES
1. Users can create an account and log in.<br>
2. The users should be able to make maintenance or repairs request.<br>
3. An admin should be able to approve/reject a repair/maintenance request.<br>
4. The admin should be able to mark request as resolved once it is done.<br>
5. The admin should be able to view all maintenance/repairs requests on the application.<br>
6. The admin should be able to filter requests.<br>
7. The user can view all his/her requests.<br>




## API ENDPOINTS ##
| HTTP Method   | URI                          | Action                    |
| ------------- |:----------------------------:|--------------------------:|
| GET	          |/api/v2/requests	             |Retrieve list of requests  |  
| GET           |/api/v2/requests/[request_id] |Retrieve a request         |  
| POST          |/api/v2/requests              |Create a new request       |   
| PUT           |/api/v2/requests/[request_id] |Update an existing request |       
| DELETE        |/api/v2/requests/[request_id] |Delete an existing request |
| POST          |/api/v2/auth/signup/          |Register a user            |
| Post          |/api/v2/auth/login/           |Log in User                |

## Testing the Endpoints

1.Clone the repository `git clone https://github.com/RuthNjeri/Maintenance-Tracker-Application.git` <br>
2.Create a virtual environment `virtualenv project-env`<br>
3.Activate the virtual environment`source project-env/bin/activate` and navigate to the application root folder `/Maintenance-Tracker-Application`<br>
4.Install the requirements `pip install requirements.txt`<br>
5.Create a database named `maintenanceapp` using [postgresql](https://www.postgresql.org/)<br>
6.Run the application `python run.py`<br>
7.Test the endpoints using [Postman](https://www.getpostman.com/)

## Screenshots
# 1. Sign Up User
![sign up](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/CreateUserapi.png)
# 2. Login User
![Log in](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/SignInUser.png)
# 3. Logged in user can create a request
![POST](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/UserCreateRequest.png)
# 4. Logged in user can get all their requests
![GET](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555780/UserGetRequests.png)
# 5. Logged in user can get a specific request
![GET](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/Usergetonerequest.png)
# 6. Logged in user can edit a request
![PUT](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/UsermodifyRequest.png)
# 7. Logged in user can delete a request without a status
![DELETE](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/UserdeleteRequest.png)
# 8. An admin can view all users requests
![GET](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/admingetallrequests.png)
# 9. An admin can change status of a request
![PUT](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/adminResolveRequest.png)
![PUT](https://res.cloudinary.com/dp2m8umak/image/upload/v1528555781/requestdisapprove.png)

## UI Tasks Screenshots  ##

# 1. Sign Up Page
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/Signup_stlonp.png)
# 2. Sign In Page
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/Signin_biwjzt.png)
# 3. A Page For The Admin To View All User Requests
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/AdminViewAllReq_ihjn5f.png)
# 4. A Page Where An Admin Can Respond To All User Requests
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/AdminRespondTorequests_fnuz6m.png)
# 5. A Page For The User To View All Their Requests
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/UserViewAllRequests_izyykh.png)
# 6. A Page For The User To Create Requests
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539521/CreateRequest_dpajio.png)

### Testing using Unittest ###

1.Clone the repository `git clone https://github.com/RuthNjeri/Maintenance-Tracker-Application.git` <br>
2.Create a virtual environment `virtualenv project-env`<br>
3.Activate the virtual environment`source project-env/bin/activate` and navigate to the application root folder `/Maintenance-Tracker-Application`<br>
4.Install the requirements `pip install requirements.txt`<br>
5.Create a database named `maintenanceapp` using [postgresql](https://www.postgresql.org/)<br>
6.Test the application using the command `pytest`<br>



   
   
   
   

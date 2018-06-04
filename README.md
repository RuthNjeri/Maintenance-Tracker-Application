# Maintenance-Tracker-Application 
[![Build Status](https://travis-ci.com/RuthNjeri/Maintenance-Tracker-Application.svg?branch=develop)](https://travis-ci.com/RuthNjeri/Maintenance-Tracker-Application)

[![Maintainability](https://api.codeclimate.com/v1/badges/d144cfc546fdaac3ff35/maintainability)](https://codeclimate.com/github/RuthNjeri/Maintenance-Tracker-Application/maintainability)

![issues open](https://img.shields.io/github/issues/RuthNjeri/Maintenance-Tracker-Application.svg)

[![Coverage Status](https://coveralls.io/repos/github/RuthNjeri/Maintenance-Tracker-Application/badge.svg)](https://coveralls.io/github/RuthNjeri/Maintenance-Tracker-Application)

Provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

## API ENDPOINTS ##
| HTTP Method   | URI                          | Action                    |
| ------------- |:----------------------------:|--------------------------:|
| GET	          |/api/v1/requests	             |Retrieve list of requests  |  
| GET           |/api/v1/requests/[request_id] |Retrieve a request         |  
| POST          |/api/v1/requests              |Create a new request       |   
| PUT           |/api/v1/requests/[request_id] |Update an existing request |       
| DELETE        |/api/v1/requests/[request_id] |Delete an existing request | 

## Testing the Endpoints
Navigate inside the Maintenance-Tracker-Application folder. `cd app` folder. open the `__init__.py`. Test the endpoints using [Postman](https://www.getpostman.com/)

## Screenshots
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927992/Specificreq_txelnk.png)
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927992/newrequestcreated_enaeaq.png)
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927991/Login2_nkcuye.png)
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927991/GetNew_specific_user_request_zst783.png)
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927991/PutReq_qlalpa.png)
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927991/DeleteReq_rceurt.png)
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927991/User1_enw9uw.png)
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527927992/user2_g1zzgo.png)

## UI Tasks ##

**Sign Up Page**<br/>

1. User [signup](https://ruthnjeri.github.io/Maintenance-Tracker-Application/UI/signUp.html)<br/>  

**Sign In Page**<br/>
 
2. User [signin](https://ruthnjeri.github.io/Maintenance-Tracker-Application/UI/signIn.html)<br/>

**A Page For The Admin To View All User Requests**<br/>

3. [Admin can view all requests](https://ruthnjeri.github.io/Maintenance-Tracker-Application/UI/AdminPage.html)<br/>

**A Page Where An Admin Can Respond To All User Requests**<br/>

4. [A page where an admin](https://ruthnjeri.github.io/Maintenance-Tracker-Application/UI/AdminRespondRequests.html) can do the following:<br />
    i)   See the details of a request<br />
    ii)  Approve or disapprove a request<br />
    iii) Resolve a request<br />

**A Page For The User To View All Their Requests**<br>

5. [See all his/her requests](https://ruthnjeri.github.io/Maintenance-Tracker-Application/UI/UserRequests.html)<br />

**A Page For The User To Create Requests**<br/>

6. [Create requests](https://ruthnjeri.github.io/Maintenance-Tracker-Application/UI/createRequest.html)<br />

### Testing ###

```
   1. Clone or download the repository in the develop branch. 
   2. Navigate to the UI directory within the Maintenance-Tracker-Application folder.
   3. Right click the templates with the .html extension and open in a browser.
```
#### Screenshots ####

**Sign Up**
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/Signup_stlonp.png)

**Sign In**
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/Signin_biwjzt.png)

**User Create Request Page**
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539521/CreateRequest_dpajio.png)

**User View All Requests Page**
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/UserViewAllRequests_izyykh.png)

**Admin View all User Requests Page**
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/AdminViewAllReq_ihjn5f.png)

**Admin Respond To User Requests Page**
![](http://res.cloudinary.com/dqvk8ugtp/image/upload/v1527539522/AdminRespondTorequests_fnuz6m.png)
   
##### Testing Endpoints #####
Navigate inside the Maintenance-Tracker-Application folder.<br>
Install pytest with the command `pip install pytest` .<br>
Run the command ```python -m pytest tests/```

   
   
   
   

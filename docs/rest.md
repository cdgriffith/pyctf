REST Interface Guide
====================

User Interfaces
---------------


Interface              |  Method   |              Body                          |  Result
---------------------- | --------- | ------------------------------------------ | ----------------------
/login                 |  POST     |          user, password                    | auth_token, timeout
/user/auth_refresh     |  POST     |             auth_token                     |  refresh
/user/change_password  |  POST     |   auth_token, password, old_password       |  changed
/user/add              |  POST     |   auth_token, user, password, admin\*      | error\*
/user/remove           |  POST     |   auth_token, user                         | 

\*Not required / may not exist




Challenge Interfaces
--------------------

Interface                 |  Method   |              Body            |  Result
------------------------- | --------- | ---------------------------- | -----------------------------
/questions                |  GET      |                              |   Dict of questions by number
/questions/list           |  GET      |                              |  {data: \[list of questions\])
/question/\<question_\#\> |  GET      |                              | question, data, answer_type, media, time_limit, title, token 
/answer/<question_\#>     |  POST     |  auth_token, token, answer   | correct, score*, error*
/score                    |  POST     |        auth_token            |  score, completed
/scoreboard               |  GET      |                              |   dict of users and their scores
/scoreboard/list          |  GET      |                              | {data: \[list of (user, score)\]) 
\*Not required / may not exist


**Example question result**

```
    { 
      "question" : "Add the two numbers in the list provided in the data together",
      "data" : [2, 6],
      "answer_type" : "integer",
      "media": "/media/image.jpg",
      "time_limit": 10, 
      "title": "Example Question",
      "token": "ExampleQuestion1Token"
    }
```

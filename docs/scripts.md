Custom Question and Answer Scripts
==================================

Each question and answer can be generated then verified via external scripts.
This allows for unique challenges for each contender, however it is NOT required. 

Your custom scripts are called from a shell, allowing for to be written in any language 
the server machine can run. For example, a Java JAR file could be called like `java -jar my_custom_question.jar`. 
These scripts operate by transferring data back and forth from the server via `STDIN` and `STDOUT` in `JSON`, encoded in `utf-8`. 


Question Script
---------------

The question script once called, is simply expected to return a `JSON` string to `STDOUT` and exit cleanly within a timeout of 15 seconds.
The JSON must contain a value of 'question', which is the question that will be presented to the user; all other fields
are optional. All the fields are seen by the user exempt the 'storage' field, which is for use exclusively by the script. 

If there is any information sent to `STDERR` an exception will be raised and logged, and the user will be given an error message. 

**Example STDOUT from question script**

```json
    { 
      "question" : "Add the two numbers in the list provided in the data together",
      "data" : [2, 6],
      "answer_type" : "integer",
      "storage": "ADD"
    }
```

Field         | Type     | Description
------------- | -------- | ----------------
 question\*   | String   | The question generated for the user to provide a response to
 data         | Any      | Additional data the question can reference
 answer_type  | String   | Describe the type of response expected `boolean`, `integer`, `list`, `string` or `dictionary`
 storage      | Any      | Question specific information used to identify this question
 media        | String   | Name of additional media file in the `media` directory
 
 \* Required
 
 
 
Answer Script
-------------
 
The answer script must accept a `JSON` string via `STDIN` after execution.  The `JSON` will always contain the users answer,
the data originally sent to the user, as well as the `storage` field.

**Example STDIN to answer script**

```json
    { 
      "answer": 8,
      "data": [2, 6],
      "storage": "ADD" 
    }
```

Field     | Type     | Description
--------- | -------- | ----------------
 answer   |  Any     | The user's answer
 data     |  Any     | Additional data the question can reference
 storage  |  Any     | Question specific information used to identify the question
 
 
 After the `JSON` string is sent via `STDIN`, the answer is expected to send back a `JSON` response on `STDOUT` with a 
 single boolean field 'correct' with either `true` or `false`.
  
  
**Example `STDOUT` from answer script**

```json
    { 
      "correct": true 
    }
```

Field        | Type      | Description
------------ | --------- | ----------------
 correct\*   |  Boolean  | `true` if it is a correct answer, else `false` 
 
 \* Required
  
 
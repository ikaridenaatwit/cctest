Introduction


This project demonstrates building a Python CLI tool that interacts with a FastAPI server using different types of HTTP requests: GET, POST, Headers, Cookies, Queries, and Paths.

 Description

 
Backend built with FastAPI

Frontend CLI developed in Python

Demonstrates practical use of:

Query Parameters

Path Parameters

Cookies

Headers

Contains unit tests to verify route behavior

 Design
Modular structure with clean separation between frontend CLI and backend API

Stateless HTTP design using REST principles

Cookie and header management is built into the interaction

Test-driven development using unittest for backend


Requirements
Python 3.x

requests library (if the CLI communicates with a FastAPI or similar backend)

Install requirements with:
Instructions 

How to run 

![image](https://github.com/user-attachments/assets/6ccff914-31ea-4809-8c72-05048bf9466d)

go to cd .v 

![image](https://github.com/user-attachments/assets/177dba35-1b50-4605-80aa-34006c0a45bc)
run the uvicorn command to run the server

![image](https://github.com/user-attachments/assets/6fb09bfb-28d6-42ec-8b09-e7822d94034b)
create another terminal go to cd .v and run the command: python testing.py for unittest


![image](https://github.com/user-attachments/assets/a8718ec3-af73-495e-a7dd-af02673a691f)

go to another terminal and go to .v directory and run the command python clizpizza.py. Once you run it make sure to enter the numbers as commands. if you want to quit you can press control c or enter "q".



![image](https://github.com/user-attachments/assets/487be770-42a6-47f8-8e89-9e5b67af879a)
Command 1 : greets the user 

![image](https://github.com/user-attachments/assets/67970001-f517-4bf3-8c22-f404720a7b43)
Command 2: command where if you enter the write input given for header it will greet you as a customer 

![image](https://github.com/user-attachments/assets/41d3b727-0559-4b49-8956-c3d58d5ceb39)

Command 3: Asks the user what order would they like today 

![image](https://github.com/user-attachments/assets/bea0ecee-3289-4421-93ca-247a196c7cd9)

Command 4: A query that lets the user enter anything they want and the driver confirms the question based on what data they entered 

![image](https://github.com/user-attachments/assets/dd679025-d062-4e84-ae31-67f5df44c259)

Command 5: Enter the topping of the pizza and the cookie will save it to command 6 

![image](https://github.com/user-attachments/assets/583ee4b2-d77c-40bc-8db4-d54a57d13b5b)

Command 6: Saves the cookie from command 5 and posts it in terminal 

![image](https://github.com/user-attachments/assets/730027a5-63f0-4e7f-b4a1-d2d868c74cb8)

Command 7: A query where the user will able to input a number of the table served 

![image](https://github.com/user-attachments/assets/d56a335c-498c-41e9-9c8b-1fbab4167d8a)

Command 8: A path where user is given the choice to input the name of the pizza and as well as toppings

![image](https://github.com/user-attachments/assets/dca3eef6-68a3-4ce6-b475-93e4afbdcc7d)

Command 9: query that lets the user enter a tip and driver answers in response to that query 

![image](https://github.com/user-attachments/assets/4669d8b9-3917-4b70-89c3-2e8c97d09f12)
Command 10: driver says goodbye 










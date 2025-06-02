Adam’s Pizzeria API

A playful FastAPI service that walks a user through ordering a custom pizza at Adam’s Pizzeria.  The API demonstrates basic REST endpoints, FastAPI routing, and simple request/response logic that can be expanded into a full‑stack application.

Introduction

This project is a toy example meant for beginners learning FastAPI.  It exposes readable, self‑documenting endpoints (thanks to Swagger UI) so you can explore HTTP interactions without writing any front‑end code.

Instructions to Run the Project

1. Prerequisites

Python 3.8 +

pip (or pipx / Poetry / Hatch – use what you like)

2. Set up a virtual environment (optional but recommended)

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

3. Install dependencies

pip install fastapi uvicorn

4. Start the development server

uvicorn main:app --reload

Assuming you saved the code above as main.py.  The --reload flag auto‑restarts on file changes – perfect for rapid tweaking.

5. Explore the API

Open http://127.0.0.1:8000/docs in your browser.  FastAPI will display an interactive Swagger UI where you can call each endpoint.

Project Description

![image](https://github.com/user-attachments/assets/9f724ed0-680f-40c2-be85-85fba320bfb1)

Summary: simple strings for users to interact with the website

![image](https://github.com/user-attachments/assets/1a6628bf-345c-4422-9c87-a405504692b9)

Creates a text asking the user what would you like today

![image](https://github.com/user-attachments/assets/8511f1ab-0592-4a68-b530-02e70334d29b)

Creates a text for the user to enter an input text by creating a variable names any pizza by inputting ?pizza=Pepperoni after /PizzaQuestion. This has to be only a string though nothing else.

![image](https://github.com/user-attachments/assets/4325f37c-40d6-4d01-8ba9-a3009b953d0b)

Asks the user in text what would the user like

![image](https://github.com/user-attachments/assets/2f3dd78f-bf84-4191-98c5-6b734ce38273)

This webpage asks what type of pizza would you like. If you type in specific answers such as "Pepperoni", "Cheese", and "Pineapple"; it would have a specific response to that question. This can be done as previously doing ?pizza=Pepperoni.

![image](https://github.com/user-attachments/assets/77cfa271-955a-4626-ae55-44fd8f451d41)

The next webpage asks the user for toppings and it is as before on the previous webpage but instead of using the variable pizza you have to use another variable called toppings. There will be specific responses based on what type of string you inserted. If you type in "Olives", "Beef", or "Chicken" ; the webpage will respond by saying it has it and will cook one right up. If you put anything else, it will respond by saying it does not have that specific topping.

![image](https://github.com/user-attachments/assets/06e6f74e-b155-466e-bfc9-43f56d866536)

Put a number by doing ?tablenumber = 0. The value must be greater than or equal to zero otherwise it will say Internal Server Error.

![image](https://github.com/user-attachments/assets/7e5176cd-151b-44fd-bdc3-65ebbb8a0a09)

This is a query so you have to input the values for variables example: http://127.0.0.1:8080/Confirmation/pepperoni/olives/5

![image](https://github.com/user-attachments/assets/7d3ae9ff-fafb-44fd-a639-cedea2e55a14)

greets the user goodbye

![image](https://github.com/user-attachments/assets/38a53b18-8fe7-4e7e-af60-1cc63970d7f3)





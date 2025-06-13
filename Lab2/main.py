from typing import Optional
from enum import Enum
from fastapi import FastAPI, Header, Response, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# A set of valid customer IDs for demonstration
customer_ids = { "Jake123", "Sam3456", "Larry987" }

# List of available pizza toppings
pizza_options = ['pepperoni', 'cheese', 'mushrooms', 'pineapple']

app = FastAPI()

@app.get("/")
async def read_root():
    """
    The root endpoint providing a welcome message.
    """
    return "Hello, my name is Adam and welcome to Adam's Pizzeria!"

@app.get("/Greetingscustomer")
async def customer_greeting(customer_id_confirm: str = Header(...)):
    """
    Welcomes a returning customer by validating their ID from the request header.
    Returns a 401 Unauthorized error if the customer ID is not valid.
    """
    if customer_id_confirm not in customer_ids:
        # Instead of raising an exception, return a JSONResponse with the error
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: Invalid Customer"}
        )
    
    # Return a success message if the customer ID is valid
    return {"message": f"Welcome {customer_id_confirm}! Haven't seen you in a while. Here is your ID: {customer_id_confirm}"}

@app.get("/PizzaConversation")
async def create_message():
    return "What would you like today?"

@app.get("/PizzaQuestion")
async def current_messages(pizza: str):
    return f"Do you want {pizza}?"

@app.get("/Pizza")
async def pizzaoptions():
    return "What pizza would you like?"

@app.post("/Choose/{topping}")
async def choose_topping(topping: str, response: Response):
    """
    Sets a 'favorite_topping' cookie based on the user's choice.
    Returns a 400 Bad Request error if the topping is not a valid option.
    """
    if topping.lower() not in pizza_options:
        # Return a JSONResponse for an invalid topping choice
        return JSONResponse(
            status_code=400,
            content={"detail": f"Invalid topping. Please choose one of: {', '.join(pizza_options)}"}
        )

    # Set the cookie in the user's browser on success
    response.set_cookie(key="favorite_topping", value=topping.lower(), httponly=True)
    return {"message": f"Success! Your favorite topping, '{topping}', has been saved."}

@app.get("/PizzaOptions")
async def pizzasuggestion(favorite_topping: Optional[str] = Cookie(None)):
    """
    Reads the 'favorite_topping' cookie and provides a suggestion.
    """
    if not favorite_topping:
        return "You haven't set a favorite topping yet! Use the 'Set favorite topping' option first."
    
    if favorite_topping in pizza_options:
         # Capitalize for a nicer message
        return f"Ah, {favorite_topping.capitalize()}! Coming right up!"
    
    # This case is unlikely if the cookie is set by our endpoint, but it is good practice
    return "We don't recognize your favorite topping."

@app.get("/SeatConfirmation")
async def table_options(tablenumber: int):
    if tablenumber >= 0:
        return f'Alright, it seems table {tablenumber} is available. Please take a seat.'
    else:
        return "That's not a valid table number. Please choose a positive number."

@app.get("/Confirmation/{pizza}/{toppings}")
async def order_served(pizza:str, toppings: str):
    return f"Here is your {pizza} with {toppings}. Enjoy!"

@app.get("/tip")
async def tip(tip: float):
    return f"Oh wow, you gave me ${tip:.2f}! That's generous. Thank you!"

@app.get("/goodbye")
async def greetingbye():
    return "Goodbye! Have a great day!"
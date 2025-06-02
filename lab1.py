from enum import Enum
from fastapi import FastAPI, Request
from pydantic import BaseModel




app = FastAPI()


pizza_options = ['pepperoni','cheese','mushrooms','pineapple']

@app.get("/Greetings")
async def read_root():
    return f"Hello my name is Adam and Welcome to Adam's Pizzeria!"

@app.get("/PizzaConversation")

async def create_message():
    return f"What Would you like today?"


@app.get("/PizzaQuestion")
async def current_messages(pizza: str):
    return f"Do you want {pizza}?"



@app.get("/Pizza")
async def pizzaoptions():
    return f"What pizza would you like?"

@app.get("/PizzaOptions")

async def pizzasuggestion(pizza: str):
    if pizza == "Pepperoni":
        return f"Pepperoni? That's a Classic! Excellent Choice"
    elif pizza == "Cheese":
        return f"Cheese? Nice! Plain Pizza is the way to go!"
    elif pizza == "Pineapple":
        return f"Pineaple?... Well Alright I guess that's what the customer wants."
    
    else:
        return f"Sorry we don't have {pizza} in our Menu"
    
@app.get("/ListOptions")

async def pizza_additional(toppings: str ):
    if toppings == "Olives":
        return f"Olives? Great I will add some Olives then"
    if toppings == "Beef":
        return f"Beef? Great I will add some Beef then"
    if toppings == "Chicken":
        return f"Chicken? Great I will add some chicken then"
    
    else:
        return f"Sorry We don't have any {toppings}"


@app.get("/SeatConfirmation")

async def table_options(tablenumber: int):
    if tablenumber>=0:
        return f'Alright it seems table {tablenumber} is available take a seat'
    
@app.get("/Confirmation/{pizza}/{toppings}/{tablenumber}")

async def order_served(pizza:str,toppings: str, tablenumber: int):
    return f"Here is {pizza} with {toppings}"

@app.get("/tip")
async def tip(tip : float):
    return f"Oh wow you gave me {tip} that's generous! Thank you!"

@app.get("/goodbye")

async def greetingbye():
    return f"Goodbye Customer have a good day!"



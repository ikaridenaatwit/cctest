Adam’s Pizzeria API

A playful FastAPI service that walks a user through ordering a custom pizza at Adam’s Pizzeria.  The API demonstrates basic REST endpoints, FastAPI routing, and simple request/response logic that can be expanded into a full‑stack application.

📜 Introduction

This project is a toy example meant for beginners learning FastAPI.  It exposes readable, self‑documenting endpoints (thanks to Swagger UI) so you can explore HTTP interactions without writing any front‑end code.

✨ Project Description

Route

Purpose

GET /Greetings

Welcome message

GET /PizzaConversation

Asks what the customer would like

GET /PizzaQuestion?pizza=…

Confirms the pizza choice

GET /Pizza

Prompts for the exact pizza type

GET /PizzaOptions?pizza=…

Responds with praise or apology based on menu

GET /ListOptions?toppings=…

Handles extra toppings

GET /SeatConfirmation?tablenumber=…

Checks if a table is available

GET /Confirmation/{pizza}/{toppings}/{tablenumber}

Final order served

GET /tip?tip=…

Thanks the customer for a tip

![image](https://github.com/user-attachments/assets/81f28b5b-fd17-4e31-825b-debe65dba738)


GET /goodbye

Says farewell

All responses are simple strings so you can focus on request flow rather than payload structure.

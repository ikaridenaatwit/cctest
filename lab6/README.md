

Lab6

<img width="975" height="380" alt="image" src="https://github.com/user-attachments/assets/6da0a777-a81e-45d4-ad68-e3d9209bf881" />


Build the docker 

<img width="975" height="215" alt="image" src="https://github.com/user-attachments/assets/df450e30-d74d-4a28-a65c-4fec36bcae66" />

Run the docker




<img width="975" height="215" alt="image" src="https://github.com/user-attachments/assets/f5143e98-66e7-40db-9c3a-e308923ef3e6" />


Execution of lab5.py

Query
 <img width="866" height="522" alt="image" src="https://github.com/user-attachments/assets/bff5122c-de66-4093-aba1-fc968682c806" />
1
Get all product names and prices
Lists each product’s product_name and list_price. Helps you see your catalog quickly.
 <img width="836" height="488" alt="image" src="https://github.com/user-attachments/assets/d89434d2-c225-4ddf-9606-11fdad2c837d" />
2
Get all customer names
Shows each customer’s first and last name. (Notice first_name can contain spaces like “Frank Lee”.)
<img width="658" height="405" alt="image" src="https://github.com/user-attachments/assets/7c452ff4-021f-4249-bcca-f35666bdd879" />
3
List category names
Simple look at available product categories.

 <img width="786" height="525" alt="image" src="https://github.com/user-attachments/assets/ce04a509-2415-4261-b875-290c982a62d4" />

4
Get all order IDs and dates
All orders with their timestamps. Order 10 has NULL (None) order_date, which often means “cart started / not finalized.”

<img width="809" height="602" alt="image" src="https://github.com/user-attachments/assets/35168d3a-5506-4602-acf7-f384a5309918" />
5
Get emails from administrators
Pulls admin user emails (e.g., for access or seed data checks).




 



 

Inner Joins

 <img width="850" height="530" alt="image" src="https://github.com/user-attachments/assets/73663c9a-a5d5-480a-a5d5-4dc31e2c7a5e" />
 
 1
 Products and their categories
Verifies each product is mapped to a category and shows the category name.
 <img width="839" height="530" alt="image" src="https://github.com/user-attachments/assets/d298fba3-f652-4a9e-aa5d-41d63c85023a" />
 2
 Customers and their order dates
One row per order per customer. None dates indicate not-finalized orders. Repeats a customer if they made multiple orders.
 <img width="922" height="622" alt="image" src="https://github.com/user-attachments/assets/3cb4881a-5222-4fe3-95b2-c876089d22f1" />
 3
 Product names and quantity ordered
Every line item from every order: which product and how many units.
 <img width="941" height="506" alt="image" src="https://github.com/user-attachments/assets/a29323f8-8b66-47ae-8832-13220e4622a1" />
 4
 Order IDs and their shipping address line
Shows where each order ships. Order 10 shows line1 = "superman@gmail.com", pointing to the address data issue mentioned earlier.
 <img width="908" height="619" alt="image" src="https://github.com/user-attachments/assets/66674872-2361-4e32-8d18-791204cf258c" />
 5
 Customers and their city
Customers can appear multiple times if they have multiple addresses (e.g., billing + shipping) or multiple address records.





 
 
 
 

Queries with functionos or group by

<img width="975" height="285" alt="image" src="https://github.com/user-attachments/assets/14d82bb6-a148-499e-bd4d-400afba83cd7" />

1
Count of products in each category ID
How many products per category.

<img width="850" height="534" alt="image" src="https://github.com/user-attachments/assets/83796b42-8a15-468e-b35d-078849c4b2b7" />
2
Sum of item prices for each order
Subtotal per order by summing line item_price.
<img width="858" height="244" alt="image" src="https://github.com/user-attachments/assets/02b211bb-81df-4c4f-90df-df3c0650b169" />
3
Average price of all products
<img width="883" height="259" alt="image" src="https://github.com/user-attachments/assets/e75768da-00ea-458e-b059-83b4b68b332a" />
4
Cheapest and most expensive products
Min and max list prices across the catalog.
<img width="938" height="213" alt="image" src="https://github.com/user-attachments/assets/535b846b-6772-4a1b-ae83-9e9a65a45b02" />
5
The single most expensive product
Top-priced item with its name.







 
 
 
 
 


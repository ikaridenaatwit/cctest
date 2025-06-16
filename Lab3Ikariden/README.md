Install dependencies
bash
Copy
Edit
npm install
3. Start the server
bash
Copy
Edit
node server.js

Description of each route

HTML Content Routes 
![image](https://github.com/user-attachments/assets/57fbd18b-2495-4a70-8acd-54816c0c009d)




Query Routes

GET	/	company	Returns a greeting like "Hello, [company]!" or "Hello world" if none given.
GET	/specials	term	Returns JSON: { youSearchedFor: [term] }.
GET	/seat	table	Placeholder route. Accepts table value but does nothing with it yet.
GET	/order	pizza, quantity	Returns order summary like "Serving 2 Pepperoni pizzas".
GET	/add-topping	topping	Returns confirmation message like "Extra olives added".

BodyInput Route Route

![image](https://github.com/user-attachments/assets/f9360442-f717-4a00-93de-937cb28599cc)


Header Route

![image](https://github.com/user-attachments/assets/8a883eee-8466-4414-b72e-06aff4fd7905)


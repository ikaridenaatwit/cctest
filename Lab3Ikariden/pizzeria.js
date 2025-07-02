// first reference required modules
const fs = require('fs');
const path = require('path');
const express = require('express');
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true}));
let port = 8080;

const jsonPath = path.join(__dirname, 'public', 'testing.json');
// get data using conventional Node callback approach
let companies = "Hello world";

let discount_question = "Do you have a discount before I take your order?"
let commentesting = "Testing Testing!";

let pizzaList = [
    { id: 1, name: "Margherita", toppings: ["Tomato Sauce", "Mozzarella", "Basil"] },
    { id: 2, name: "Pepperoni", toppings: ["Tomato Sauce", "Mozzarella", "Pepperoni"] },
    { id: 3, name: "Hawaiian", toppings: ["Tomato Sauce", "Mozzarella", "Ham", "Pineapple"] },
    { id: 4, name: "Veggie Supreme", toppings: ["Tomato Sauce", "Mozzarella", "Onions", "Peppers", "Olives", "Mushrooms"] }
];

let tip_question = "Did you enjoy the service? A tip for the staff is always appreciated!";

app.get('/welcome', (req, res) => {
    res.send('<h1>Welcome to our Pizzeria!</h1><p>The best pizza in town.</p>');
});

app.get('/question', (req, res) => {
    res.send('<h1>We only order pizza what would you like today?</h1>')
});

app.get('/specials', (req, res) => {
    const { term } = req.query;
     res.json({ youSearchedFor: term || null });
});

app.get('/askingtable', (req, res) => {
    res.send('<h1>Which table would you like to be seated sir?</h1>')
})
app.get('/seat', (req, res) => {
    const {table} = req.query;

    res.send(`Confirmation: You have been assigned to table number ${table}`);

})

app.get('/pizzas', (req, res) => res.json(pizzaList));
//body input

app.post('/pizzas', (req, res) => {
  const { name, toppings } = req.body;   



  const newPizza = {
    id: pizzaList.length + 1,
    name,
    toppings
  };

  pizzaList.push(newPizza);              
  res.status(201).json(newPizza);        
});
app.get('/tipquestion', (req, res) => {
    res.json(tip_question);
});
//(tip)
app.get('/tip/:amount', (req, res) => {
    const tipAmount = req.params.amount;
    
    if (isNaN(tipAmount)) {
        res.status(400).send("That's not a valid number! Please provide a numerical tip amount.");
    } else {
        res.send(`Thank you for your generous tip of $${tipAmount}!`);
    }
});

app.get('/orderserved', (req, res) => {
    res.send('<h1>Here is your order</h1>')

});

app.get('/order', (req, res) => {
  const { pizza, quantity = 1 } = req.query;
  if (!pizza) return res.status(400).send('Specify a pizza type');
  res.json({ order: `Serving ${quantity} ${pizza} pizza${quantity > 1 ? 's' : ''}` });
});

app.get('/add-topping', (req, res) => {
  const { topping } = req.query;
  if (!topping) return res.status(400).send('Specify a topping');
  res.json({ confirmation: `Extra ${topping} added` });
});

// curl -H "customer123: VIP-Member-456" http://localhost:8080/valued_customer using git

app.get('/valued_customer', (req, res) => {
  const customHeader = req.headers['customer123'];

  if (!customHeader) {
    return res.status(400).send('Missing required header: customHeader');
  }

  res.send(`Hello Valued Customer:  ${customHeader}`);
});



app.get('/goodbye', (req, res) => {

    res.send('<h1>Thank you and come again!</h1>')

});



app.use(express.json());


app.listen(port, () => {
console.log("Server running at port= " + port);
});


import unittest
from fastapi.testclient import TestClient
from main import app 

class TestPizzeriaApp(unittest.TestCase):

    def setUp(self):
        
        self.client = TestClient(app)

    def test_read_root(self):
        
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.text, '"Hello, my name is Adam and welcome to Adam\'s Pizzeria!"')

    def test_welcome_customer_success(self):
       
        headers = {"customer-id-confirm": "Jake123"}
        response = self.client.get("/Greetingscustomer", headers=headers)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.json(), {
            "message": "Welcome Jake123! Haven't seen you in a while. Here is your ID: Jake123"
        })

    def test_welcome_customer_unauthorized(self):
        
        headers = {"customer-id-confirm": "UnknownPerson"}
        response = self.client.get("/Greetingscustomer", headers=headers)
        self.assertEqual(response.status_code, 401)
       
        self.assertEqual(response.json(), {"detail": "Unauthorized: Invalid Customer"})

    def test_set_favorite_topping_cookie_success(self):
        
        response = self.client.post("/Choose/pepperoni")
        self.assertEqual(response.status_code, 200)
        self.assertIn("favorite_topping", response.cookies)
        self.assertEqual(response.cookies["favorite_topping"], "pepperoni")
        self.assertEqual(response.json(), {"message": "Success! Your favorite topping, 'pepperoni', has been saved."})

    def test_set_favorite_topping_cookie_invalid(self):
     
        response = self.client.post("/Choose/anchovies")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid topping", response.json()["detail"])

    def test_get_suggestion_with_cookie(self):
      
        cookies = {"favorite_topping": "mushrooms"}
       
        response = self.client.get("/PizzaOptions", cookies=cookies)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.text, '"Ah, Mushrooms! Coming right up!"')
    
    def test_get_suggestion_without_cookie(self):
       
        response = self.client.get("/PizzaOptions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"You haven\'t set a favorite topping yet! Use the \'Set favorite topping\' option first."')

    def test_confirm_table_success(self):
        
        response = self.client.get("/SeatConfirmation?tablenumber=12")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"Alright, it seems table 12 is available. Please take a seat."')
        
    def test_confirm_table_failure_with_negative_number(self):
       
        response = self.client.get("/SeatConfirmation?tablenumber=-1")
     
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.text, '"That\'s not a valid table number. Please choose a positive number."')

    def test_leave_tip(self):
       
        response = self.client.get("/tip?tip=10.50")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"Oh wow, you gave me $10.50! That\'s generous. Thank you!"')

    def test_say_goodbye(self):
       
        response = self.client.get("/goodbye")
        self.assertEqual(response.status_code, 200)
       
        self.assertEqual(response.text, '"Goodbye! Have a great day!"')
        
if __name__ == '__main__':
    unittest.main()
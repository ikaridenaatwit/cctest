import requests
import sys

# The address of our running FastAPI server
# FIX 1: Changed port from 8080 to 8000, which is the default for FastAPI.
BASE_URL = "http://127.0.0.1:8000"

def print_menu():
    """Prints the main menu of options to the console."""
    print("\n--- Adam's Pizzeria Interactive CLI ---")
    print("1. Get root greeting")
    print("2. Welcome a returning customer (uses Header)")
    print("3. What would you like today? (Start order)")
    print("4. Ask about a pizza (uses Query Param)")
    print("5. Set favorite topping (sets Cookie with POST)")
    print("6. Get topping suggestion (reads Cookie)")
    print("7. Confirm table (uses Query Param)")
    print("8. Place final order (uses Path Params)")
    print("9. Leave a tip (uses Query Param)")
    print("10. Say goodbye")
    print("q. Quit")
    print("---------------------------------------")

def handle_response(response):
    
    if response.ok: 
        print(f"\n SUCCESS (Status Code: {response.status_code})")
        try:
            
            json_response = response.json()
            
            if isinstance(json_response, dict):
                for key, value in json_response.items():
                    print(f"  {key.capitalize()}: {value}")
            else:
                
                print(f"  Server says: {json_response}")
        except requests.exceptions.JSONDecodeError:
            
            
            print(f"  Server says: {response.text.strip('\"')}")
    else:
        
        print(f"\n ERROR (Status Code: {response.status_code})")
        try:
            
            print(f"  Details: {response.json().get('detail', 'No details provided.')}")
        except requests.exceptions.JSONDecodeError:
            
            print(f"  Details: {response.text}")

def main():
    """The main function to run the interactive loop."""
    
    session = requests.Session()
    
    while True:
        print_menu()
        choice = input("Enter your choice: ").lower().strip()

        if not choice:
            continue

        res = None 
        try:
            if choice == '1':
                res = session.get(f"{BASE_URL}/")
            
            elif choice == '2':
                customer_id = input("Enter customer ID (e.g., Jake123, Sam3456): ")
                headers = {"customer-id-confirm": customer_id}
                res = session.get(f"{BASE_URL}/Greetingscustomer", headers=headers)

            elif choice == '3':
                res = session.get(f"{BASE_URL}/PizzaConversation")

            elif choice == '4':
                pizza_name = input("What pizza are you curious about? (e.g., margherita): ")
                res = session.get(f"{BASE_URL}/PizzaQuestion", params={"pizza": pizza_name})
            
            elif choice == '5':
                topping = input("Enter your favorite topping to save (e.g., pepperoni, pineapple): ")
                res = session.post(f"{BASE_URL}/Choose/{topping}")
            
            elif choice == '6':
                res = session.get(f"{BASE_URL}/PizzaOptions")
            
            elif choice == '7':
                try:
                    table_str = input("What table number would you like? ")
                    table = int(table_str)
                    res = session.get(f"{BASE_URL}/SeatConfirmation", params={"tablenumber": table})
                except ValueError:
                    print("\n Invalid input. Please enter a whole number for the table.")

            elif choice == '8':
                pizza = input("What is the name of the pizza you're ordering? ")
                toppings = input("What toppings would you like on it? ")
                res = session.get(f"{BASE_URL}/Confirmation/{pizza}/{toppings}")

            elif choice == '9':
                try:
                    amount_str = input("How much would you like to tip? $")
                    amount = float(amount_str)
                    res = session.get(f"{BASE_URL}/tip", params={"tip": amount})
                except ValueError:
                    print("\n Invalid input. Please enter a number for the tip amount.")

            elif choice == '10':
                res = session.get(f"{BASE_URL}/goodbye")

            elif choice == 'q':
                print("\nThank you for using the Pizzeria CLI. Goodbye!")
                break
            
            else:
                print("\n Invalid choice, please try again.")

            
            if res:
                handle_response(res)

        except requests.exceptions.RequestException:
            print(f"\ Could not connect to the API server.")
            print(f"Please ensure your FastAPI app is running on {BASE_URL}")
            sys.exit()

        
        if choice != 'q':
             input("\n--- Press Enter to continue ---")


if __name__ == "__main__":
    main()
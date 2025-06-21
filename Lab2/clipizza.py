import requests
import sys


BASE_URL = "http://127.0.0.1:8080"

def print_menu():
    """Prints the main menu of options to the console."""
    print("\n--- Adam's Pizzeria Interactive CLI ---")
    print("1. Get root greeting")
    print("2. Welcome a returning customer (header) ")
    print("3. What would you like today? (Start order)")
    print("4. Ask about a pizza (Query)")
    print("5. Set favorite topping (sets Cookie with POST)")
    print("6. Get topping suggestion (reads Cookie)")
    print("7. Confirm table (Query)")
    print("8. Place final order (uses Path)")
    print("9. Leave a tip (Query)")
    print("10. Say goodbye")
    print("q. Quit")
    print("---------------------------------------")

def handle_response(response):
    if response.ok:
        
        try:
            json_response = response.json()
            if isinstance(json_response, dict):
                for key, value in json_response.items():
                    print(f"  {key.capitalize()}: {value}")
            else:
                print(f"  Server says: {json_response}")
        except Exception:
            print(f"  Server says: {response.text}")
    else:
        
        try:
            json_response = response.json()
            # Print all key/value pairs in JSON error
            for key, value in json_response.items():
                print(f"  {key.capitalize()}: {value}")
        except Exception:
            print(f"  Details: {response.text}")

def main():
    
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
                if not customer_id:
                    print("\nCustomer ID cannot be empty. Please try again.")
                    continue
                
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
            print(f"\nCould not connect to the API server.")
            print(f"Please ensure your FastAPI app is running on {BASE_URL}")
            sys.exit()

        if choice != 'q':
             input("\n--- Press Enter to continue ---")


if __name__ == "__main__":
    main()

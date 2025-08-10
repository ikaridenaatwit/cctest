import mysql.connector
from mysql.connector import Error
def connect_to_db():
    try:
        mydb = mysql.connector.connect(
            host="lease-link.cq7iaykk4axi.us-east-1.rds.amazonaws.com",
            user="LeaseLinkadmin",
            password="leaselinkadmin",
            database="my_guitar_shop"
        )
        print("Successfully connected to MySQL database!")

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

    return mydb

def query_addresses(mydb):
    """
    Queries the database for all addresses and prints them.
    Assumes 'mydb' is an active database connection object.
    """
    mycursor = None  # Initialize cursor to None
    try:
        # Create a cursor object from the provided connection
        mycursor = mydb.cursor()

        # Define the SQL SELECT query
        sql_query = "SELECT address_id, line1 FROM addresses"

        # Execute the query
        mycursor.execute(sql_query)

        # Fetch all the results
        results = mycursor.fetchall()

        # Iterate through the fetched results and print them
        print("\n--- Querying All Addresses ---")
        for row in results:
            print(f"Address ID: {row[0]}, Line 1: {row[1]}")

    except mysql.connector.Error as err:
        print(f"Error during address query: {err}")

    finally:
        # Ensure the cursor is always closed to free up resources
        if mycursor:
            mycursor.close()
   

def execute_and_print_query(mydb, sql_query, title):
    """
    Executes a given SQL query and prints the results.
    - mydb: The active database connection object.
    - sql_query: The SQL query string to execute.
    - title: A descriptive title for the query.
    """
    if not mydb or not mydb.is_connected():
        print("Database connection is not active. Cannot execute query.")
        return

    mycursor = None
    try:
        # Using a dictionary cursor makes accessing columns by name easy
        mycursor = mydb.cursor(dictionary=True)

        print("\n" + "="*50)
        print(f"EXECUTING QUERY: {title}")
        print("="*50)
        
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        if results:
            # Print table headers from the keys of the first result row
            headers = results[0].keys()
            print(" | ".join(f"{h:<25}" for h in headers))
            print("-" * (28 * len(headers)))

            # Print each row of data
            for row in results:
                print(" | ".join(f"{str(v):<25}" for v in row.values()))
        else:
            print("No results returned for this query.")

    except Error as err:
        print(f"Error executing query: {err}")
    finally:
        # Close the cursor after we are done with it
        if mycursor:
            mycursor.close()


def main():
    mydb = connect_to_db()
    query_addresses(mydb)

    if mydb is None:
        return
    try:
        print("\n\n--- 5 Simple Single Table Queries ---")
        execute_and_print_query(mydb, "SELECT product_name, list_price FROM products;", "1. Get all product names and prices")
        execute_and_print_query(mydb, "SELECT first_name, last_name FROM customers;", "2. Get all customer names")
        execute_and_print_query(mydb, "SELECT category_name FROM categories;", "3. List category names")
        execute_and_print_query(mydb, "SELECT order_id, order_date FROM orders;", "4. Get all order IDs and dates")
        execute_and_print_query(mydb, "SELECT email_address FROM administrators;", "5. Get emails from administrators")
        
        print("\n\n--- Running Queries with Inner Joins ---")
        execute_and_print_query(mydb, "SELECT products.product_name, categories.category_name FROM products JOIN categories ON products.category_id = categories.category_id;", "1. Products and their categories")
        execute_and_print_query(mydb, "SELECT customers.first_name, orders.order_date FROM customers JOIN orders ON customers.customer_id = orders.customer_id;", "2. Customers and their order dates")
        execute_and_print_query(mydb, "SELECT products.product_name, order_items.quantity FROM products JOIN order_items ON products.product_id = order_items.product_id;", "3. Product names and quantity ordered")
        execute_and_print_query(mydb, "SELECT orders.order_id, addresses.line1 FROM orders JOIN addresses ON orders.ship_address_id = addresses.address_id;", "4. Order IDs and their shipping address line")
        execute_and_print_query(mydb, "SELECT customers.first_name, addresses.city FROM customers JOIN addresses ON customers.customer_id = addresses.customer_id;", "5. Customers and their city")

        
        print("\n\n--- Running Queries with Functions or GROUP BY ---")
        execute_and_print_query(mydb, "SELECT category_id, COUNT(*) FROM products GROUP BY category_id;", "1. Count of products in each category ID")
        execute_and_print_query(mydb, "SELECT order_id, SUM(item_price) FROM order_items GROUP BY order_id;", "2. Sum of item prices for each order")
        execute_and_print_query(mydb, "SELECT AVG(list_price) FROM products;", "3. Average price of all products")
        execute_and_print_query(mydb, "SELECT MIN(list_price) AS cheapest_product, MAX(list_price) AS priciest_product FROM products;", "4. Cheapest and most expensive products")
        execute_and_print_query(mydb, "SELECT product_name, list_price FROM products ORDER BY list_price DESC LIMIT 1;", "5. The single most expensive product")

    except Error as err:
        print(f"Error executing query: {err}")
    

main()
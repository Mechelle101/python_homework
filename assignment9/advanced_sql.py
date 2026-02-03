
import sqlite3

# Task 1: Complex Join with Aggregation
query = """
SELECT o.order_id,
        SUM(p.price * li.quantity) AS total_price
FROM orders o
JOIN line_items li ON o.order_id = li.order_id
JOIN products p ON li.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5;
"""

with sqlite3.connect('../db/lesson.db') as conn:
  cursor = conn.cursor()
  cursor.execute(query)
  rows = cursor.fetchall()
  
print("Order Id Total Price")
for order_id, total_price in rows:
  print(f"{order_id} \t {total_price }")

# Task 2: Understanding Subqueries
query_task_2 = """
SELECT c.customer_name,
  AVG(sub.total_price) AS average_total_price
FROM customers c 
  LEFT JOIN (
  SELECT o.customer_id AS customer_id_b,
    SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
  GROUP BY o.order_id
  ) sub
ON c.customer_id = sub.customer_id_b
GROUP BY c.customer_id;
"""

with sqlite3.connect('../db/lesson.db') as conn:
  cursor = conn.cursor()
  cursor.execute(query_task_2)
  rows = cursor.fetchall()
  
print("\nTask 2 Results")
for customer_name, average_total_price in rows:
  print(f"{customer_name} : {average_total_price }")
print()
  
# Task 3: Insert Transaction Based on Data
def task_3():
  with sqlite3.connect('../db/lesson.db') as conn:
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    
    try:
      # Get customer id for 'Perez and Sons'
      cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_name = ?;",
        ("Perez and Sons",)
      )
      # Extracting the value from the tuple so you can use it later
      customer_id = cursor.fetchone()[0]
      
      # Get employee id for 'Miranda Harris'
      cursor.execute(
        """
        SELECT employee_id
        FROM employees
        WHERE first_name = ? 
        AND last_name = ?;        
        """, 
        ("Miranda", "Harris")
      )
      # Extracting the value from the tuple so you can use it later
      employee_id = cursor.fetchone()[0]
      
      # Get product ids for the 5 least expensive products
      cursor.execute(
        "SELECT product_id FROM products ORDER BY price ASC LIMIT 5;"
      )
      product_ids = [row[0] for row in cursor.fetchall()]
      
      # Insert the order and capture order_id
      cursor.execute(
        """
        INSERT INTO orders (customer_id, employee_id, date)
        VALUES (?, ?, DATE('now'))
        RETURNING order_id;
        """,
        (customer_id, employee_id)
      )
      # Extracting the value from the tuple so you can use it later
      order_id = cursor.fetchone()[0]
      
      # Insert 5 line_items (10 of each product)
      for product_id in product_ids:
        cursor.execute(
          """
          INSERT INTO line_items (order_id, product_id, quantity)
          VALUES (?, ?, ?);
          """,
          (order_id, product_id, 10)
        )
        
      # Verify the inserted data
      cursor.execute(
        """
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?
        ORDER BY li.line_item_id;
        """,
        (order_id,)
      )
      results = cursor.fetchall()
      
      # Commit everything as one transaction
      conn.commit()
      
    except Exception:
      # Just in case something fails, "atomicity"
      conn.rollback()
      raise
    
  print("\nTask 3 Results")
  print("New order id: ", order_id)
  for line_item_id, quantity, product_name in results:
    print(f"{line_item_id} \t {quantity} \t {product_name }")
      
# Comment out the function so it doesn't get run while working on task 4
# task_3()
print("This is where Task 3 would be executed.")

# Task 4: Aggregation with HAVING
query_task_4 = """
SELECT e.employee_id,
       e.first_name,
       e.last_name,
       COUNT(o.order_id) AS order_count
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC, e.employee_id;
"""

with sqlite3.connect('../db/lesson.db') as conn:
  cursor = conn.cursor()
  cursor.execute(query_task_4)
  rows = cursor.fetchall()
  
  print("\nTask 4 Results (Employees with more than 5 orders)")
  for employee_id, first_name, last_name, order_count in rows:
    print(f"{employee_id} \t {first_name} \t {last_name} \t {order_count }")
    
  
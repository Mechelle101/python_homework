import sqlite3
import pandas as pd

# ----------------------------------
# Task 5: Read data into a dataframe
# ----------------------------------

try:
  with sqlite3.connect("../db/lesson.db") as conn:
    cursor = conn.cursor()
    
    # 1) Reading data into a DF
    try:
      sql_stmt = """
        SELECT
          li.line_item_id,
          li.quantity,
          p.product_id,
          p.product_name,
          p.price
          FROM line_items li
          JOIN products p ON li.product_id = p.product_id;
      """
      df = pd.read_sql_query(sql_stmt, conn)
    except sqlite3.Error as e:
      print("Error reading data into DataFrame", e)
      
    # Print the first 5 lines
    print("-----Task 5.1: Printing first 5 lines of DataFrame-----")
    print(df.head())
    print()
    
    # 2) Add a total column (qty * price)
    df['total'] = df['quantity'] * df['price']
    
    # Print the first five lines
    print("-----Task 5.2: DataFrame with Total Column-----")
    print(df.head())
    print()
    
    # Task 5.3: Group by product id
    summary_df = df.groupby("product_id").agg({
      "line_item_id": "count",
      "total": "sum",
      "product_name": "first"
    })
    
    # Print first 5 lines
    print("-----Task 5.3: Grouped summary -----")
    print(summary_df.head())
    print()
    
    # Task 5.4 Sort by product name
    summary_df = summary_df.sort_values(by="product_name")
    print("-----Task 5.4: Sorting by product name -----")
    print(summary_df.head())
    print()
    
    # Task 5.5: Write the DF to order_summary.csv
    summary_df.to_csv("order_summary.csv")
    
    print("order_summary.csv written successfully.")
    
except sqlite3.Error as e:
  print("Error connecting to database", e)
  
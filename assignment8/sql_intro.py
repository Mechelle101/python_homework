import sqlite3

#  Task 3: Functions
# Each function inserts into one table.
# - prevents duplication
# - handles exceptions
# - returns the PK for the row it inserted
"""
Insert a publisher if it does not exist.
Publishers have. unique not null name.
If publisher with this name already exists do not insert again
"""
def add_publisher(cursor, publisher_name):
  try:
    cursor.execute("SELECT publisher_id FROM Publishers WHERE name = ?", (publisher_name,))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error checking existing publisher", e)
    return None
    
  if len(result) > 0:
    return result[0][0]
  
  try:
    cursor.execute("INSERT INTO Publishers (name) VALUES (?)", (publisher_name,))
  except sqlite3.Error as e:
    print("Error inserting new publisher", e)
    return None
  
  try:
    cursor.execute("SELECT publisher_id FROM Publishers WHERE name = ?", (publisher_name,))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error retrieving publisher id after insert", e)
    return None
  
  if len(result) > 0:
    return result[0][0]
  return None
  
"""
Insert a magazine...
Magazines have unique....
If a magazine exists do not insert again
Return ID
"""
def add_magazine(cursor, magazine_name, publisher_name):
  try:
    cursor.execute("SELECT magazine_id FROM Magazines WHERE name = ?", (magazine_name,))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error checking existing magazine.", e)
    return None
  
  if len(result) > 0:
    return result[0][0]
  
  # Looking up the publisher id (FK) before inserting a magazine
  try:
    cursor.execute("SELECT publisher_id FROM Publishers WHERE name = ?", (publisher_name,))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error looking up publisher", e)
    return None
  
  if len(result) == 0: 
    print(f"Publisher not found for magazine '{magazine_name}': {publisher_name}")
    return None
  
  publisher_id = result[0][0]
  
  try:
    cursor.execute("INSERT INTO Magazines (name, publisher_id) VALUES (?, ?)", (magazine_name, publisher_id))
  except sqlite3.Error as e:
    print("Error inserting magazine", e)
    return None
  
  try:
    cursor.execute("SELECT magazine_id FROM Magazines WHERE name = ?", (magazine_name,))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error retrieving magazine id after insert", e)
    return None
  
  if len(result) >  0:
    return result[0][0]
  return None
  
"""
Insert a subscriber...
subscriber.name not unique
If a subscriber with same name and address exists do not insert again
"""  
def add_subscriber(cursor, subscriber_name, address):
  try:
    cursor.execute("SELECT subscriber_id FROM Subscribers WHERE name = ? AND address = ?", (subscriber_name, address))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error checking existing subscriber", e)
    return None
  
  if len(result) > 0:
    return result[0][0]
  
  try:
    cursor.execute("INSERT INTO Subscribers (name, address) VALUES (?, ?)", (subscriber_name, address))
  except sqlite3.Error as e:
    print("Error inserting subscriber", e)
    return None
  
  try:
    cursor.execute("SELECT subscriber_id FROM Subscribers WHERE name = ? AND address = ?", (subscriber_name, address))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error retrieving subscriber id after insert", e)
    return None
  
  if len(result) > 0:
    return result[0][0]
  return None
  
"""
Insert a subscription if it dows not already exist
subscriptions is a join table between subscribers and magazines
FKs are, 
subscriber_id -> Subscribers.subscriber_id
magazine_id -> Magazines.magazine_id
It also stores expiration date
"""
def add_subscription(cursor, subscriber_name, address, magazine_name, expiration_date):
  # Look up subscriber id using the name and address
  try:
    cursor.execute("SELECT subscriber_id FROM Subscribers WHERE name = ? AND address = ?", (subscriber_name, address) )
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error looking up subscriber for subscription", e)
    return None
  
  if len(result) == 0:
    print(f"Subscriber not found for subscription {subscriber_name} | {address}")
    return None
  
  subscriber_id = result[0][0]
  
  # Look up magazine id by magazine name
  try:
    cursor.execute("SELECT magazine_id FROM Magazines WHERE name = ?", (magazine_name,))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error looking up magazine for subscription", e)
    return None
  
  if len(result) == 0:
    print(f"Magazine not found for subscription: {magazine_name}")
    return None
  
  magazine_id = result[0][0]
  
  # Check for a duplicate subscription, the same subscriber and magazine
  try:
    cursor.execute("SELECT subscription_id FROM Subscriptions WHERE subscriber_id = ? AND magazine_id = ?", (subscriber_id, magazine_id))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error checking existing subscription",e)
    return None
  
  if len(result) > 0:
    return result[0][0]
  
  # Insert the subscription
  try:
    cursor.execute("INSERT INTO Subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)", (subscriber_id, magazine_id, expiration_date))
  except sqlite3.Error as e:
    print("Error inserting subscription", e)
    return None
  
  # Now retrieve the subscription id after insert
  try:
    cursor.execute("SELECT subscription_id FROM Subscriptions WHERE subscriber_id = ? AND magazine_id = ?", (subscriber_id, magazine_id))
    result = cursor.fetchall()
  except sqlite3.Error as e:
    print("Error retrieving subscription id after insert", e)
    return None
  
  if len(result) > 0:
    return result[0][0]
  return None

# ===========================
# Task 1: Created a new SQLite DB
# Task 2: Define the DB structure
# Task 3: Populate tables with data
# ===========================
try:
  # Task 1: create and connect to the database
  with sqlite3.connect("../db/magazines.db") as conn:
    print("Connected to magazine database successfully.")
    
    # Task 3: enforce FK constraints
    try:
      conn.execute("PRAGMA foreign_keys = 1")
    except sqlite3.Error as e:
      print("Error enabling foreign keys", e)
      
    # leaving the block automatically closes the connection  
    cursor = conn.cursor()
    
    # ----------------------------------------------
    # Task 2: create the tables
    # ----------------------------------------------
    
    # Create the publishers table
    try:
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS Publishers (
          publisher_id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE
        );
        """)
    except sqlite3.Error as e:
      print("There was an error creating the publishers table", e)
      
    # Create the magazines table (1:M with publishers -> magazines)
    # Magazines has the FK that points to publishers
    try:
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS Magazines (
          magazine_id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE,
          publisher_id INTEGER NOT NULL,
          FOREIGN KEY (publisher_id) REFERENCES Publishers (publisher_id)
          );
          """)
    except sqlite3.Error as e:
      print("Error creating Magazine table", e)
      
    # Create a subscribers table
    try:
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscribers (
          subscriber_id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          ADDRESS TEXT NOT NULL
        );
        """)
    except sqlite3.Error as e:
      print("Error creating subscribers table", e)
      
    # Create the subscriptions table M:N with magazines <-> subscribers 
    # Subscriptions has FKs to both subscribers and magazines
    try:
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscriptions (
          subscription_id INTEGER PRIMARY KEY,
          subscriber_id INTEGER NOT NULL,
          magazine_id INTEGER NOT NULL,
          expiration_date TEXT NOT NULL,
          FOREIGN KEY (subscriber_id) REFERENCES Subscribers (subscriber_id),
          FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id) 
        );
      """)
    except sqlite3.Error as e:
      print("There was an error creating subscriptions table", e)
      
    # ----------------------------------------------
    # Task 3: Populate tables with data
    # ----------------------------------------------
    add_publisher(cursor, "Penguin Publishing")
    add_publisher(cursor, "Time Media Group")
    add_publisher(cursor, "Science Weekly Press")
      
    add_magazine(cursor, "Tech Today", "Penguin Publishing")
    add_magazine(cursor, "History Monthly", "Time Media Group")
    add_magazine(cursor, "Nature & Science", "Science Weekly Press")
      
    add_subscriber(cursor, "Alex Johnson", "101 Main St, Springfield, MO")
    add_subscriber(cursor, "Alex Johnson", "55 Park Ave, Charlotte, NC")
    add_subscriber(cursor, "Jamie Lee", "22 Oak St, Portland, OR")
      
    add_subscription(cursor, "Alex Johnson", "101 Main St, Springfield, MO", "Tech Today", "2026-12-31")
    add_subscription(cursor, "Alex Johnson", "101 Main St, Springfield, MO", "History Monthly", "2026-06-30")
    add_subscription(cursor, "Jamie Lee", "22 Oak St, Portland, OR", "Nature & Science", "2027-01-15")
      
    # Task 3: Commit the changes to the DB
    try:
      conn.commit()
    except sqlite3.Error as e:
      print("Error committing changes to the DB", e)
      
    # This print confirms that tasks 2 and 3 were completed Hopefully
    print("(Task 2 & 3) Tables created successfully, and data inserted.")
    
    # ------------------------------
    # Task 4: SQL Queries
    # ------------------------------
    # 1) Retrieve all the information from the subscribers table
    try:
      cursor.execute("SELECT * FROM Subscribers;")
      result = cursor.fetchall()
      print("----All Subscribers----")
      for row in result:
        print(row)
      print()
    except sqlite3.Error as e:
      print("Error retrieving subscribers", e)
    print()
      
    # 2) Retrieve all magazines sorted by name
    try:
      cursor.execute("SELECT * FROM Magazines ORDER BY name;")
      result = cursor.fetchall()
      print("----All Magazines Sorted by Name----")
      for row in result:
        print(row)
      print()
    except sqlite3.Error as e:
      print("Error retrieving magazines", e)
    print()
    
    # 3) Find magazines for a particular publisher
    publisher = "Science Weekly Press"
    
    try:
      cursor.execute("""
        SELECT m.magazine_id, m.name, p.name
        FROM Magazines m
        JOIN Publishers p ON m.publisher_id = p.publisher_id
        WHERE p.name = ?
        ORDER BY m.name;
      """, (publisher,))
      
      result = cursor.fetchall()
      print(f"----Magazines published by {publisher}----")
      for row in result:
        print(row)
      print()
    except sqlite3.Error as e:
      print("Error retrieving magazines for publisher", e)
    print()
    
except sqlite3.Error as e:
  print("Database connection error", e)  

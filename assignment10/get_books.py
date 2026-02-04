

# Task 1: Reviewed robots.txt 
# Reviewed the library robots file
# for user-agent: *, only /staff/ is disallowed.
# and include respectful pacing

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd
import json

# Task 2: Understanding HTML/DOM for the Durham Library Site
SEARCH_URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

# Result item (li):
LI_SELECTOR = 'li[data-test-id="searchResultItem"]'

# Title:
TITLE_SELECTOR = 'h3.cp-title span.title-content'

# Authors:
AUTHOR_SELECTOR = '.cp-by-author-block a.author-link'

# Format-Year container:
FORMAT_CONTAINER_SELECTOR = 'div.cp-format-info'

# Format-Year text:
FORMAT_TEXT_SELECTOR = 'span.cp-screen-reader-message'

# Task 3: Writing a program to execute this data
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
  driver.get(SEARCH_URL)
  
  li_entries = driver.find_elements(By.CSS_SELECTOR, LI_SELECTOR)
  print("Number of results found:", len(li_entries))
  
  results = []
  
  for li in li_entries:
    # Title
    title_elem = li.find_element(By.CSS_SELECTOR, TITLE_SELECTOR)
    title = title_elem.text.strip()
    
    # Authors
    author_elems = li.find_elements(By.CSS_SELECTOR, AUTHOR_SELECTOR)
    author_names = [a.text.strip() for a in author_elems if a.text.strip()]
    authors_joined = "; ".join(author_names)
    
    # Format-Year
    format_container = li.find_element(By.CSS_SELECTOR, FORMAT_CONTAINER_SELECTOR)
    format_elem = format_container.find_element(By.CSS_SELECTOR, FORMAT_TEXT_SELECTOR)
    format_year = format_elem.text.strip()
    
    results.append({
      "Title": title,
      "Authors": authors_joined,
      "Format-Year": format_year
    })
    
    df = pd.DataFrame(results)
    print(df)
  
finally:
  driver.quit()
  
  # Task 4: Write out the data
  df.to_csv("get_books.csv", index=False)
  
  with open("get_books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)
    

    

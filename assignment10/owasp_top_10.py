
# assignment10/owasp_top_10.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv


OWASP_PROJECT_URL = "https://owasp.org/www-project-top-ten/"


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    # 1) Load the project page (assignment link)
    driver.get(OWASP_PROJECT_URL)

    wait = WebDriverWait(driver, 20)

    # 2) Find the link to the current Top 10 page (2025) using XPath, then open it
    top10_link_el = wait.until(
        EC.presence_of_element_located((By.XPATH, '(//a[contains(@href, "/Top10/2025/")])[1]'))
    )
    top10_url = top10_link_el.get_attribute("href")
    driver.get(top10_url)

    # 3) XPath: find the ordered list right after the "Top 10:2025 List" heading
    # Then grab all <a> tags within that list (these are the 10 vulnerability links).
    top10_a_elements = wait.until(
        EC.presence_of_all_elements_located((
            By.XPATH,
            '//h3[contains(normalize-space(.), "Top 10:2025 List")]/following::ol[1]//a'
        ))
    )

    results = []
    seen = set()

    for a in top10_a_elements:
        title = (a.text or "").strip()
        href = a.get_attribute("href")

        # Deduplicate in case the page structure changes or repeats items
        if title and href and href not in seen:
            seen.add(href)
            results.append({"Title": title, "URL": href})

    # Keep only the first 10
    results = results[:10]

    # 4) Print list to verify
    print(results)

    # 5) Write CSV file
    with open("owasp_top_10.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "URL"])
        writer.writeheader()
        writer.writerows(results)

finally:
    driver.quit()

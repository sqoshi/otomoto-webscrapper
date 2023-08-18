from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run the browser in headless mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Create a WebDriver instance
driver = webdriver.Chrome(options=chrome_options)

# URL to the page you want to scrape
url = 'https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from=2020&year-to=2020&make=Alfa%20Romeo&model=Giulia&auction-type=All&page=2'

# Load the page
driver.get(url)

# Wait for the JavaScript to load (you might need to adjust the waiting time)
driver.implicitly_wait(5)

# Get the page content after JavaScript rendering
page_content = driver.page_source

# Close the browser
driver.quit()

# Now you can process the page content as needed
print(page_content)

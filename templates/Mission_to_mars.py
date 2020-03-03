import requests
import pandas as pd
import matplotlib as mp
import sqlalchemy
from bs4 import BeautifulSoup
import pymongo

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.Mission_to_Mars_db
collection = db.items 

def scrape():

    mars_dict = {}

    url = "https://mars.nasa.gov/news/"

# Retrieve page with the requests module
    response = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, "html.parser")

# Examine the results, then determine element that contains sought info
    print(soup.prettify())

    title = soup.find('div', class_='content_title').text
    paragraph = soup.find('div', class_='rollover_description_inner').text

# Display scrapped data 
    print(title)
    print(paragraph)
    mars_dict['title'] = title
    mars_dict['paragraph'] = paragraph

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(image_url)


# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    featured_image  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[2:-2]

# Website yrl 
    main_url = 'https://www.jpl.nasa.gov'

# Merge the Main URL with image route
    featured_image_url = main_url + featured_image

# return image link
    a =featured_image_url
    mars_dict['featured_image_url'] = a
# Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)

# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

# Find all elements that contain tweets
    new_comments = soup.find_all('div', class_='js-tweet-text-container')

# Retrieve all elements that contain news title in the specified range
# Look for entries that display weather related words to exclude non weather related tweets 
    for comment in new_comments: 
        weather_comment = comment.find('p').text
        if 'Sol' and 'pressure' in weather_comment:
            print(weather_comment)
            break
        else: 
            pass



# Visit Mars facts url and read using pandas
    mars_fact = pd.read_html('http://space-facts.com/mars/')
# mars_fact

    type(mars_fact)

# assign to DataFrme
    mars_df = pd.DataFrame(mars_fact[0])
# generate columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

# make index to the Description
    mars_df.set_index('Description', inplace=True)

# Save html code to folder
    mars_df.to_html()
    mars_df

    from selenium import webdriver
    import urllib.parse

    BASE_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    FILE = "html-selenium.txt"
    FILE_WAIT = "html-selenium-wait.txt"

# wait with selenium 10 seconds
    driver = webdriver.Firefox()
    driver.get(BASE_URL)
    driver.implicitly_wait(10)
    html = driver.page_source
    driver.close()
    with open(FILE_WAIT, "w+", encoding="utf-8") as f:
        f.write(html)


    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='description')

    print("ITEMS")
    print(items)

    
    # Store link that leads to full image website
    a_tags = soup.find_all('a', class_='itemLink product-item')
    for a_tag in a_tags:
        results = [{ "Title": a_tag.text,"Img_URL": urllib.parse.urljoin("https://astrogeology.usgs.gov", a_tag["href"]),}]
    

    # Display hemisphere_image_urls
    return results

if __name__ == "__main__":
    scrape()





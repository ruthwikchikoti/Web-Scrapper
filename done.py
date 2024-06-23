import requests
from tabulate import tabulate
from bs4 import BeautifulSoup

user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"}

flipkart_product_url = input("ENTER THE FLIPKART PRODUCT URL: ")
snapdeal_product_url = input("ENTER THE SNAPDEAL PRODUCT URL: ")
amazon_product_url = input("ENTER THE AMAZON PRODUCT URL: ")

def scrape_flipkart(url, user_agent):
    try:
        response = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(response.content, 'html.parser')
        name_element = soup.find('span', class_='B_NuCI')
        price_element = soup.find('div', class_='_30jeq3 _16Jk6d')
        
        if price_element:
            price = price_element.get_text()
            name = name_element.get_text()
            return price.strip(), name.strip()
    except Exception as e:
        return None

def scrape_snapdeal(url, user_agent):
    try:
        response = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(response.content, 'html.parser')
        name_element = soup.find('h1', class_='pdp-e-i-head')
        price_element = soup.find('span', class_='payBlkBig')
        
        if price_element:
            price = price_element.get_text()
            name = name_element.get_text()
            return price.strip(), name.strip()
    except Exception as e:
        return None

def scrape_amazon(url, user_agent):
    try:
        response = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(response.content, 'html.parser')
        name_element = soup.find('span', class_='a-size-large product-title-word-break')
        price_element = soup.find('span', class_='a-price-whole')
        
        if price_element:
            price = price_element.get_text()
            name = name_element.get_text()
            return price.strip(), name.strip()
    except Exception as e:
        return None

flipkart_price, flipkart_name = scrape_flipkart(flipkart_product_url, user_agent)
snapdeal_price, snapdeal_name = scrape_snapdeal(snapdeal_product_url, user_agent)
amazon_price, amazon_name = scrape_amazon(amazon_product_url, user_agent)

if None in (flipkart_price, snapdeal_price, amazon_price):
    print("An error occurred while scraping product information.")
else:
    flipkart_price = float(flipkart_price.replace("₹", "").replace(",", ""))
    snapdeal_price = float(snapdeal_price.replace("₹", "").replace(",", ""))
    amazon_price = float(amazon_price.replace("₹", "").replace(",", ""))
    
    product_details = [
        ["Product Source", "Product Name", "Product Price"],
        ["Flipkart", flipkart_name, flipkart_price],
        ["Snapdeal", snapdeal_name, snapdeal_price],
        ["Amazon", amazon_name, amazon_price]
    ]

    print(tabulate(product_details, headers="firstrow", tablefmt="fancy_grid"))

    best_product_price = min(flipkart_price, snapdeal_price, amazon_price)
    best_product_by = None

    if best_product_price == flipkart_price:
        best_product_by = "Flipkart"
        best_product_name = flipkart_name
    elif best_product_price == snapdeal_price:
        best_product_by = "Snapdeal"
        best_product_name = snapdeal_name
    else:
        best_product_by = "Amazon"
        best_product_name = amazon_name

    best_products = [
        [best_product_by, best_product_name, best_product_price]
    ]

    print()
    print(tabulate(best_products, tablefmt="fancy_grid"))

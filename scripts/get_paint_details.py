from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

url = "https://www.dulux.com.au/paint/1step-prep/1step-prep-water-based-primer-sealer-and-undercoat/"

def get_price(page, size, url):
        try:
            # find size button and click on it
            for x in range(7):
                btn = page.get_by_test_id(size + "__" + str(x)).locator("xpath=..")
                if btn.is_visible():
                    break
            btn.click(timeout=200)
            time.sleep(1.5)

            # get price from html
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            title = soup.find("span", class_="item-name__family").get_text()
            price = soup.find(attrs={"data-testid": "d2c-price-value"}).get_text()
        except Exception as e:
            price = "not found"
            print(e)

        # write to file
        with open("../product_details/paint.txt", "a") as f:
            if price != "not found":
                f.write(title + "\t" + size + "\t" + price.lstrip("$") + "\t" + url + "\n")
        return price

def load_product(page, url):
    page.goto(url)

    try:
        page.get_by_test_id("d2c-selected-colour-info").get_by_role("button").click(timeout=1000)
        time.sleep(2)
        page.get_by_test_id("active-hues-grouping-item").first.click(timeout=1000)
        page.get_by_test_id("colour-atlas-listing").first.get_by_role("button").first.click(timeout=1000)
        page.get_by_test_id("colourAtlasListingPanel").first.get_by_role("button").first.click(timeout=1000)
        time.sleep(2)
    except Exception as e:
        print(e)
        
    print(get_price(page, "500ML", url))
    print(get_price(page, "1L", url))
    print(get_price(page, "2L", url))
    print(get_price(page, "4L", url))
    print(get_price(page, "10L", url))
    print(get_price(page, "15L", url))

def run():
    with sync_playwright() as p:
        # launch browser
        print("Launching chromium...")
        browser = p.chromium.launch(headless=False)
        # bypass anti-bot
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0"
        )

        page = context.new_page()
        # clear details file
        with open("../product_details/paint.txt", "w") as f:
             f.write("")

        try:
            with open("../product_details/paint_urls.txt", "r") as f:
                for line in f:
                    if line[0] != "#":
                        load_product(page, line.strip("\n"))
        except FileNotFoundError:
             print(f"Error: file not found")


run()
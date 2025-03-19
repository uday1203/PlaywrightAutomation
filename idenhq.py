import json
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from tqdm import tqdm

# Replace with your login credentials
credentials = {
    'username': 'uppara.udaykumar@cmr.edu.in',  # Replace with your email
    'password': 'sEIjYqZB'  # Replace with your password
}


def login(page):
    """
    Logs into the application using provided credentials.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        PlaywrightTimeoutError: If the login process takes too long.
    """
    try:
        # Fill out the login form
        page.fill("#email", credentials['username'])
        page.fill("#password", credentials['password'])

        # Click the 'Sign in' button
        page.click('button[type="submit"]')

        # Wait for navigation after login
        page.wait_for_load_state("networkidle", timeout=10000)

        print("Login completed.")
    except PlaywrightTimeoutError as e:
        print(f"Login failed due to timeout: {e}")
        raise
    except Exception as e:
        print(f"An error occurred during login: {e}")
        raise


def click_launch_challenge(page):
    """
    Clicks on the 'Launch Challenge' button after closing the popup.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        PlaywrightTimeoutError: If the button or necessary elements do not load within the timeout period.
    """
    try:
        # Wait for and click the close button
        page.wait_for_selector('button:has(svg.lucide-x)', timeout=5000)
        page.click('button:has(svg.lucide-x)')

        print("Close button clicked.")
        page.wait_for_selector('body')

        # Wait for and click the 'Launch Challenge' button
        page.wait_for_selector('button:has-text("Launch Challenge")')
        page.click('button:has-text("Launch Challenge")')

        # Wait for the next page or content to load
        page.wait_for_selector("body")
        print("Launched the challenge.")
    except PlaywrightTimeoutError as e:
        print(f"Failed to click 'Launch Challenge' or close the popup: {e}")
        raise
    except Exception as e:
        print(f"An error occurred while launching the challenge: {e}")
        raise


def navigate_to_product_catalog(page):
    """
    Navigates to the Product Catalog by interacting with the UI.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        PlaywrightTimeoutError: If the navigation or element selection fails.
    """
    try:
        # Click the menu button to open data tools
        page.wait_for_selector('xpath=//*[@id="root"]/div[2]/main/div/div/div[2]/div/div/div[1]/button')
        page.click('xpath=//*[@id="root"]/div[2]/main/div/div/div[2]/div/div/div[1]/button')

        print("Menu button clicked.")
        page.wait_for_selector('button[aria-controls="radix-:r1:"]')

        # Click 'Data Tools' button
        page.click('button[aria-controls="radix-:r1:"]')

        print("Data Tools button clicked.")
        page.wait_for_selector('button[aria-controls="radix-:r2:"]')

        # Click 'Inventory Management' button
        page.click('button[aria-controls="radix-:r2:"]')

        print("Inventory Management button clicked.")
        page.wait_for_selector('button:has(svg.lucide-store)')

        # Click 'Product Catalog' button
        page.click('button:has(svg.lucide-store)')

        print("Product Catalog button clicked.")
        page.wait_for_selector('button:has(svg.lucide-database)')

        # Click 'Load Product Data' button
        page.click('button:has(svg.lucide-database)')

        print("Load Product Data button clicked.")
    except PlaywrightTimeoutError as e:
        print(f"Failed to navigate to Product Catalog: {e}")
        raise
    except Exception as e:
        print(f"An error occurred during navigation: {e}")
        raise


def scroll_page_until_end(page, max_scrolls=1000):
    """
    Scrolls the page until all products are loaded or a limit is reached.

    Args:
        page: The Playwright page object representing the browser page.
        max_scrolls (int): The maximum number of scroll attempts before stopping.

    Raises:
        PlaywrightTimeoutError: If the scrolling process encounters a timeout.
    """
    try:
        infinite_scroll_selector = '.infinite-table'
        product_count_selector = "div.flex.justify-between.items-center.px-2 .text-sm.text-muted-foreground"

        # Wait for the infinite scroll table to load
        page.wait_for_selector(infinite_scroll_selector)

        prev_height = -1
        scroll_count = 0

        while scroll_count < max_scrolls:
            # Ensure the infinite scroll element exists
            infinite_scroll = page.query_selector(infinite_scroll_selector)
            if not infinite_scroll:
                print("Infinite scroll element not found!")
                break

            # Scroll within the container
            page.evaluate(f"document.querySelector('{infinite_scroll_selector}').scrollTop = document.querySelector('{infinite_scroll_selector}').scrollHeight")
            page.wait_for_timeout(1000)  # Wait for content to load

            # Check if scroll height has changed (indicating more content has loaded)
            new_height = page.evaluate(f"document.querySelector('{infinite_scroll_selector}').scrollHeight")
            if new_height == prev_height:
                print("Reached the end of the product list.")
                break

            prev_height = new_height
            scroll_count += 1

            # Extract and print the number of shown and total products from the page
            product_info = page.query_selector(product_count_selector)
            if product_info:
                products_text = product_info.inner_text()
                match = re.search(r"Showing (\d+) of (\d+) products", products_text)
                if match:
                    shown_products = int(match.group(1))
                    total_products = int(match.group(2))  # Update this dynamically if needed

                    print(f"Shown Products: {shown_products}, Total Products: {total_products}")
                    if shown_products >= total_products:
                        print("All products are displayed.")
                        return

        print(f"Scrolling completed after {scroll_count} attempts.")
    except PlaywrightTimeoutError as e:
        print(f"Scrolling failed due to timeout: {e}")
        raise
    except Exception as e:
        print(f"An error occurred during scrolling: {e}")
        raise


def extract_product_data(page):
    """
    Extracts product details from the page.

    Args:
        page: The Playwright page object representing the browser page.

    Returns:
        A list of dictionaries containing product information.

    Raises:
        Exception: If there is an error while extracting product data.
    """
    try:
        rows_selector = "table tbody tr"
        rows = page.query_selector_all(rows_selector)

        product_data = []
        for row in tqdm(rows, desc="Extracting product data", unit="row"):
            # Extract product details for each row
            id_ = row.query_selector("td:nth-child(1)").inner_text()
            title = row.query_selector("td:nth-child(2)").inner_text()
            category = row.query_selector("td:nth-child(3)").inner_text()
            warranty = row.query_selector("td:nth-child(4)").inner_text()
            mass = row.query_selector("td:nth-child(5)").inner_text()
            brand = row.query_selector("td:nth-child(6)").inner_text()
            price = row.query_selector("td:nth-child(7)").inner_text()

            # Append the extracted data to the list
            product_data.append({
                "id": id_,
                "title": title,
                "category": category,
                "warranty": warranty,
                "mass": mass,
                "brand": brand,
                "price": price
            })

        return product_data
    except Exception as e:
        print(f"Error while extracting product data: {e}")
        raise


def save_to_json(data, output_path="Data.json"):
    """
    Saves the extracted data to a JSON file.

    Args:
        data: The data to save (list of product information).
        output_path (str): The path where the JSON file will be saved.

    Raises:
        IOError: If there's an error writing to the file.
    """
    try:
        with open(output_path, "w") as file:
            json.dump(data, file, indent=2)

        print(f"Data saved to {output_path}.")
    except IOError as e:
        print(f"Error saving data to file: {e}")
        raise


def start_browser():
    """
    Initiates the browser automation, logs in if needed, navigates through the site,
    extracts product data, and saves it to a JSON file.
    """
    with sync_playwright() as p:
        # Launch the browser in normal mode (not incognito)
        browser = p.chromium.launch(headless=False)

        # Create a new context and page
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://hiring.idenhq.com/")

        # Check if the user is already logged in by looking for the login button
        login_button = page.query_selector('button[type="submit"]')

        if login_button:
            print("User is not logged in, proceeding with login...")
            login(page)  # Proceed with login
        else:
            print("User is already logged in, skipping login...")

        # Wait for the page to load and click the 'Launch Challenge' button
        click_launch_challenge(page)

        # Navigate to the product catalog page
        navigate_to_product_catalog(page)

        # Scroll to load all products
        scroll_page_until_end(page)

        # Extract product data
        print("Started extracting data")
        product_data = extract_product_data(page)

        # Save the extracted data to a JSON file
        save_to_json(product_data)

        # Close the browser
        browser.close()


if __name__ == "__main__":
    start_browser()

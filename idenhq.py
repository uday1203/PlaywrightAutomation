# -*- coding: utf-8 -*-
"""IDENHQ.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jvXYg_O4DXXEyV2dGNJP9ANw-9eFaHC5
"""

!pip install playwright
!playwright install
!apt-get install -y libgbm-dev

import nest_asyncio
nest_asyncio.apply()

import json
import time
import asyncio
from playwright.async_api import async_playwright


credentials = {
    'username': 'uppara.udaykumar@cmr.edu.in',
    'password': 'sEIjYqZB'
}


async def login(page):
    await page.fill("#email", credentials['username'])
    await page.fill("#password", credentials['password'])
    await page.click('button[type="submit"]')
    await page.wait_for_load_state("networkidle")
    print("Login completed.")


async def click_launch_challenge(page):
    await page.wait_for_selector('button:has-text("Launch Challenge")')
    await page.click('button:has-text("Launch Challenge")')
    await page.wait_for_selector("body")
    print("Launched the challenge.")


async def navigate_to_product_catalog(page):
    await page.wait_for_selector('xpath=//*[@id="root"]/div[2]/main/div/div/div[2]/div/div/div[1]/button')
    await page.click('xpath=//*[@id="root"]/div[2]/main/div/div/div[2]/div/div/div[1]/button')

    print("Button clicked using XPath.")
    print("Menu button clicked and menu opened.")
    await page.wait_for_selector('button[aria-controls="radix-:r1:"]')

    await page.click('button[aria-controls="radix-:r1:"]')
    print("Data Tools button clicked.")

    await page.wait_for_selector('button[aria-controls="radix-:r2:"]')
    await page.click('button[aria-controls="radix-:r2:"]')
    print("Inventory Management button clicked.")

    await page.wait_for_selector('button:has(svg.lucide-store)')
    await page.click('button:has(svg.lucide-store)')
    print("Product Catalog button clicked.")

    await page.wait_for_selector('button:has(svg.lucide-database)')
    await page.click('button:has(svg.lucide-database)')
    print("Load Product Data button clicked.")


async def get_product_data(page):
    product_data = []
    scroll_finished = False

    while not scroll_finished:
        await asyncio.sleep(2)  # Give time for data to load

        new_products = await page.evaluate('''() => {
            const rows = document.querySelectorAll('table tbody tr');
            const products = [];

            if (rows.length === 0) {
                console.log("⚠️ No table rows found! Check your selector.");
            }

            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 0) {
                    const product = {
                        id: cells[0].textContent.trim(),
                        name: cells[1].textContent.trim(),
                        category: cells[2].textContent.trim(),
                        warranty: cells[3].textContent.trim(),
                        mass: cells[4].textContent.trim(),
                        brand: cells[5].textContent.trim(),
                        price: cells[6].textContent.trim(),
                    };
                    products.push(product);
                }
            });

            console.log("✅ Extracted products:", products);
            return products;
        }''')

        if new_products:
            print(f"✅ Extracted {len(new_products)} new products.")
        else:
            print("⚠️ No new products found.")

        product_data.extend(new_products)

        more_data_to_load = await page.query_selector('tr.infinite-table-row')

        if not more_data_to_load:
            scroll_finished = True
        else:
            await page.evaluate('window.scrollBy(0, window.innerHeight);')
            await asyncio.sleep(2)

    return product_data


async def save_to_json(data):
    output_path = "productData.json"
    with open(output_path, "w") as file:
        json.dump(data, file, indent=2)
    print(f"Data saved to {output_path}.")


async def start_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://hiring.idenhq.com/")

        login_button = await page.query_selector('button[type="submit"]')

        if login_button:
            print("User is not logged in, proceeding with login...")
            await login(page)
        else:
            print("User is already logged in, skipping login...")

        await click_launch_challenge(page)
        await navigate_to_product_catalog(page)

        product_data = await get_product_data(page)
        await save_to_json(product_data)

        print(product_data)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(start_browser())
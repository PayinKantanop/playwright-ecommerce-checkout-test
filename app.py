# app.py
import time
import re
from playwright.sync_api import sync_playwright,expect

def run(playwright):
    # เปิดเบราว์เซอร์ Chromium ขึ้นมา
    # headless=False เพื่อให้เราเห็นหน้าต่างเบราว์เซอร์
    browser = playwright.chromium.launch(headless=False)
    
    # เปิดหน้าเว็บ (tab) ใหม่
    page = browser.new_page()
    
    # ไปที่ URL ที่ต้องการ
    page.goto("https://www.saucedemo.com/")

    #กรอก Username
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    time.sleep(5)

    #กดปุ่ม Login
    login_button = page.locator('[data-test="login-button"]')
    login_button.click()

    #ตรวจสอบ ว่ามาหน้าถูกต้องหรือไม่
    expect(page).to_have_url(re.compile(r"/inventory.html"))
    expect(page.locator(".title")).to_have_text("Products")
    time.sleep(3)

    #เพิ่มตระกร้าสินค้า
    Sauce_Labs_Backpack_AddtoCart_button = page.locator('[name=add-to-cart-sauce-labs-backpack]')
    Sauce_Labs_Backpack_AddtoCart_button.click()
    time.sleep(3)

    #ตรวจสอบว่าตระกร้าสินค้ามีรายการเพิ่มขึ้น
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_be_visible()
    time.sleep(2)

    #ไปที่หน้าตระกร้าสินค้า
    page.goto("https://www.saucedemo.com/cart.html")
    expect(page).to_have_url(re.compile(r"/cart.html"))
    expect(page.locator(".title")).to_have_text("Your Cart")
    time.sleep(3)

    #ตรวจสินค้าว่ามีสินค้าจริงไหม
    expect(page.locator('[data-test="inventory-item-name"]')).to_be_visible()

    #กดปุ่ม Checkout
    checkout_button = page.locator("#checkout")
    checkout_button.click()

    #ตรวจสอบว่าไปหน้า Check out ไหม
    expect(page).to_have_url(re.compile(r"/checkout-step-one.html"))
    expect(page.locator(".title")).to_have_text("Checkout: Your Information")
    
    #เติมค่าลงใน Form
    page.locator("#first-name").fill("Kantanop")
    page.locator("#last-name").fill("Kamkunsri")
    page.locator("#postal-code").fill("65000")
    time.sleep(3)
    
    #คลิกปุ่ม Continue
    continuce_button = page.locator("#continue")
    continuce_button.click()

    #ตรสจสอบไปหน้า Check ouy Step2 ไหม
    expect(page).to_have_url(re.compile(r"/checkout-step-two.html"))
    expect(page.locator(".title")).to_have_text("Checkout: Overview")
    expect(page.locator('[data-test="inventory-item-name"]')).to_be_visible()
    time.sleep(3)

    #คลิกปุ่ม Finish
    finish_button = page.locator("#finish")
    finish_button.click()

    #ตรวจสอบว่าซื้อสินค้าสำเร็จไหม
    expect(page).to_have_url(re.compile(r"/checkout-complete.html"))
    expect(page.locator('[data-test="complete-header"]')).to_have_text("Thank you for your order!")

    # แสดง title ของหน้าเว็บออกมาใน terminal
    print(page.title())
    
    # รอ 5 วินาที
    time.sleep(5)
    
    # ปิดเบราว์เซอร์
    browser.close()

# เริ่มการทำงานของ Playwright
with sync_playwright() as playwright:
    run(playwright)
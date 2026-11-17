from decimal import Decimal

from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BASE_URL = "https://www.saucedemo.com"
PASSWORD = "secret_sauce"
BACKPACK = "Sauce Labs Backpack"


def sign_in(page: Page, username: str = "standard_user") -> InventoryPage:
    login = LoginPage(page)
    login.open()
    login.login(username, PASSWORD)
    return InventoryPage(page)


def test_valid_login_opens_inventory(page: Page) -> None:
    sign_in(page)

    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


def test_locked_account_is_denied(page: Page) -> None:
    login = LoginPage(page)
    login.open()
    login.login("locked_out_user", PASSWORD)

    expect(login.error).to_be_visible()
    expect(login.error).to_contain_text("locked out")
    expect(page).to_have_url(f"{BASE_URL}/")


def test_empty_username_shows_required_validation(page: Page) -> None:
    login = LoginPage(page)
    login.open()
    login.login("", PASSWORD)

    expect(login.error).to_be_visible()
    expect(login.error).to_contain_text("Username is required")
    expect(page).not_to_have_url(f"{BASE_URL}/inventory.html")


def test_add_product_updates_badge_and_cart(page: Page) -> None:
    inventory = sign_in(page)
    inventory.add_product(BACKPACK)

    expect(inventory.cart_badge).to_have_text("1")
    inventory.open_cart()
    expect(CartPage(page).item_named(BACKPACK)).to_be_visible()


def test_remove_only_product_clears_cart_and_badge(page: Page) -> None:
    inventory = sign_in(page)
    inventory.add_product(BACKPACK)
    inventory.open_cart()
    cart = CartPage(page)
    cart.remove_product(BACKPACK)

    expect(cart.item_named(BACKPACK)).to_have_count(0)
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)


def test_sort_prices_low_to_high(page: Page) -> None:
    inventory = sign_in(page)
    inventory.sort_control.select_option("lohi")

    prices = inventory.product_prices()
    assert prices == sorted(prices)


def test_checkout_requires_first_name(page: Page) -> None:
    inventory = sign_in(page)
    inventory.add_product(BACKPACK)
    inventory.open_cart()
    CartPage(page).checkout()
    checkout = CheckoutPage(page)
    checkout.enter_customer("", "Rao", "560001")

    expect(checkout.error).to_be_visible()
    expect(checkout.error).to_contain_text("First Name is required")
    expect(page).to_have_url(f"{BASE_URL}/checkout-step-one.html")
    expect(checkout.finish_button).to_have_count(0)


def test_complete_purchase_and_verify_subtotal(page: Page) -> None:
    inventory = sign_in(page)
    inventory.add_product(BACKPACK)
    inventory.open_cart()
    CartPage(page).checkout()
    checkout = CheckoutPage(page)
    checkout.enter_customer("Asha", "Rao", "560001")

    assert checkout.displayed_subtotal() == checkout.reviewed_item_total()

    checkout.finish_purchase()
    expect(checkout.complete_header).to_have_text("Thank you for your order!")

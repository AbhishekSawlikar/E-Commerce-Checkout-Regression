from decimal import Decimal

from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.items = page.locator('[data-test="inventory-item"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.sort_control = page.locator('[data-test="product-sort-container"]')
        self.prices = page.locator('[data-test="inventory-item-price"]')

    def add_product(self, name: str) -> None:
        item = self.items.filter(has=self.page.get_by_text(name, exact=True))
        item.get_by_role("button", name="Add to cart").click()

    def product_prices(self) -> list[Decimal]:
        values = self.prices.all_text_contents()
        return [Decimal(value.strip().replace("$", "")) for value in values]

    def open_cart(self) -> None:
        self.cart_link.click()

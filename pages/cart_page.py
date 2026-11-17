from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.items = page.locator('[data-test="inventory-item"]')
        self.checkout_button = page.locator('[data-test="checkout"]')

    def item_named(self, name: str):
        return self.items.filter(has=self.page.get_by_text(name, exact=True))

    def remove_product(self, name: str) -> None:
        self.item_named(name).get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        self.checkout_button.click()

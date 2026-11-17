from decimal import Decimal

from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.error = page.locator('[data-test="error"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.subtotal = page.locator('[data-test="subtotal-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.complete_header = page.locator('[data-test="complete-header"]')

    def enter_customer(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()

    def reviewed_item_total(self) -> Decimal:
        values = self.item_prices.all_text_contents()
        return sum(
            (Decimal(value.strip().replace("$", "")) for value in values),
            start=Decimal("0"),
        )

    def displayed_subtotal(self) -> Decimal:
        value = self.subtotal.inner_text().split("$")[-1]
        return Decimal(value.strip())

    def finish_purchase(self) -> None:
        self.finish_button.click()

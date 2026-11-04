# Copyright (c) 2026, Manish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):
	def after_insert(self):
		self.update_airport_shop_count()

	def on_trash(self):
		self.update_airport_shop_count()

	def update_airport_shop_count(self):
		if self.airport:
			count = frappe.db.count("Airport Shop", {"airport": self.airport})
			frappe.db.set_value("Airport", self.airport, "number_of_shops", count)

# Copyright (c) 2026, Manish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class LeaseContract(Document):
	def validate(self):
		self.calculate_total_rent()
		self.calculate_duration()
		self.prevent_double_leasing()
		self.auto_expire()

	def on_submit(self):
		self.update_shop_status("Occupied")

	def on_cancel(self):
		self.update_shop_status("Available")

	def calculate_total_rent(self):
		total = sum(row.monthly_rent or 0 for row in self.shops)
		self.total_rent = total

	def calculate_duration(self):
		if self.start_date and self.end_date:
			delta = (getdate(self.end_date) - getdate(self.start_date)).days
			self.contract_duration = max(delta // 30, 1)

	def prevent_double_leasing(self):
		if self.contract_status != "Active":
			return
		for row in self.shops:
			active_contracts = frappe.get_all(
				"Lease Contract",
				filters={
					"contract_status": "Active",
					"docstatus": 1,
					"name": ["!=", self.name],
				},
				fields=["name"],
			)
			for contract in active_contracts:
				overlap = frappe.get_all(
					"Contract Shop Item",
					filters={"parent": contract.name, "shop": row.shop},
					fields=["name"],
				)
				if overlap:
					frappe.throw(f"Shop {row.shop} is already under an active contract: {contract.name}")

	def auto_expire(self):
		if self.contract_status != "Active":
			return
		if self.end_date and getdate(self.end_date) < getdate():
			self.contract_status = "Expired"

	def update_shop_status(self, status):
		for row in self.shops:
			if frappe.db.exists("Airport Shop", row.shop):
				frappe.db.set_value("Airport Shop", row.shop, "shop_status", status)

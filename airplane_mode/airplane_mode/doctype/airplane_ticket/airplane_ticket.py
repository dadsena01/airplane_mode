# Copyright (c) 2026, Manish and contributors
# For license information, please see license.txt

import random

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		self.calculate_total_amount()
		self.remove_duplicate_add_ons()
		self.validate_overbooking()

		if self.status == "Boarded" and not self.is_new():
			original_seat = frappe.db.get_value("Airplane Ticket", self.name, "seat")
			if self.seat != original_seat:
				frappe.throw("Seat cannot be changed after boarding.")

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Cannot submit the ticket unless the status is 'Boarded'")

	def before_insert(self):
		if not self.seat:
			self.seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"

	def calculate_total_amount(self):
		add_on_total = sum(row.amount or 0 for row in self.get("add_ons", []))
		self.total_amount = (self.flight_price or 0) + add_on_total

	def remove_duplicate_add_ons(self):
		seen = set()
		unique_add_ons = []
		for row in self.get("add_ons", []):
			if row.item not in seen:
				seen.add(row.item)
				unique_add_ons.append(row)
		self.set("add_ons", unique_add_ons)

	def validate_overbooking(self):
		if not self.flight:
			return
		airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
		if not airplane:
			return
		capacity = frappe.db.get_value("Airplane", airplane, "capacity")
		if capacity is None:
			return
		filters = {"flight": self.flight, "docstatus": ["!=", 2]}
		if not self.is_new():
			filters["name"] = ("!=", self.name)
		ticket_count = frappe.db.count("Airplane Ticket", filters=filters)
		if ticket_count >= capacity:
			frappe.throw(f"Cannot book: Flight {self.flight} is at full capacity ({capacity} seats)")

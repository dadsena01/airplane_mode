import random

import frappe


def execute():
	if not frappe.db.exists("DocType", "Airplane Ticket"):
		return
	if not frappe.db.has_column("Airplane Ticket", "seat"):
		return
	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"seat": ("in", ["", None])},
		pluck="name",
	)
	for name in tickets:
		seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"
		frappe.db.set_value("Airplane Ticket", name, "seat", seat, update_modified=False)

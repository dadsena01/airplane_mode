# Copyright (c) 2026, Manish and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime


def update_ticket_gate_numbers(flight_name, gate_number):
	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"flight": flight_name, "docstatus": ["!=", 2]},
		pluck="name",
	)
	for name in tickets:
		frappe.db.set_value("Airplane Ticket", name, "gate_number", gate_number)


def send_rent_reminders():
	if not frappe.db.get_single_value("Shop Settings", "enable_rent_reminders"):
		return
	contracts = frappe.get_all(
		"Lease Contract",
		filters={"contract_status": "Active", "docstatus": 1},
		fields=["name", "tenant"],
	)
	this_month = now_datetime().strftime("%Y-%m")
	for contract in contracts:
		existing = frappe.db.exists(
			"Rent Payment",
			{
				"contract": contract.name,
				"payment_month": ("like", f"{this_month}-%"),
				"docstatus": 1,
			},
		)
		if existing:
			continue
		tenant = frappe.get_doc("Tenant", contract.tenant)
		if not tenant.email:
			continue
		lease = frappe.get_doc("Lease Contract", contract.name)
		shop_names = []
		total_rent = 0
		for row in lease.shops:
			shop = frappe.db.get_value("Airport Shop", row.shop, "shop_name")
			shop_names.append(shop or row.shop)
			total_rent += row.monthly_rent or 0
		frappe.sendmail(
			recipients=[tenant.email],
			subject="Rent Due for Your Shops",
			message=(
				f"Dear {tenant.tenant_name},<br><br>"
				f"Your rent of {total_rent} for shops: "
				f"{', '.join(shop_names)} is due for "
				f"{this_month}.<br><br>"
				f"Please make the payment at your earliest convenience."
				f"<br><br>Thank you,<br>Airport Authority"
			),
		)

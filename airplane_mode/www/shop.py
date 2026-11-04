import frappe
from frappe.utils import fmt_money


def get_context(context):
	name = frappe.form_dict.get("name")
	if not name:
		context.shop = None
		return
	try:
		doc = frappe.get_doc("Airport Shop", name)
		context.shop = doc
		context.airport_name = doc.airport
		context.contract = None
		context.tenant_name = None
		context.formatted_rent = None
		context.contract_start = None
		context.contract_end = None

		active_contract = frappe.db.get_value(
			"Contract Shop Item",
			{"shop": name, "parenttype": "Lease Contract"},
			"parent",
		)
		if active_contract:
			lease = frappe.get_doc("Lease Contract", active_contract)
			if lease.contract_status == "Active" and lease.docstatus == 1:
				context.contract = lease
				context.tenant_name = frappe.db.get_value("Tenant", lease.tenant, "tenant_name")
				for row in lease.shops:
					if row.shop == name:
						context.formatted_rent = fmt_money(row.monthly_rent)
						break
				context.contract_start = lease.start_date
				context.contract_end = lease.end_date
	except frappe.DoesNotExistError:
		context.shop = None

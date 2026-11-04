import frappe


def execute(filters=None):
	airlines = frappe.get_all("Airline", pluck="name")
	data = []
	total_revenue = 0
	for airline in airlines:
		airplanes = frappe.get_all("Airplane", filters={"airline": airline}, pluck="name")
		revenue = 0
		for airplane in airplanes:
			flights = frappe.get_all("Airplane Flight", filters={"airplane": airplane}, pluck="name")
			for flight in flights:
				amounts = frappe.get_all(
					"Airplane Ticket",
					filters={"flight": flight, "docstatus": 1},
					pluck="total_amount",
				)
				revenue += sum(t or 0 for t in amounts)
		data.append({"airline": airline, "revenue": revenue})
		total_revenue += revenue

	data.append({"airline": "Total", "revenue": total_revenue})

	columns = [
		{"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
		{"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
	]

	chart = {
		"data": {
			"labels": [row["airline"] for row in data if row["airline"] != "Total"],
			"datasets": [
				{"name": "Revenue", "values": [row["revenue"] for row in data if row["airline"] != "Total"]}
			],
		},
		"type": "donut",
	}

	report_summary = [{"label": "Total Revenue", "value": total_revenue, "datatype": "Currency"}]

	return columns, data, None, chart, report_summary

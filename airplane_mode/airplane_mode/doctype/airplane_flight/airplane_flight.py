import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	website = frappe._dict(
		template="airplane_mode/doctype/airplane_flight/templates/airplane_flight.html",
		condition_field="is_published",
		page_title_field="airplane",
	)

	def autoname(self):
		pass

	def make_route(self):
		return self.scrub(self.name)

	def validate(self):
		self.update_gate_status()
		if not self.route:
			self.route = self.make_route()

	def on_update(self):
		if self.has_value_changed("gate") and self.gate:
			frappe.enqueue(
				"airplane_mode.airplane_mode.tasks.update_ticket_gate_numbers",
				queue="short",
				flight_name=self.name,
				gate_number=self.gate,
			)

	def on_submit(self):
		self.db_set("status", "Completed")

	def update_gate_status(self):
		if self.has_value_changed("gate"):
			if self.get_db_value("gate"):
				frappe.db.set_value("Gate", self.get_db_value("gate"), "status", "Available")
			if self.gate:
				frappe.db.set_value("Gate", self.gate, "status", "Occupied")


@frappe.whitelist()
def get_crew_for_airline(doctype, txt, searchfield, start, page_len, filters):
	airplane = filters.get("airplane")
	airline = frappe.db.get_value("Airplane", airplane, "airline")
	if not airline:
		return []
	crew = frappe.get_all(
		"Crew Member",
		fields=["name", "role"],
		filters={"airline": airline},
		or_filters={"name": ("like", f"%{txt}%"), "role": ("like", f"%{txt}%")},
		limit=page_len,
		start=start,
	)
	return [(c["name"], c["role"]) for c in crew]

frappe.ui.form.on("Airplane Flight", {
	setup: function (frm) {
		frm.set_query("gate", () => ({
			filters: { status: "Available" },
		}));
	},
	airplane: function (frm) {
		frm.set_query("crew_members.crew_member", "crew_members", function () {
			if (!frm.doc.airplane) return {};
			return {
				query: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.get_crew_for_airline",
				filters: { airplane: frm.doc.airplane },
			};
		});
	},
});

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		if (frm.doc.status !== "Boarded") {
			// if (frm.is_new() || frm.is_dirty()) {
			frm.add_custom_button(__("Assign Seat"), function () {
				let d = new frappe.ui.Dialog({
					title: __("Assign Seat"),
					fields: [
						{
							fieldname: "seat",
							fieldtype: "Data",
							label: __("Seat Number"),
							reqd: 1,
						},
					],
					primary_action: function () {
						let values = d.get_values();
						if (values) {
							frm.set_value("seat", values.seat);
							d.hide();
						}
					},
				});
				d.show();
			});
		}
	},
});

// Copyright (c) 2026, Manish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lease Contract", {
	validate: function (frm) {
		if (frm.doc.end_date && frm.doc.start_date && frm.doc.end_date <= frm.doc.start_date) {
			frappe.throw(__("End date must be after start date"));
		}
	},
});

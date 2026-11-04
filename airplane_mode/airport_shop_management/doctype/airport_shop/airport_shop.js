frappe.ui.form.on("Airport Shop", {
	setup: function (frm) {
		frm.set_query("shop_type", () => ({
			filters: { enabled: 1 },
		}));
	},
});

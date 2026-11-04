import frappe


def get_context(context):
	shops = frappe.get_all(
		"Airport Shop",
		fields=["name", "shop_number", "shop_name", "airport", "shop_type", "area_sq_ft", "shop_status"],
		order_by="shop_name",
	)
	context.shops = shops
	context.total_shops = len(shops)
	context.available_shops = len([s for s in shops if s.shop_status == "Available"])
	context.occupied_shops = len([s for s in shops if s.shop_status == "Occupied"])

# Copyright (c) 2026, Manish and contributors
# For license information, please see license.txt

from datetime import timedelta

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class RentPayment(Document):
	def validate(self):
		self.auto_set_due_date()
		self.apply_late_fee()

	def auto_set_due_date(self):
		if not self.due_date and self.payment_month:
			month_start = getdate(self.payment_month)
			last_day = month_start.replace(day=28) + timedelta(days=4)
			last_day = last_day - timedelta(days=last_day.day - 1)
			self.due_date = last_day

	def apply_late_fee(self):
		if self.payment_date and self.due_date:
			if getdate(self.payment_date) > getdate(self.due_date):
				self.late_fee = 500
				self.payment_status = "Overdue"

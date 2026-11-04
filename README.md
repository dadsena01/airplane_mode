<div align="center" markdown="1">

<h1>Airplane Mode</h1>

**Airline operations and airport shop leasing, built on Frappe**

</div>

Airplane Mode is a Frappe app for running an airport. It covers airlines, flights, tickets and crew, and
the shops inside the airport that are leased to tenants.

### Modules

- **Airplane Mode**: airlines, airplanes, airports, gates, flights, crew, passengers and tickets
- **Airport Shop Management**: shops, shop types, tenants, lease contracts and rent payments

### Features

- Book tickets with add-ons. The ticket total is the flight price plus the add-ons.
- A ticket gets a random seat if none is set, and the seat is locked once the passenger has boarded
- Bookings stop when a flight reaches the airplane's capacity
- A ticket can only be submitted once its status is Boarded
- Gate status follows the flight, and a gate change is copied to every ticket on that flight
- Published flights get their own web page
- Lease contracts total the monthly rent and stop a shop being leased twice
- Submitting a contract marks its shops Occupied, and cancelling it marks them Available
- Rent payments get a due date at the end of the month and a late fee when paid after it
- Monthly rent reminder emails to tenants who have not paid, which you can switch off in Shop Settings
- Notifications one day before a flight departs and three days before a lease ends
- Web forms to book a ticket (`/book-flight-ticket`) and to ask about a shop (`/shop-inquiry`)
- Public shop pages at `/shops` and `/shop?name=<shop>`

### Reports

- **Revenue By Airline**: ticket revenue per airline, with a donut chart and a total
- **Add-on Popularity**: how often each add-on is sold
- **Airplanes By Airline**: airplanes grouped by airline

### Installation

You need Frappe 16 and Python 3.14 or later.

```bash
bench get-app https://github.com/dadsena01/airplane_mode --branch version-16
bench --site your.site install-app airplane_mode
```

Installing the app loads the default Shop Types from fixtures.

### Development

This app uses `pre-commit` with ruff, eslint, prettier and pyupgrade.

```bash
cd apps/airplane_mode
pre-commit install
```

Run the tests:

```bash
bench --site test_site set-config allow_tests true
bench --site test_site run-tests --app airplane_mode
```

### Support

Found a bug or have a question? [Open an issue](https://github.com/dadsena01/airplane_mode/issues).

#### License

MIT

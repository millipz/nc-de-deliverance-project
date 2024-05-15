from pg8000.native import literal
from db.connection import db


def seed(
    address,
    counterparty,
    currency,
    department,
    design,
    payment_type,
    payment,
    purchase_order,
    sales_order,
    staff,
    transaction,
):
    insert_address_data(address)
    insert_counterparty_data(counterparty)
    insert_currency_data(currency)
    insert_department_data(department)
    insert_design_data(design)
    insert_payment_type_data(payment_type)
    insert_staff_data(staff)
    insert_sales_order_data(sales_order)
    insert_purchase_order_data(purchase_order)
    insert_transaction_data(transaction)
    insert_payment_data(payment)


def insert_address_data(address):
    """Inserts address data"""
    start_of_query = """INSERT INTO address
    (address_id, address_line_1, address_line_2, district, city, postal_code,
    country, phone, created_at, last_updated)
    VALUES """

    values = ", ".join(
        [
            f"""({literal(addr['address_id'])},
                            {literal(addr['address_line_1'])},
                            {literal(addr['address_line_2'])},
                            {literal(addr['district'])},
                            {literal(addr['city'])},
                            {literal(addr['postal_code'])},
                            {literal(addr['country'])},
                            {literal(addr['phone'])},
                            {literal(addr['created_at'])},
                            {literal(addr['last_updated'])})"""
            for addr in address
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_counterparty_data(counterparty):
    """Inserts counterparty data"""
    start_of_query = """INSERT INTO counterparty
    (
        counterparty_id,
        counterparty_legal_name,
        legal_address_id,
        commercial_contact,
        delivery_contact,
        created_at, l
        ast_updated
    )
    VALUES """

    values = ", ".join(
        [
            f"""({literal(cpty['counterparty_id'])},
                            {literal(cpty['counterparty_legal_name'])},
                            {literal(cpty['legal_address_id'])},
                            {literal(cpty['commercial_contact'])},
                            {literal(cpty['delivery_contact'])},
                            {literal(cpty['created_at'])},
                            {literal(cpty['last_updated'])})"""
            for cpty in counterparty
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_currency_data(currency):
    """Inserts currency data"""
    start_of_query = """INSERT INTO currency
    (
        currency_id,
        currency_code,
        created_at,
        last_updated
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(curr['currency_id'])},
                {literal(curr['currency_code'])},
                {literal(curr['created_at'])},
                {literal(curr['last_updated'])}
            )"""
            for curr in currency
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_department_data(departments):
    """Inserts department data"""
    start_of_query = """INSERT INTO department
    (
        department_id,
        department_name,
        location,
        manager,
        created_at,
        last_updated
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(dept['department_id'])},
                {literal(dept['department_name'])},
                {literal(dept['location'])},
                {literal(dept['manager'])},
                {literal(dept['created_at'])},
                {literal(dept['last_updated'])}
            )"""
            for dept in departments
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_design_data(design):
    """Inserts design data"""
    start_of_query = """INSERT INTO design
    (
        design_id,
        created_at,
        design_name,
        file_location,
        file_name,
        last_updated
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(design['design_id'])},
                {literal(design['created_at'])},
                {literal(design['design_name'])},
                {literal(design['file_location'])},
                {literal(design['file_name'])},
                {literal(design['last_updated'])}
            )"""
            for design in design
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_payment_type_data(payment_types):
    """Inserts payment type data"""
    start_of_query = """INSERT INTO payment_type
    (
        payment_type_id,
        payment_type_name,
        created_at,
        last_updated
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(ptype['payment_type_id'])},
                {literal(ptype['payment_type_name'])},
                {literal(ptype['created_at'])},
                {literal(ptype['last_updated'])}
            )"""
            for ptype in payment_types
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_staff_data(staff_records):
    """Inserts staff data"""
    start_of_query = """INSERT INTO staff
    (
        staff_id,
        first_name,
        last_name,
        department_id,
        email_address,
        created_at,
        last_updated
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(staff['staff_id'])},
                {literal(staff['first_name'])},
                {literal(staff['last_name'])},
                {literal(staff['department_id'])},
                {literal(staff['email_address'])},
                {literal(staff['created_at'])},
                {literal(staff['last_updated'])}
            )"""
            for staff in staff_records
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_sales_order_data(sales_order):
    """Inserts sales order data"""
    start_of_query = """INSERT INTO sales_order
    (
        sales_order_id,
        created_at,
        last_updated,
        design_id,
        staff_id,
        counterparty_id,
        units_sold,
        unit_price,
        currency_id,
        agreed_delivery_date,
        agreed_payment_date,
        agreed_delivery_location_id
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(order['sales_order_id'])},
                {literal(order['created_at'])},
                {literal(order['last_updated'])},
                {literal(order['design_id'])},
                {literal(order['staff_id'])},
                {literal(order['counterparty_id'])},
                {literal(order['units_sold'])},
                {literal(order['unit_price'])},
                {literal(order['currency_id'])},
                {literal(order['agreed_delivery_date'])},
                {literal(order['agreed_payment_date'])},
                {literal(order['agreed_delivery_location_id'])}
            )"""
            for order in sales_order
        ]
    )

    query = start_of_query + values

    db.run(query)


def insert_purchase_order_data(purchase_orders):
    """Inserts purchase order data"""
    start_of_query = """INSERT INTO purchase_order
    (
        purchase_order_id,
        created_at,
        last_updated,
        staff_id,
        counterparty_id,
        item_code,
        item_quantity,
        item_unit_price,
        currency_id,
        agreed_delivery_date,
        agreed_payment_date,
        agreed_delivery_location_id
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(po['purchase_order_id'])},
                {literal(po['created_at'])},
                {literal(po['last_updated'])},
                {literal(po['staff_id'])},
                {literal(po['counterparty_id'])},
                {literal(po['item_code'])},
                {literal(po['item_quantity'])},
                {literal(po['item_unit_price'])},
                {literal(po['currency_id'])},
                {literal(po['agreed_delivery_date'])},
                {literal(po['agreed_payment_date'])},
                {literal(po['agreed_delivery_location_id'])}
            )"""
            for po in purchase_orders
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_transaction_data(transactions):
    """Inserts transaction data"""
    start_of_query = """INSERT INTO transaction
    (
        transaction_id,
        transaction_type,
        sales_order_id,
        purchase_order_id,
        created_at,
        last_updated
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(txn['transaction_id'])},
                {literal(txn['transaction_type'])},
                {literal(txn['sales_order_id'])},
                {literal(txn['purchase_order_id'])},
                {literal(txn['created_at'])},
                {literal(txn['last_updated'])}
            )"""
            for txn in transactions
        ]
    )

    query = start_of_query + values
    db.run(query)


def insert_payment_data(payments):
    """Inserts payment data"""
    start_of_query = """INSERT INTO payment
    (
        payment_id,
        created_at,
        last_updated,
        transaction_id,
        counterparty_id,
        payment_amount,
        currency_id,
        payment_type_id,
        paid,
        payment_date,
        company_ac_number,
        counterparty_ac_number
    )
    VALUES """

    values = ", ".join(
        [
            f"""(
                {literal(payment['payment_id'])},
                {literal(payment['created_at'])},
                {literal(payment['last_updated'])},
                {literal(payment['transaction_id'])},
                {literal(payment['counterparty_id'])},
                {literal(payment['payment_amount'])},
                {literal(payment['currency_id'])},
                {literal(payment['payment_type_id'])},
                {literal(payment['paid'])},
                {literal(payment['payment_date'])},
                {literal(payment['company_ac_number'])},
                {literal(payment['counterparty_ac_number'])}
            )"""
            for payment in payments
        ]
    )

    query = start_of_query + values
    db.run(query)

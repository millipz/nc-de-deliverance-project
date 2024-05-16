from db.data.address import address
from db.data.counterparty import counterparty
from db.data.currency import currency
from db.data.department import department
from db.data.design import design
from db.data.payment_type import payment_type
from db.data.payment import payment
from db.data.purchase_order import purchase_order
from db.data.sales_order import sales_order
from db.data.staff import staff
from db.data.transaction import transaction

index = ({
    "address": address,
    "counterparty": counterparty,
    "currency": currency,
    "department": department,
    "design": design,
    "payment_type": payment_type,
    "payment": payment,
    "purchase_order": purchase_order,
    "sales_order": sales_order,
    "staff": staff,
    "transaction": transaction
})
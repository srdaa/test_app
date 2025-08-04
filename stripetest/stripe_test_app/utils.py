from .models import Order

def order_line_items(order: Order):
    line_items = []
    for item in order.items_in_order:
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.item.title,
                        "description": item.item.description
                    },
                    "unit_amount": item.item.price

                },
                "quantity": item.quantity
            }
        )
    return line_items

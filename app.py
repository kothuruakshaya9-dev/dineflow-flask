from flask import Flask, render_template, request,session
from data.menu_data import menu

app = Flask(__name__)

cart = {}

CATEGORIES = [
    "Starters",
    "Rotis",
    "Curries",
    "Main Course",
    "Desserts",
    "Street Classics",
    "Beverages",
]


@app.route("/", methods=["GET", "POST"])
def menu_page():
    cat_index = int(request.args.get("cat", 0))
    category = CATEGORIES[cat_index]

    if request.method == "POST":
        item_id = int(request.form["item_id"])
        action = request.form["action"]

        if action == "add":
            cart[item_id] = cart.get(item_id, 0) + 1
        elif action == "remove" and item_id in cart:
            cart[item_id] -= 1
            if cart[item_id] == 0:
                del cart[item_id]

    return render_template(
        "menu.html",
        menu=menu,
        cart=cart,
        category=category,
        cat_index=cat_index,
        has_next=cat_index < len(CATEGORIES) - 1,
        has_prev=cat_index > 0,
    )


@app.route("/summary")
def summary():
    items = []
    total = 0

    for item_id, qty in cart.items():
        item = menu.get(item_id)
        if not item:
            continue

        amount = item["price"] * qty
        total += amount
        items.append(
            {
                "id": item_id,
                "name": item["name"],
                "qty": qty,
                "price": item["price"],
                "amount": amount,
            }
        )

    return render_template("summary.html", items=items, total=total)


@app.route("/remove/<int:item_id>")
def remove_item(item_id):
    if item_id in cart:
        del cart[item_id]
    return summary()


@app.route("/bill")
def bill():
    items = []
    subtotal = 0

    for item_id, qty in cart.items():
        item = menu.get(item_id)
        if not item:
            continue

        amount = item["price"] * qty
        subtotal += amount
        items.append((item["name"], qty, amount))

    tax = subtotal * 0.05
    total = subtotal + tax

    return render_template(
        "bill.html",
        items=items,
        subtotal=subtotal,
        tax=tax,
        total=total,
    )


if __name__ == "__main__":
    
    app.run()
import streamlit as st
import json
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Zafran Shop",
    page_icon="🛍️",
    layout="wide"
)

# =========================
# FILE
# =========================

path = "Products.json"


# =========================
# LOAD DATA
# =========================

def load_data():

    if not os.path.exists(path):
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(path, "w") as f:
            json.dump([], f, indent=4)

        return []

    try:
        with open(path, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        return []


data = load_data()


# =========================
# SAVE DATA
# =========================

def save_data():

    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# EMAIL CHECK
# =========================

def email_check(email):

    if "@" in email and ".com" in email:
        return True

    return False


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.dashboard-title {
    font-size: 36px;
    font-weight: 700;
    color: #172033;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 16px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
    border: 1px solid #eeeeee;
}

.card-title {
    color: #6b7280;
    font-size: 14px;
}

.card-value {
    color: #172033;
    font-size: 30px;
    font-weight: 700;
}

.section-title {
    font-size: 24px;
    font-weight: 650;
    color: #172033;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("# 🛍️ Zafran Shop")

    st.caption("E-Commerce Management System")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Register Customer",
            "🛒 Add Product",
            "➖ Remove Product",
            "🛍️ My Cart",
            "📦 Orders",
            "👥 Customers"
        ]
    )

    st.divider()

    st.caption("Zafran Shop")
    st.caption("Python + Streamlit")


# =========================
# DASHBOARD
# =========================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="dashboard-title">Welcome to Zafran Shop 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">E-Commerce Management Dashboard</div>',
        unsafe_allow_html=True
    )

    st.write("")

    total_customers = len(data)

    total_cart_items = sum(
        len(customer.get("cart", []))
        for customer in data
    )

    customers_with_cart = sum(
        1 for customer in data
        if len(customer.get("cart", [])) > 0
    )

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Total Customers</div>
                <div class="card-value">{total_customers}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Products in Carts</div>
                <div class="card-value">{total_cart_items}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Customers With Cart</div>
                <div class="card-value">{customers_with_cart}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Total Accounts</div>
                <div class="card-value">{total_customers}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Recent Customers

    st.markdown(
        '<div class="section-title">👥 Customers</div>',
        unsafe_allow_html=True
    )

    if data:

        customer_table = []

        for customer in data:

            customer_table.append({
                "Name": customer.get("name", ""),
                "Email": customer.get("email", ""),
                "ID Number": customer.get("id_no", ""),
                "Cart Items": len(customer.get("cart", []))
            })

        st.dataframe(
            customer_table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No customers registered yet.")


# =========================
# REGISTER CUSTOMER
# =========================

elif page == "👤 Register Customer":

    st.title("👤 Register Customer")

    st.write("Create a new customer account.")

    with st.form("register_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter customer name"
        )

        email = st.text_input(
            "Email",
            placeholder="example@gmail.com"
        )

        id_no = st.text_input(
            "ID Number",
            placeholder="Enter customer ID"
        )

        submit = st.form_submit_button(
            "Register Customer",
            use_container_width=True
        )

    if submit:

        name = name.strip()
        email = email.strip()
        id_no = id_no.strip()

        if not name or not email or not id_no:

            st.error("Please fill all fields.")

        elif not email_check(email):

            st.error("Invalid email address.")

        else:

            exists = False

            for customer in data:

                if customer["id_no"] == id_no:

                    exists = True
                    break

            if exists:

                st.warning("Customer already exists.")

            else:

                data.append({
                    "name": name.title(),
                    "email": email,
                    "id_no": id_no,
                    "cart": []
                })

                save_data()

                st.success(
                    "Customer registered successfully! 🎉"
                )


# =========================
# ADD PRODUCT
# =========================

elif page == "🛒 Add Product":

    st.title("🛒 Add Product To Cart")

    st.write("Add a product to a customer's shopping cart.")

    with st.form("add_product_form"):

        id_no = st.text_input(
            "Customer ID",
            placeholder="Enter customer ID"
        )

        product = st.text_input(
            "Product Name",
            placeholder="Enter product name"
        )

        submit = st.form_submit_button(
            "Add Product To Cart",
            use_container_width=True
        )

    if submit:

        id_no = id_no.strip()
        product = product.strip().title()

        if not id_no or not product:

            st.error("Please fill all fields.")

        else:

            customer_found = False

            for customer in data:

                if customer["id_no"] == id_no:

                    customer_found = True

                    customer["cart"].append(product)

                    save_data()

                    st.success(
                        f"'{product}' added to cart successfully! 🛒"
                    )

                    break

            if not customer_found:

                st.error("Customer ID not found.")


# =========================
# REMOVE PRODUCT
# =========================

elif page == "➖ Remove Product":

    st.title("➖ Remove Product From Cart")

    st.write("Remove a product from a customer's cart.")

    with st.form("remove_product_form"):

        id_no = st.text_input(
            "Customer ID",
            placeholder="Enter customer ID"
        )

        product = st.text_input(
            "Product Name",
            placeholder="Enter product name"
        )

        submit = st.form_submit_button(
            "Remove Product",
            use_container_width=True
        )

    if submit:

        id_no = id_no.strip()
        product = product.strip().title()

        customer_found = False

        for customer in data:

            if customer["id_no"] == id_no:

                customer_found = True

                if product in customer["cart"]:

                    customer["cart"].remove(product)

                    save_data()

                    st.success(
                        f"'{product}' removed successfully."
                    )

                else:

                    st.warning(
                        "This product is not in the customer's cart."
                    )

                break

        if not customer_found:

            st.error("Customer ID not found.")


# =========================
# MY CART
# =========================

elif page == "🛍️ My Cart":

    st.title("🛍️ My Cart")

    id_no = st.text_input(
        "Enter Customer ID",
        placeholder="Enter ID number"
    )

    if st.button(
        "🔍 Search Customer",
        use_container_width=True
    ):

        customer_found = False

        for customer in data:

            if customer["id_no"] == id_no.strip():

                customer_found = True

                st.success("Customer found!")

                st.subheader(
                    f"👤 {customer['name']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write("**Email**")
                    st.write(customer["email"])

                with col2:

                    st.write("**ID Number**")
                    st.write(customer["id_no"])

                st.divider()

                st.subheader("🛒 Shopping Cart")

                cart = customer.get("cart", [])

                if cart:

                    for number, product in enumerate(
                        cart,
                        start=1
                    ):

                        st.write(
                            f"**{number}.** {product}"
                        )

                    st.info(
                        f"Total Items: {len(cart)}"
                    )

                else:

                    st.info(
                        "🛒 Your cart is empty."
                    )

                break

        if not customer_found:

            st.error("Customer ID not found.")


# =========================
# ORDERS
# =========================

elif page == "📦 Orders":

    st.title("📦 Orders")

    st.write(
        "View customer shopping information."
    )

    if data:

        orders = []

        for customer in data:

            cart = customer.get("cart", [])

            orders.append({
                "Customer": customer["name"],
                "Email": customer["email"],
                "ID Number": customer["id_no"],
                "Products": ", ".join(cart)
                if cart else "Empty",
                "Total Items": len(cart)
            })

        st.dataframe(
            orders,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No customer data available.")


# =========================
# CUSTOMERS
# =========================

elif page == "👥 Customers":

    st.title("👥 Customers")

    st.write(
        "All registered customers."
    )

    if data:

        customers = []

        for customer in data:

            customers.append({
                "Name": customer["name"],
                "Email": customer["email"],
                "ID Number": customer["id_no"],
                "Cart Items": len(
                    customer.get("cart", [])
                )
            })

        st.dataframe(
            customers,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No customers registered yet.")

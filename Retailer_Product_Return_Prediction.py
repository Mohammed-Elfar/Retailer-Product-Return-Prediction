import streamlit as st
import pandas as pd
import pickle

# Load model
MODEL_PATH = '/Users/mohammedmahmood/Desktop/Data projects/Data science/Fresco Retailer Product Return Prediction/Retailer_Product_Return_Prediction (1).sav'
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

st.title("Retailer Product Return Prediction")
st.write("Enter product and transaction details to predict if a product will be returned.")

# --- User inputs --- 
quantity = st.selectbox("Quantity", options=[1, 2, 3, 4, 5])
unit_price = st.slider("Unit Price", min_value=70.0, max_value=1500.0, value=500.0, step=1.0)
price = quantity * unit_price  # Auto-calculated Price

tax = st.slider("Tax", min_value=7.35, max_value=787.5, value=50.0, step=0.01)
income = st.slider("Income", min_value=7157, max_value=159984, value=40000, step=1)

# Auto-calculated columns
tax_ratio = tax / price if price != 0 else 0
total_price = price + tax

# Show auto-calculated columns
st.markdown("### Auto-calculated fields")
col1, col2, col3 = st.columns(3)
col1.metric("Price (Quantity × Unit Price)", f"{price:.2f}")
col2.metric("Tax Rate", f"{tax_ratio:.3f}")
col3.metric("Price After Tax", f"{total_price:.2f}")

# --- Category mapping for dynamic subcategory ---
category_map = {
    'Bags': ['Mens', 'Women'],
    'Books': ['Academic', 'DIY', 'Fiction', 'Non-Fiction'],
    'Clothing': ['Mens', 'Women'],
    'Electronics': ['Audio and video', 'Cameras', 'Computers', 'Mobiles', 'Personal Appliances'],
    'Footwear': ['Kids', 'Mens', 'Women'],
    'Home and kitchen': ['Bath', 'Furnishing', 'Kitchen', 'Tools']
}

# Product category and dynamic subcategory
product_category = st.selectbox("Product Category", list(category_map.keys()))
product_subcategory = st.selectbox("Product Subcategory", category_map[product_category])

# Other inputs
reviews = st.slider("Reviews (rating)", min_value=1, max_value=5, value=3)

payment_mode = st.selectbox("Payment Mode", ['Mobile Payments', 'Credit Card', 'Debit Card', 'Cash'])
city = st.selectbox("City", ['Hyderabad', 'Bangalore', 'Kolkata', 'New Delhi', 'Chennai', 'Pune',
                             'Ahmedabad', 'Gurgaon', 'Vishakhapatnam', 'Mumbai'])

# --- Prediction ---
if st.button("Predict Product Return"):
    input_df = pd.DataFrame([{
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Tax": tax,
        "Reviews": reviews,
        "Income": income,
        "Price": price,
        "tax_ratio": tax_ratio,
        "total_price": total_price,
        "product_category": product_category,
        "Product_Subcategory": product_subcategory,
        "Payment_mode": payment_mode,
        "city": city
    }])

    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][1]  

    st.subheader("🔎 Prediction Result")
    if prediction == 1:
        st.error(f"⚠️ The product is **likely to be RETURNED** (Probability: {proba:.2%})")
    else:
        st.success(f"✅ The product is **likely NOT to be returned** (Probability: {1 - proba:.2%})")

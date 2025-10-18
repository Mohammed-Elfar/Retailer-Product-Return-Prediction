import streamlit as st
import pandas as pd
import pickle

# Load model
MODEL_PATH = '/Users/mohammedmahmood/Desktop/Data projects/Data science/Fresco Retailer Product Return Prediction/Retailer_Product_Return_Prediction.sav'
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

st.title("Retailer Product Return Prediction")
st.write("Enter product and transaction details to predict if a product will be returned.")

# --- User inputs ---
quantity = st.slider("Quantity", min_value=1, max_value=5, value=1)
unit_price = st.slider("Unit Price", min_value=70.0, max_value=1500.0, value=500.0, step=1.0)
tax = st.slider("Tax", min_value=7.35, max_value=787.5, value=50.0, step=0.01)
income = st.slider("Income", min_value=7157, max_value=159984, value=40000, step=1)
price = st.slider("Price", min_value=70.0, max_value=7500.0, value=1000.0, step=1.0)

# Auto-calculated columns
tax_ratio = tax / price if price != 0 else 0
total_price = price + tax

# Show auto-calculated columns nicely as metrics
st.markdown("### Auto-calculated fields")
col1, col2 = st.columns(2)
col1.metric("Tax Rate", f"{tax_ratio:.3f}")
col2.metric("Price After Tax", f"{total_price:.2f}")

# Other inputs
reviews = st.slider("Reviews (rating)", min_value=1, max_value=5, value=3)
month = st.selectbox("Month", ['January', 'February', 'March', 'April', 'May', 'June',
                               'July', 'August', 'September', 'October', 'November', 'December'])
product_category = st.selectbox("Product Category", ['Books', 'Clothing', 'Home and kitchen', 'Footwear', 'Bags', 'Electronics'])
product_subcategory = st.selectbox("Product Subcategory", ['Fiction', 'Women', 'Bath', 'Mens', 'Kitchen', 'Furnishing', 'Mobiles', 'DIY',
                                                           'Kids', 'Non-Fiction', 'Audio and video', 'Computers', 'Cameras', 'Tools',
                                                           'Academic', 'Personal Appliances'])
payment_mode = st.selectbox("Payment Mode", ['Mobile Payments', 'Credit Card', 'Debit Card', 'Cash'])
city = st.selectbox("City", ['Hyderabad', 'Bangalore', 'Kolkata', 'New Delhi', 'Chennai', 'Pune',
                             'Ahmedabad', 'Gurgaon', 'Vishakhapatnam', 'Mumbai'])

# Prepare data for prediction on button click
if st.button("Predict Product Return"):
    input_df = pd.DataFrame([{
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Tax": tax,
        "Reviews": reviews,
        "Income": income,
        "price": price,
        "tax_ratio": tax_ratio,
        "total_price": total_price,
        "Month": month,
        "product_category": product_category,
        "Product_Subcategory": product_subcategory,
        "Payment_mode": payment_mode,
        "city": city
    }])

    try:
        # proba = model.predict_proba(input_df)[0][1]
        prediction = model.predict(input_df)

        st.write(f"Predicted probability of return: ")

        if prediction[0] == 1:
            st.error(f"⚠️ The product is likely to be RETURNED. (Probability: ")
        else:
            st.success(f"✅ The product is likely NOT to be returned. )")
    except Exception as e:
        st.error(f"Error during prediction: {e}")
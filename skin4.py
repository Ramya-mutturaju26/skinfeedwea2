import streamlit as st
import requests
import sqlite3
import pandas as pd

# -----------------------------
# Weather Function
# -----------------------------
def get_weather(city, api_key):
    api_key="a5482befe9542069c10e8562404b6027"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        return data['main']['temp'], data['main']['humidity'], data['weather'][0]['description']
    return None, None, None

# -----------------------------
# Recommendation Logic
# -----------------------------
def recommend_product(skin_type, preference, temp, humidity, uv_index=7):
    if preference == "Mineral":
        return "Re’equil Sheer Zinc Tinted SPF 50 — dermatologist‑approved mineral sunscreen"
    elif preference == "Chemical":
        return "Neutrogena Ultra Sheer Dry Touch SPF 50 — lightweight chemical sunscreen"
    elif preference == "Hybrid":
        return "Minimalist SPF 50 Sunscreen — hybrid protection with zinc oxide + chemical filters"
    else:
        if uv_index > 6:
            return "Mineral Sunscreen SPF 50"
        elif skin_type == "dry" and humidity < 40:
            return "Hydrating Moisturizer"
        elif skin_type == "oily" and temp > 30:
            return "Lightweight Gel Moisturizer"
        else:
            return "Basic Non‑comedogenic Moisturizer"

# -----------------------------
# Feedback Database
# -----------------------------
def init_db():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (city TEXT, skin_type TEXT, preference TEXT, product TEXT, rating INTEGER)''')
    conn.commit()
    conn.close()

def save_feedback(city, skin_type, preference, product, rating):
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("INSERT INTO feedback VALUES (?, ?, ?, ?, ?)", (city, skin_type, preference, product, rating))
    conn.commit()
    conn.close()

def load_feedback():
    conn = sqlite3.connect("feedback.db")
    df = pd.read_sql_query("SELECT * FROM feedback", conn)
    conn.close()
    return df

# -----------------------------
# Professional Styling
# -----------------------------
style = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f7fa;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stHeader"] {
    background: #2c3e50;
    color: white;
}
h1, h2, h3 {
    color: #2c3e50;
}
.stButton>button {
    background-color: #2c3e50;
    color: white;
    border-radius: 5px;
}
</style>
"""
st.markdown(style, unsafe_allow_html=True)

# -----------------------------
# Navigation
# -----------------------------
st.sidebar.title("Dermatology Assistant")
page = st.sidebar.radio("Navigate:", ["Home", "Weather & Skincare", "Feedback Dashboard", "Dermatologist Insights"])

# -----------------------------
# Pages
# -----------------------------
if page == "Home":
    st.title("Dermatology‑Style Skincare App")
    st.write("Welcome to your professional skincare assistant. Navigate using the sidebar.")

elif page == "Weather & Skincare":
    st.title("Weather & Skincare Recommendations")
    city = st.text_input("Enter your city:")
    skin_type = st.selectbox("Select your skin type:", ["normal", "oily", "dry"])
    preference = st.radio("Choose sunscreen type:", ["Mineral", "Chemical", "Hybrid", "Moisturizer"])

    if st.button("Get Recommendation"):
        temp, humidity, description = get_weather(city, "YOUR_API_KEY")
        if temp is not None:
            product = recommend_product(skin_type, preference, temp, humidity)
            st.subheader("Weather Report")
            st.metric("Temperature", f"{temp} °C")
            st.metric("Humidity", f"{humidity} %")
            st.write(f"Condition: {description}")

            st.subheader("Dermatologist Recommendation")
            st.success(product)

            rating = st.slider("Rate this recommendation", 1, 5)
            if st.button("Save Feedback"):
                save_feedback(city, skin_type, preference, product, rating)
                st.success("Feedback saved successfully.")
        else:
            st.error("Could not fetch weather data. Check city/API key.")

elif page == "Feedback Dashboard":
    st.title("Feedback Dashboard")
    df = load_feedback()
    if not df.empty:
        st.write("### User Feedback Records")
        st.dataframe(df)

        st.write("### Ratings Distribution")
        st.bar_chart(df["rating"].value_counts())

        st.write("### Average Rating by Skin Type")
        avg_skin = df.groupby("skin_type")["rating"].mean()
        st.line_chart(avg_skin)

        st.write("### Average Rating by Preference")
        avg_pref = df.groupby("preference")["rating"].mean()
        st.bar_chart(avg_pref)
    else:
        st.info("No feedback yet.")

elif page == "Dermatologist Insights":
    st.title("Dermatologist Insights")
    st.write("""
    - Mineral sunscreens are best for sensitive or acne‑prone skin.
    - Chemical sunscreens are lightweight and good for daily wear.
    - Hybrid sunscreens balance protection and texture.
    - Always reapply sunscreen every 2–3 hours outdoors.
    """)

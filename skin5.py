import streamlit as st
import requests

# -----------------------------
# Weather Function
# -----------------------------
def get_weather(city, api_key):
    api_key = "a5482befe9542069c10e8562404b6027"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        data = requests.get(url).json()
        if "main" in data:
            return data['main']['temp'], data['main']['humidity'], data['weather'][0]['description']
    except Exception:
        pass
    return None, None, None

# -----------------------------
# Recommendation Logic
# -----------------------------
def recommend_product(skin_type, preference, temp, humidity, uv_index=7):
    if preference == "Mineral":
        if skin_type == "oily":
            return "Re’equil Sheer Zinc Tinted SPF 50 🌞"
        else:
            return "Earth Rhythm Mineral Sunscreen SPF 50 🌿"
    elif preference == "Chemical":
        if skin_type == "dry":
            return "Derma Co Hyaluronic Aqua Gel SPF 50 💧"
        else:
            return "Neutrogena Ultra Sheer Dry Touch SPF 50 ✨"
    elif preference == "Hybrid":
        return "Minimalist SPF 50 Sunscreen ⚡"
    else:
        if uv_index > 6:
            return "Mineral Sunscreen SPF 50 🌞"
        elif skin_type == "dry" and humidity < 40:
            return "Hydrating Moisturizer 💧"
        elif skin_type == "oily" and temp > 30:
            return "Lightweight Gel Moisturizer ✨"
        else:
            return "Basic Non-comedogenic Moisturizer 🌿"

# -----------------------------
# Professional Dark Mode UI Styling
# -----------------------------
professional_dark_bg = """
<style>
/* Main app container background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc !important;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
/* Sidebar background customization */
[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid #334155;
}
/* Header glassmorphism look */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
/* Style text elements to be readable on dark background */
h1, h2, h3, p, span, label {
    color: #f8fafc !important;
}
/* Polishing interactive buttons */
.stButton>button {
    background-color: #38bdf8 !important; /* Premium Cyan/Blue accent */
    color: #0f172a !important;
    border-radius: 6px !important;
    border: none !important;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #7dd3fc !important;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
}
/* Clean up input labels styling */
.stWidgetForm {
    background-color: rgba(30, 41, 59, 0.7);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 20px;
}
</style>
"""
st.markdown(professional_dark_bg, unsafe_allow_html=True)

# -----------------------------
# Multi-Page Navigation
# -----------------------------
st.sidebar.markdown("## 📊 Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Weather & Skincare", "Feedback Dashboard"])

# -----------------------------
# Page 1: Home
# -----------------------------
if page == "Home":
    st.title("🌤️ Skincare & Sunscreen Analytics")
    st.markdown("### Welcome to your weather-driven skincare assistant.")
    st.write(
        "This enterprise-grade application leverages real-time weather API metrics "
        "to diagnose and recommend optimal skin-protection products dynamically."
    )
    st.info("💡 Select **Weather & Skincare** in the sidebar to run a live recommendation engine.")

# -----------------------------
# Page 2: Weather & Skincare
# -----------------------------
elif page == "Weather & Skincare":
    st.title("🩺 Real-Time Recommendation Engine")
    
    api_key = "YOUR_API_KEY"
    
    with st.form("skincare_form"):
        city = st.text_input("📍 Enter your city:", placeholder="e.g., London, New York")
        skin_type = st.selectbox("Select skin profile:", ["normal", "oily", "dry"])
        preference = st.radio("Choose formulation preference:", ["Mineral", "Chemical", "Hybrid", "Moisturizer"])
        
        submit_button = st.form_submit_button("Generate Formulation Strategy")

    if submit_button:
        if not city:
            st.warning("Please specify a city name.")
        else:
            temp, humidity, description = get_weather(city, api_key)
            if temp is not None:
                product = recommend_product(skin_type, preference, temp, humidity)
                
                # Metrics layout
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Temperature", value=f"{temp} °C")
                with col2:
                    st.metric(label="Humidity", value=f"{humidity} %")
                
                st.success(f"**Current Atmosphere:** {description.title()}")
                st.info(f"**Recommended Product Solution:** {product}")
            else:
                st.error("Execution failed: Unable to fetch weather data. Please verify city name syntax.")

# -----------------------------
# Page 3: Feedback Dashboard
# -----------------------------
elif page == "Feedback Dashboard":
    st.title("📈 User Metrics Dashboard")
    st.write("Visualized user satisfaction rates and product preference distribution indexes.")
    st.bar_chart({"Sample Ratings": [3, 4, 5, 2, 5]})
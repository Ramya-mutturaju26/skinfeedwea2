import streamlit as st
import requests

# -----------------------------
# Weather Function
# -----------------------------
def get_weather(city, api_key):
    # Note: Hardcoded key inside function overrides the one passed from the UI
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
# Professional UI Styling
# -----------------------------
# Using a clean, subtle light-grey/blue gradient common in modern SaaS dashboards
professional_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e0e0e0;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
/* Style buttons to look sharper */
.stButton>button {
    background-color: #4A90E2 !important;
    color: white !important;
    border-radius: 6px !important;
    border: none !important;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #357ABD !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
"""
st.markdown(professional_bg, unsafe_allow_html=True)

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
    
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeather key if changing global execution
    
    # Wrap elements in a clean form structure
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
                
                # Metrics layout for professional analytical split
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
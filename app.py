import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Travel Genie AI", page_icon="🧞", layout="wide")

# --- 2. SECURITY: API SETUP ---
# Securely fetching from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception:
    st.error("API Key not found. Please add GEMINI_API_KEY to Streamlit Secrets.")

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Tries to load your real CSVs from GitHub
        hotels = pd.read_csv("hotel_details.csv")
        # Cleaning the 'Place' column for easier matching
        hotels['Place'] = hotels['Place'].str.lower()
        return hotels
    except Exception:
        # Fallback Mock Data so the app stays live if CSV is missing
        hotel_data = {
            'Hotel Name': ['Taj Palace', 'The Oberoi', 'FabHotel Prime'],
            'Rating': [9.5, 9.2, 7.5],
            'Place': ['delhi', 'bangalore', 'mumbai'],
            'Condition': ['Exceptional', 'Excellent', 'Good']
        }
        return pd.DataFrame(hotel_data)

hotel_df = load_data()

# --- 4. AI GENERATOR FUNCTION ---
def get_ai_itinerary(city, days, interests):
    prompt = f"""
    Act as a professional travel consultant. Create a detailed {days}-day itinerary for {city}.
    The user is specifically interested in: {interests}.
    Include morning, afternoon, and evening activities. 
    Format with bold headers and bullet points.
    """
    response = model.generate_content(prompt)
    return response.text

# --- 5. USER INTERFACE (SIDEBAR) ---
st.title("🧞 Travel Genie: AI Business Travel Architect")
st.markdown("---")

with st.sidebar:
    st.header("Trip Configuration")
    name = st.text_input("👤 Your Name", "Guest")
    dest = st.text_input("🌍 Destination City", "Bangalore")
    days = st.slider("📅 Duration (Days)", 1, 7, 3)
    interests = st.text_area("🎯 Interests", "Nature, History, Local Food")
    st.info("Hybrid AI: Gemini Plans + Local Dataset Hotels")

# --- 6. EXECUTION LOGIC ---
if st.button("Generate Professional Itinerary"):
    with st.spinner("Genie is crafting your journey..."):
        # Layout columns for a professional dashboard look
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"📍 {days}-Day Plan for {dest.title()}")
            # Call Gemini AI using the variables from the sidebar
            itinerary = get_ai_itinerary(dest, days, interests)
            st.markdown(itinerary)
            
        with col2:
            st.subheader("🏨 Accommodation")
            # Search local CSV/DataFrame for hotel recommendation
            filtered_h = hotel_df[hotel_df["Place"].str.contains(dest.lower(), na=False)]
            
            if not filtered_h.empty:
                top_h = filtered_h.sort_values(by="Rating", ascending=False).iloc[0]
                st.success(f"**Recommended:** {top_h['Hotel Name']}")
                st.write(f"⭐ Rating: {top_h['Rating']}")
                st.write(f"📝 Condition: {top_h['Condition']}")
            else:
                st.warning("No local hotel data found for this city. Check our Indian cities database!")

        st.divider()
        st.balloons()
        st.caption(f"Prepared for {name} | Powered by Gemini 1.5 Flash")

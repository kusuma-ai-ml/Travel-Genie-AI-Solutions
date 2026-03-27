import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Travel Genie AI", page_icon="🧞", layout="wide")

# --- 2. SECURITY: API SETUP ---
# Fetches your key safely from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("API Key not found. Please add GEMINI_API_KEY to Streamlit Secrets.")

# --- 3. DATA LOADING (WITH MOCK DATA FALLBACK) ---
@st.cache_data
def load_data():
    try:
        # Tries to load your real CSVs if they exist on GitHub
        hotels = pd.read_csv("hotel_details.csv")
        places = pd.read_csv("Top Indian Places to Visit.csv")
        hotels['Place'] = hotels['Place'].str.lower()
        return hotels, places
    except Exception:
        # Fallback Mock Data so the app never crashes for recruiters
        hotel_data = {
            'Hotel Name': ['Taj Palace', 'The Oberoi', 'FabHotel Prime'],
            'Rating': [9.5, 9.2, 7.5],
            'Place': ['delhi', 'bangalore', 'mumbai'],
            'Condition': ['Exceptional', 'Excellent', 'Good']
        }
        return pd.DataFrame(hotel_data), None

hotel_df, _ = load_data()

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
    name = st.text_input("👤 Your Name", "Professional")
    dest = st.text_input("🌍 Destination City", "Bangalore")
    days = st.slider("📅 Duration (Days)", 1, 7, 3)
    interests = st.text_area("🎯 Interests", "Nature, History, Local Food")
    st.info("This app uses a Hybrid RAG approach: AI for planning + Local Data for hotels.")

# --- 6. EXECUTION LOGIC ---
if st.button("Generate Professional Itinerary"):
    with st.spinner("Genie is crafting your journey..."):
        # Create columns for a professional dashboard look
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"📍 {days}-Day Plan for {dest.title()}")
            # Call Gemini AI
            itinerary = get_ai_itinerary(dest, days, interests)
            st.markdown(itinerary)
            
        with col2:
            st.subheader("🏨 Accommodation")
            # Search local CSV for hotel recommendation
            filtered_h = hotel_df[hotel_df["Place"].str.contains(dest.lower(), na=False)]
            
            if not filtered_h.empty:
                top_h = filtered_h.sort_values(by="Rating", ascending=False).iloc[0]
                st.success(f"**Recommended:** {top_h['Hotel Name']}")
                st.write(f"⭐ Rating: {top_h['Rating']}")
                st.write(f"📝 Condition: {top_h['Condition']}")
            else:
                st.warning("No local hotel data found for this city. Check our Indian cities database!")

        st.

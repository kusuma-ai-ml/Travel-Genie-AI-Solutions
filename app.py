import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. SETUP THE API (Safely retrieving from Secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Please set up the Gemini API Key in Streamlit Secrets!")

# 1. SETUP THE PAGE
st.set_page_config(page_title="Travel Genie", page_icon="🧞")

# 2. THE AI GENERATOR FUNCTION
def get_ai_itinerary(city, days, interests):
    prompt = f"""
    Act as a professional travel consultant. Create a {days}-day itinerary for {city}.
    The user is interested in: {', '.join(interests)}.
    Format the output with daily headers and bullet points.
    """
    response = model.generate_content(prompt)
    return response.text

# 3. LOAD YOUR DATA
@st.cache_data
def load_data():
    # --- Everything below is indented 4 spaces ---
    hotel_data = {
        'Hotel Name': ['Taj Palace', 'The Oberoi', 'FabHotel Prime'],
        'Rating': [9.5, 9.2, 7.5],
        'Place': ['delhi', 'bangalore', 'mumbai'],
        'Condition': ['Exceptional', 'Excellent', 'Good']
    }
    
    places_data = {
        'Name': ['Red Fort', 'Lalbagh Garden', 'Gateway of India'],
        'City': ['delhi', 'bangalore', 'mumbai'],
        'Type': ['Historical', 'Nature', 'Historical'],
        'time needed to visit in hrs': [3.0, 2.0, 1.5]
    }
    
    hotels = pd.DataFrame(hotel_data)
    places = pd.DataFrame(places_data)
    
    return hotels, places 


hotel_df, places_df = load_data()

# 4. INTERFACE
st.title("🧞 Travel Genie: AI Business Travel Architect")
st.write("Filling the gap between complex data and seamless travel.")

with st.sidebar:
    st.header("Trip Details")
    name = st.text_input("👤 Name", "Professional")
    dest = st.text_input("🌍 Destination", "Bangalore").lower()
    days = st.number_input("📅 Days", 1, 10, 3)
    hrs = st.number_input("⏱️ Sightseeing Hrs/Day", 1, 12, 6)

# 5. LOGIC (Your original logic converted for Web)
# 3. INTERFACE
if st.button("Generate Professional Itinerary"):
    with st.spinner("Genie is thinking..."):
        # This calls the AI function we created in Step B
        ai_plan = get_ai_itinerary(dest, days, user_input['interests'])
        st.markdown(ai_plan)
        
        # Local CSV lookup for the Hotel (using your existing data)
        hotel_df, _ = load_data()
        filtered_h = hotel_df[hotel_df["Place"].str.contains(dest.lower(), na=False)]
        
        if not filtered_h.empty:
            top_h = filtered_h.sort_values(by="Rating", ascending=False).iloc[0]
            st.success(f"🏨 Recommended Stay: {top_h['Hotel Name']}")
        else:
            st.info("AI suggested the plan! (Local hotel data for this city was not found).")
        st.info("Searching for local attractions...")

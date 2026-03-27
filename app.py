import streamlit as st
import pandas as pd

# 1. SETUP THE PAGE
st.set_page_config(page_title="Travel Genie", page_icon="🧞")

# 2. LOAD YOUR DATA
@st.cache_data
def load_data():
    # MOCK HOTEL DATA
    hotel_data = {
        'Hotel Name': ['Taj Palace', 'The Oberoi', 'FabHotel Prime'],
        'Rating': [9.5, 9.2, 7.5],
        'Place': ['delhi', 'bangalore', 'mumbai'],
        'Condition': ['Exceptional', 'Excellent', 'Good']
    }
# --- This part calls the function and saves the result into variables the app can use ---
hotel_df, places_df = load_data()

# --- Now the rest of your app will recognize 'hotel_df' and 'places_df' ---

if st.button("Generate Professional Itinerary"):
    filtered_h = hotel_df[hotel_df["Place"].str.contains(dest, na=False)]
    # ... the rest of your code ...
    # MOCK PLACES DATA
    places_data = {
        'Name': ['Red Fort', 'Lalbagh Garden', 'Gateway of India'],
        'City': ['delhi', 'bangalore', 'mumbai'],
        'Type': ['Historical', 'Nature', 'Historical'],
        'time needed to visit in hrs': [3.0, 2.0, 1.5]
    }
    
    hotels = pd.DataFrame(hotel_data)
    places = pd.DataFrame(places_data)
    return hotels, places

# 3. INTERFACE
st.title("🧞 Travel Genie: AI Business Travel Architect")
st.write("Filling the gap between complex data and seamless travel.")

with st.sidebar:
    st.header("Trip Details")
    name = st.text_input("👤 Name", "Professional")
    dest = st.text_input("🌍 Destination", "Bangalore").lower()
    days = st.number_input("📅 Days", 1, 10, 3)
    hrs = st.number_input("⏱️ Sightseeing Hrs/Day", 1, 12, 6)

# 4. LOGIC (Your original logic converted for Web)
if st.button("Generate Professional Itinerary"):
    # Filter hotels
    filtered_h = hotel_df[hotel_df["Place"].str.contains(dest, na=False)]
    
    if not filtered_h.empty:
        top_h = filtered_h.sort_values(by="Rating", ascending=False).iloc[0]
        st.success(f"🏨 Recommended Stay: {top_h['Hotel Name']}")
        st.write(f"Rating: {top_h['Rating']} | Condition: {top_h['Condition']}")
    else:
        st.warning("No hotel data found for this city.")

    # Filter places
    city_places = places_df[places_df["City"] == dest]
    if not city_places.empty:
        st.subheader("📍 Planned Sightseeing")
        for i, row in city_places.head(days * 2).iterrows():
            st.write(f"✅ {row['Name']} ({row['Type']})")
    else:
        st.info("Searching for local attractions...")

import streamlit as st
import pandas as pd

# 1. SETUP THE PAGE
st.set_page_config(page_title="Travel Genie", page_icon="🧞")

# 2. LOAD YOUR DATA
# This looks for the files you just uploaded to GitHub
@st.cache_data
def load_data():
    hotels = pd.read_csv("hotel_details.csv")
    places = pd.read_csv("Top Indian Places to Visit.csv")
    # Basic cleaning
    hotels['Place'] = hotels['Place'].str.lower()
    places['City'] = places['City'].str.lower()
    return hotels, places

hotel_df, places_df = load_data()

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

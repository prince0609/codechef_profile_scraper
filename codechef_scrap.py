import sys
import requests
from bs4 import BeautifulSoup
import streamlit as st

# ensure console output uses UTF-8
sys.stdout.reconfigure(encoding="utf-8")

def codechef_scraper(username):
    url = f"https://www.codechef.com/users/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if(not response):
       return None
    soup = BeautifulSoup(response.text, "html.parser")

    rating = soup.find('div', class_="rating-number")
    if rating:
        rating = rating.text.strip()
        highest_rating = soup.find('div', class_="rating-header text-center")
        highest_rating = highest_rating.find('small').text.split(' ')[2][:-1]
        ranks = soup.find('div', class_="rating-ranks")
        global_rank, country_rank = [strong.text for strong in ranks.find_all('strong')]
    else:
        rating = "Unrated"
        highest_rating = "Unrated"
        global_rank = "Unranked"
        country_rank = "Unranked"

    problem_solved_contest = soup.find('section', class_="rating-data-section problems-solved")
    problem_solved = (problem_solved_contest.find_all('h3'))[3].text.split(' ')[3]
    contest_participated = ((problem_solved_contest.find_all('h3'))[2].text.split(' ')[1])[1:-1]

    return {
        "Username": username,
        "Rating": rating,
        "Highest Rating": highest_rating,
        "Contests Participated": contest_participated,
        "Global Rank": global_rank,
        "Country Rank": country_rank,
        "Problems Solved": problem_solved
    }


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="CodeChef Profile Scraper", page_icon="🍴", layout="centered")

st.title("🍴 CodeChef Profile Scraper")

username = st.text_input("Enter CodeChef Username:")

if st.button("Fetch Profile"):
    if username.strip() == "":
        st.warning("⚠️ Please enter a username.")
    else:
        with st.spinner("Fetching data..."):
            try:
                data = codechef_scraper(username)
                if not data:
                    st.error("❌ Profile not found.")
                else:
                    st.success("✅ Profile data fetched!")

                # Display stats in nice cards
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Rating", data["Rating"])
                    st.metric("Highest Rating", data["Highest Rating"])
                    st.metric("Contests", data["Contests Participated"])
                with col2:
                    st.metric("Global Rank", data["Global Rank"])
                    st.metric("Country Rank", data["Country Rank"])
                    st.metric("Problems Solved", data["Problems Solved"])

            except Exception as e:
                st.error(f"❌ Error fetching data: {e}")

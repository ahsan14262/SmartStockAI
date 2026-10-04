import streamlit as st

st.title("About Us")
st.write("Meet the Smart Stock Agent team.")

team = [
    {
        "name": "Muhammad Kashif",
        "email": "mkashifansari579@gmail.com",
        "phone": "03308342284",
    },
    {
        "name": "Muhammad Ahsan",
        "email": "ahsan14262@gmail.com",
        "phone": None,
    },
    {
        "name": "Muhammad Zeeshan",
        "email": None,
        "phone": None,
    },
    {
        "name": "Muhammad Aamir Iqbal",
        "email": None,
        "phone": None,
    },
]

for member in team:
    st.subheader(member["name"])
    if member["email"]:
        st.write(f"📧 {member['email']}")
    if member["phone"]:
        st.write(f"📱 {member['phone']}")
    st.divider()

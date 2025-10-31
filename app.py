

import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# ---------- Configure Gemini ----------
genai.configure(api_key="Your API")
model = genai.GenerativeModel('gemini-1.5-pro')

# ---------- Sample User & Transaction Data ----------
users_df = pd.DataFrame({
    'user_id': [1, 2],
    'username': ['SallyLee', 'CooperGu'],
    'password': ['pass1234', 'abcd1234'],
    'email': ['sally@example.com', 'cooper@example.com']
})

transactions_df = pd.DataFrame({
    'transaction_id': [101, 102, 103, 201, 202],
    'user_id': [1, 1, 1, 2, 2],
    'amount': [500.0, 4000.0, 15.75, 100.0, 2500.0],
    'transaction_location': ['USA', 'France', 'USA', 'USA', 'Japan'],
    'transaction_date': pd.to_datetime(['2025-04-01', '2025-04-02', '2025-04-03', '2025-04-01', '2025-04-05']),
    'is_foreign': [False, True, False, False, True]
})

# ---------- Helper Functions ----------
def authenticate(username, password):
    user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
    if not user.empty:
        return int(user['user_id'].iloc[0])
    return None

def retrieve_user_profile(user_id):
    user_info = users_df[users_df['user_id'] == user_id].iloc[0]
    user_transactions = transactions_df[transactions_df['user_id'] == user_id].sort_values(by='transaction_date', ascending=False)
    return user_info, user_transactions

def build_prompt(user_info, transactions, user_input):
    summary = ", ".join(
        [f"${row['amount']} at {row['transaction_location']} on {row['transaction_date'].strftime('%Y-%m-%d')}"
         for _, row in transactions.iterrows()])

    prompt = (
        "You are a fraud assistant chatbot working for the bank. Speak as the bank using 'we' and 'our team'. Do not refer to the bank in the third person. "
        f"The user, {user_info['username']}, has recently made these transactions: {summary}. "
        f"The user asks: '{user_input}'. "
        "Provide a brief fraud risk assessment, then offer suggested next steps. End with: "
        "(1) Verify a specific transaction, (2) Learn how to prevent fraud, or (3) Report an issue. Wait for the user's choice before continuing."
    )
    return prompt

def follow_up_prompt(topic):
    if topic == "Verify a specific transaction":
        return (
            "You are a bank's AI assistant. The user wants to verify a suspicious transaction. "
            "Guide the user through confirming the merchant, location, and travel history. "
            "Speak as the bank, using phrases like 'we' and 'our system'. Do not tell the user to contact the bank — you *are* the bank."
        )
    elif topic == "Learn how to prevent fraud":
        return (
            "You are the bank's AI assistant. Provide proactive fraud prevention tips, such as enabling 2FA, using transaction alerts, and monitoring account activity. "
            "Use a friendly tone and speak as the bank. Avoid saying 'your bank' or referring to yourself in third person."
        )
    elif topic == "Report an issue":
        return (
            "The user wants to report suspicious activity. You are the bank's fraud assistant. Explain how the user can freeze their card, change passwords, and initiate a fraud report. "
            "Do NOT tell them to 'contact your bank'. You *are* the bank. Use phrases like 'we’ll take care of this' or 'we’ll freeze your account now'."
        )
    return "You are a helpful banking assistant. Continue the conversation in a helpful, friendly tone, staying in character as the user's bank."

def get_ai_response(prompt, history=[]):
    messages = [{"role": "user" if i % 2 == 0 else "model", "parts": [msg]} for i, msg in enumerate(history)]
    convo = model.start_chat(history=messages)
    response = convo.send_message(prompt)
    return response.text

# ---------- Streamlit UI ----------
st.set_page_config(page_title="MiniBank Fraud Chatbot", layout="centered")
st.title("🔐 MiniBank Fraud Detection Chatbot")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.history = []
    st.session_state.follow_up = False

if not st.session_state.authenticated:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_id = authenticate(username, password)
        if user_id:
            st.session_state.authenticated = True
            st.session_state.user_id = user_id
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
else:
    user_info, transactions = retrieve_user_profile(st.session_state.user_id)
    st.success(f"Hello, {user_info['username']}! You are now logged in.")

    if not st.session_state.follow_up:
        st.subheader("Ask about your account")
        user_input = st.text_input("Your question")

        if st.button("Ask") and user_input:
            prompt = build_prompt(user_info, transactions, user_input)
            response = get_ai_response(prompt, st.session_state.history)
            st.session_state.history.append(user_input)
            st.session_state.history.append(response)
            st.session_state.follow_up = True
            st.rerun()
    else:
        st.subheader("What would you like to do next?")
        option = st.radio("Choose one:", [
            "Verify a specific transaction",
            "Learn how to prevent fraud",
            "Report an issue"
        ])
        if st.button("Continue"):
            prompt = follow_up_prompt(option)
            response = get_ai_response(prompt, st.session_state.history)
            st.session_state.history.append(option)
            st.session_state.history.append(response)
            st.session_state.follow_up = False
            st.rerun()

    if st.session_state.history:
        st.markdown("---")
        st.subheader("Conversation History")
        for i in range(0, len(st.session_state.history), 2):
            st.markdown(f"**👤 You:** {st.session_state.history[i]}")
            st.markdown(f"**🤖 AI:** {st.session_state.history[i+1]}")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.history = []
        st.session_state.follow_up = False
        st.rerun()

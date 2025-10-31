# 🛡️ AI Fraud Detection Chatbot: A Guided Transaction Assistant

## 🌟 Project Overview

This project presents a prototype for an **AI-powered assistant chatbot** designed for the banking industry to enhance the user experience in reviewing transactions and detecting potential fraud.

The core idea is to move beyond passive fraud alerts by providing a guided, conversational interface. [cite_start]The chatbot reviews simulated user transaction data, flags unusual activity, and provides step-by-step guidance for verifying or reporting suspicious transactions[cite: 3].

[cite_start]This system demonstrates the practical application of **Generative AI** in a high-stakes financial setting, acting as a "real" bank assistant and laying the foundation for a more advanced fraud-prevention system[cite: 1, 3].

---

## ✨ Features

* [cite_start]**Simulated Authenticated Environment**: The chatbot simulates a secure banking environment with a login feature and personalized responses[cite: 4].
* [cite_start]**Gemini API Integration**: Uses **Google's Gemini API** to power the AI responses, enabling it to act in the voice of the bank (e.g., using "we" and "our system")[cite: 2, 4].
* [cite_start]**Transaction Review**: Helps users review their recent transactions and flag anything unusual[cite: 1].
* [cite_start]**Guided Fraud Verification**: Guides users step-by-step through verifying or reporting suspicious activity[cite: 1].
* [cite_start]**Interactive UI**: Built with **Python** and the **Streamlit** package for a clean, interactive user interface[cite: 2].

---

## 💻 Technology Stack

* **Language**: Python
* **Framework/UI**: Streamlit
* **AI Model**: Google Gemini API
* [cite_start]**Data**: Simulated and randomly generated transaction data [cite: 2]

---

## ⚙️ Installation and Setup

### Prerequisites

You need a Python environment and an API key for the Google Gemini API.

1.  **Get a Gemini API Key**: Obtain your key from Google AI Studio.
2.  **Set Environment Variable**: For security, set your API key as an environment variable named `GEMINI_API_KEY`.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [Your-Repo-Link-Here]
    cd [Your-Repo-Directory]
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your default web browser.

---

## 🔮 Future Development

This prototype demonstrates a strong proof-of-concept, but there is clear scope for further enhancement:

* [cite_start]**Real Database Integration**: Integrate a real SQL database instead of the current simulated dataset to handle actual banking transaction structures[cite: 5].
* [cite_start]**Improved Conversational Flexibility**: Enhance the Natural Language Understanding (NLU) to handle a broader range of general and financial queries, moving beyond only fraud-related questions[cite: 4, 5].
* [cite_start]**Visual AI Fraud Scoring**: Explore the integration of visual AI-driven fraud scoring for more robust detection[cite: 5].

---

## 👤 Author

* **Yenjo (Sally) Lee**

---

## 📜 License

[Choose and insert a license here, e.g., MIT License]

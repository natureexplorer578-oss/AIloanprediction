# AI-Driven Credit Scoring & Loan Decision Support System

## 📌 Project Overview

The AI-Driven Credit Scoring and Loan Decision Support System is a machine learning-based application that predicts loan approval status and estimates the eligible loan amount based on an applicant's financial and personal information.

The system combines Machine Learning and Generative AI to provide loan predictions along with easy-to-understand explanations, helping users better understand the predicted results.

## 🎯 Objectives

- Predict loan approval or rejection using machine learning.
- Estimate the eligible loan amount based on applicant details.
- Provide understandable explanations of prediction results using Generative AI.
- Build an interactive interface for users to enter details and view predictions.

## ⚙️ Key Features

- **Loan Amount Prediction:** Estimates the eligible loan amount using a regression model.
- **Loan Approval Prediction:** Uses a classification model to predict whether a loan is approved or rejected.
- **AI-Powered Explanations:** Integrates Google Gemini to generate natural-language explanations of prediction results.
- **Interactive Interface:** Allows users to enter financial details and view results through Streamlit.

## 🧠 Machine Learning Approach

The project uses two machine learning models:

1. **Regression:** Predicts the eligible loan amount.
2. **Classification:** Predicts the loan approval status.

Applicant details include annual income, CIBIL score, education, employment status, dependents, assets, and loan term.

## 🤖 Generative AI Integration

Google Gemini is integrated using the Google Gen AI Python SDK.

After the machine learning models generate their predictions, relevant applicant details and the prediction status are sent to Gemini through a prompt.

Gemini generates a natural-language explanation that is displayed in the application through the Loan AI Assistant.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Machine Learning:** Regression and Classification
- **Libraries:** Pandas, Joblib
- **Generative AI:** Google Gemini API
- **Frontend / Application:** Streamlit
- **Environment Management:** Python dotenv

## 🔄 Application Workflow

1. User enters personal and financial details.
2. The regression model predicts the eligible loan amount.
3. The classification model predicts the loan approval status.
4. The prediction details are passed to Google Gemini.
5. Gemini generates an explanation.
6. Streamlit displays the prediction and AI-generated explanation.

## 🚀 How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/natureexplorer578-oss/AIloanprediction.git
   ```

2. Navigate to the project directory:

   ```bash
   cd AIloanprediction
   ```

3. Install the required dependencies (add a requirements.txt file with your project's dependencies):

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your Google Gemini API key in a `.env` file:

   ```env
   GOOGLE_API_KEY=your_api_key
   ```

5. Run the application:

   ```bash
   streamlit run app.py
   ```


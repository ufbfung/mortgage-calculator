import streamlit as st
import requests
import json

def main():
    # Define FRED API key and base URL
    fred_api_key = 'ac53cf8d2bfd2dec1edc849ca32d3cbd'
    fred_base_url = 'https://api.stlouisfed.org/fred/'

    # Define the series ID for the most recent 30-year fixed-rate mortgage
    fred_series_id = 'MORTGAGE30US'

    # Define the API request URL
    fred_url = f'{fred_base_url}series/observations?series_id={fred_series_id}&api_key={fred_api_key}&file_type=json&limit=1&sort_order=desc'

    # Send the API request and parse the response JSON
    response = requests.get(fred_url)
    data = json.loads(response.content.decode())

    # Extract the most recent observation and the interest rate
    latest_observation = data['observations'][0]
    interest_rate = float(latest_observation['value'])

    # Set loan term to 30 years
    loan_term_years = 30

    # Get user input for mortgage amount and down payment as a percentage of the mortgage amount
    mortgage_amount = st.number_input('Enter the mortgage amount:', value=400000)
    down_payment_percent = st.slider('Enter the down payment as a percentage of the mortgage amount:', 0, 100, 20)

    # Convert down payment percentage to dollar amount
    down_payment = mortgage_amount * (down_payment_percent / 100)

    # Calculate the loan amount, number of monthly payments, and monthly interest rate
    loan_amount = mortgage_amount - down_payment
    loan_term_months = loan_term_years * 12
    monthly_interest_rate = (interest_rate / 100) / 12

    # Calculate the monthly mortgage payment
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-loan_term_months))

    # Print the monthly mortgage payment
    st.write(f'The monthly mortgage payment is ${monthly_payment:.2f}')

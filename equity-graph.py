import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta

st.sidebar.header('Mortgage Calculator')

total_cost = st.sidebar.slider('Total cost of the property', 100000, 1000000, 500000, 10000)
down_payment_percent = st.sidebar.slider('Down payment percentage', 1, 100, 20)

mortgage_interest_rate = st.sidebar.slider('Mortgage interest rate', 0.0, 10.0, 3.5, step=0.1)
mortgage_term_years = st.sidebar.slider('Mortgage term (years)', 1, 50, 30)

def calculate_equity_over_time(total_cost, down_payment_percent, mortgage_interest_rate, mortgage_term_years):
    down_payment = total_cost * down_payment_percent / 100
    loan_amount = total_cost - down_payment
    monthly_payment = (loan_amount * mortgage_interest_rate / 12) / (1 - (1 + mortgage_interest_rate / 12) ** (-mortgage_term_years * 12))

    equity = []
    months = []
    total_paid = 0
    remaining_balance = loan_amount

    while remaining_balance > 0:
        months.append(len(equity))
        equity_percent = (total_cost - remaining_balance) / total_cost * 100
        equity.append(equity_percent)

        interest_payment = remaining_balance * mortgage_interest_rate / 12
        principal_payment = monthly_payment - interest_payment
        total_paid += monthly_payment
        remaining_balance -= principal_payment

    fig, ax = plt.subplots()
    ax.plot(months, equity)
    ax.set_xlabel('Months')
    ax.set_ylabel('Equity Percentage')

    # Add markers for 25%, 50%, and 75% equity
    ax.axhline(y=25, color='gray', linestyle='--')
    ax.axhline(y=50, color='gray', linestyle='--')
    ax.axhline(y=75, color='gray', linestyle='--')

    return fig, equity

fig, equity = calculate_equity_over_time(total_cost, down_payment_percent/100, mortgage_interest_rate/100, mortgage_term_years)

st.pyplot(fig)

today = date.today()
years = None

for i, eq in enumerate(equity):
    if eq >= 25:
        dt = today + timedelta(days=(i * 30))
        years = int((dt - today).days / 365.25)
        st.write(f"You will have 25% equity on {dt.strftime('%Y-%m-%d')} ({years} years from today).")
        break
else:
    st.write('You will not have 25% equity.')

for i, eq in enumerate(equity):
    if eq >= 50:
        dt = today + timedelta(days=(months[i] * 30))
        years = int((dt - today).days / 365.25)
        st.write(f"You will have 50% equity on {dt.strftime('%Y-%m-%d')} ({years} years from today).")
        break
else:
    st.write('You will not have 50% equity.')

for i, eq in enumerate(equity):
    if eq >= 75:
        dt = today + timedelta(days=(months[i] * 30))
        years = int((dt - today).days / 365.25)
        st.write(f"You will have 75% equity on {dt.strftime('%Y-%m-%d')} ({years} years from today).")
        break
else:
    st.write('You will not have 75% equity.')

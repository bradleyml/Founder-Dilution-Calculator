import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_dilution(initial_equity, funding_rounds):
    """
    Calculates founder equity dilution over multiple funding rounds.
    
    Parameters:
    - initial_equity: float, founder's initial equity (as a percentage, e.g., 100 for full ownership)
    - funding_rounds: list of tuples, each tuple represents (investment amount, post-money valuation)
    
    Returns:
    - DataFrame showing equity dilution after each round
    """
    equity = initial_equity
    dilution_data = []
    
    for round_num, (investment, valuation) in enumerate(funding_rounds, start=1):
        new_equity = equity * (1 - (investment / valuation))
        dilution_data.append([f'Round {round_num}', investment, valuation, equity, new_equity])
        equity = new_equity
    
    df = pd.DataFrame(dilution_data, columns=["Round", "Investment", "Post-Money Valuation", "Pre-Round Equity (%)", "Post-Round Equity (%)"])
    return df

def plot_dilution(df):
    """Plots the founder's equity dilution over rounds."""
    fig, ax = plt.subplots()
    ax.plot(df['Round'], df['Post-Round Equity (%)'], marker='o', linestyle='-', color='b', label='Founder Equity')
    ax.set_xlabel("Funding Round")
    ax.set_ylabel("Equity (%)")
    ax.set_title("Founder Equity Dilution Over Rounds")
    ax.grid()
    ax.legend()
    st.pyplot(fig)

def main():
    """Streamlit app for founder dilution assessment."""
    st.title("Founder Dilution Calculator")
    initial_equity = st.number_input("Enter founder's initial equity percentage", min_value=0.0, max_value=100.0, value=100.0)
    num_rounds = st.number_input("Enter number of funding rounds", min_value=1, value=1, step=1)
    
    funding_rounds = []
    for i in range(num_rounds):
        st.subheader(f"Round {i+1}")
        investment = st.number_input(f"Investment amount for Round {i+1}", min_value=0.0, value=500000.0, step=10000.0)
        valuation = st.number_input(f"Post-money valuation for Round {i+1}", min_value=investment, value=5000000.0, step=10000.0)
        funding_rounds.append((investment, valuation))
    
    if st.button("Calculate Dilution"):
        df = calculate_dilution(initial_equity, funding_rounds)
        st.write("### Equity Dilution Report:")
        st.dataframe(df)
        plot_dilution(df)

if __name__ == "__main__":
    main()

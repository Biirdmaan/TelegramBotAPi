import streamlit as st
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv
import plotly.express as px

# Load environment variables
load_dotenv()

def init_supabase():
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    return create_client(url, key)

def load_data():
    supabase = init_supabase()
    response = supabase.table('wallet_transactions').select("*").execute()
    return pd.DataFrame(response.data)

def main():
    st.title("Wallet Transactions Dashboard")
    
    # Load data
    df = load_data()
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transactions", len(df))
    with col2:
        st.metric("Open Positions", len(df[df['status'] == 'Open']))
    with col3:
        st.metric("Closed Positions", len(df[df['status'] == 'Closed']))
    
    # Transactions table
    st.subheader("Recent Transactions")
    st.dataframe(df)
    
    # ROI Distribution
    st.subheader("ROI Distribution")
    df['roi_clean'] = df['roi_percentage'].str.rstrip('%').astype(float)
    st.bar_chart(df['roi_clean'])
    
    # Status breakdown using plotly
    st.subheader("Status Breakdown")
    status_counts = df['status'].value_counts()
    fig = px.pie(values=status_counts.values, names=status_counts.index, title='Transaction Status')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main() 
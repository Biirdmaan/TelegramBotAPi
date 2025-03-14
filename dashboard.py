import streamlit as st
import pandas as pd
from supabase import create_client
import plotly.express as px
import asyncio
from telegram_bot_client import TelegramBotClient
from store_csv_to_supabase import process_csv_to_supabase
import re
import time

def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def load_data():
    """Load all wallet data from Supabase"""
    try:
        supabase = init_supabase()
        response = supabase.table('wallet_transactions').select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def validate_wallet_address(address):
    """Validate the wallet address format"""
    pattern = r'^[A-Za-z0-9]{44}$'
    return bool(re.match(pattern, address))

async def fetch_new_wallet_data(wallet_address, status_placeholder):
    """Fetch data for a new wallet address"""
    client = None
    try:
        # Set a timeout for the entire operation
        async with asyncio.timeout(30):
            print("DEBUG: Starting fetch process...")  # Terminal debug message
            status_placeholder.info('Fetching wallet data...')  # User message
            
            try:
                client = TelegramBotClient()
                print("DEBUG: Client initialized")
            except Exception as e:
                print(f"DEBUG: Failed to initialize client: {str(e)}")
                status_placeholder.error("Failed to connect to service")
                return False
            
            try:
                print("DEBUG: Attempting to start client...")
                await asyncio.wait_for(client.start(), timeout=10)
                print("DEBUG: Client started successfully")
            except asyncio.TimeoutError:
                print("DEBUG: Timeout during client.start()")
                status_placeholder.error("Connection timeout. Please try again.")
                return False
            except Exception as e:
                print(f"DEBUG: Error during client.start(): {str(e)}")
                return False
            
            try:
                print("DEBUG: Sending command to get file...")
                csv_path = await asyncio.wait_for(
                    client.send_command_and_get_file(wallet_address, wait_time=25),
                    timeout=30
                )
                print(f"DEBUG: Got response, csv_path: {csv_path}")
                
                if not csv_path:
                    print("DEBUG: No CSV path returned")
                    status_placeholder.error("No data available for this wallet")
                    return False
                
                print("DEBUG: Attempting to store in database...")
                success = process_csv_to_supabase(wallet_address)
                
                if not success:
                    print("DEBUG: Failed to store in database")
                    status_placeholder.error("Failed to store wallet data")
                    return False
                
                print("DEBUG: Data stored successfully")
                status_placeholder.success("✅ Wallet data added successfully!")
                return True
                
            except asyncio.TimeoutError:
                print("DEBUG: Timeout while getting file")
                status_placeholder.error("Request timeout. Please try again.")
                return False
            except Exception as e:
                print(f"DEBUG: Error getting data: {str(e)}")
                if "limit of 3 requests per day" in str(e):
                    status_placeholder.warning("⚠️ Rate limit reached: You have reached the limit of 3 requests per day!")
                else:
                    status_placeholder.error("Failed to fetch wallet data")
                return False
            
    except Exception as e:
        print(f"DEBUG: Top level error: {str(e)}")
        status_placeholder.error("An error occurred")
        return False
    finally:
        if client:
            try:
                print("DEBUG: Attempting to close client...")
                await asyncio.wait_for(client.close(), timeout=5)
                print("DEBUG: Client closed successfully")
            except Exception as e:
                print(f"DEBUG: Error closing client: {str(e)}")

def set_page_config():
    """Configure the Streamlit page"""
    st.set_page_config(
        page_title="Solana Wallet Analyzer",
        page_icon="💎",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def local_css():
    """Add custom CSS"""
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #9945FF;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
        }
        .metric-card {
            background-color: #1E1E1E;
            border-radius: 0.5rem;
            padding: 1rem;
            border: 1px solid #333;
        }
        .wallet-input {
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 0.5rem;
            padding: 0.5rem;
        }
        h1 {
            color: #9945FF;
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 2rem;
        }
        h2 {
            color: #14F195;
            font-size: 1.5rem;
            font-weight: 500;
        }
        .stDataFrame {
            border: 1px solid #333;
            border-radius: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def display_wallet_data(df, selected_wallet):
    """Display data for selected wallet"""
    wallet_df = df[df['wallet_address'] == selected_wallet]
    
    # Calculate ROI first
    if not wallet_df.empty:
        wallet_df['roi_clean'] = wallet_df['roi_percentage'].str.rstrip('%').astype(float)
        avg_roi = wallet_df['roi_clean'].mean()
    else:
        avg_roi = 0
    
    # Summary metrics in modern cards
    st.markdown("### Portfolio Overview")
    metrics_container = st.container()
    with metrics_container:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container():
                st.markdown("""
                    <div class="metric-card">
                        <h4 style="color: #14F195;">Total Transactions</h4>
                        <h2 style="color: white;">{}</h2>
                    </div>
                """.format(len(wallet_df)), unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown("""
                    <div class="metric-card">
                        <h4 style="color: #14F195;">Open Positions</h4>
                        <h2 style="color: white;">{}</h2>
                    </div>
                """.format(len(wallet_df[wallet_df['status'] == 'Open'])), unsafe_allow_html=True)
        
        with col3:
            with st.container():
                st.markdown("""
                    <div class="metric-card">
                        <h4 style="color: #14F195;">Closed Positions</h4>
                        <h2 style="color: white;">{}</h2>
                    </div>
                """.format(len(wallet_df[wallet_df['status'] == 'Closed'])), unsafe_allow_html=True)
        
        with col4:
            with st.container():
                st.markdown("""
                    <div class="metric-card">
                        <h4 style="color: #14F195;">Average ROI</h4>
                        <h2 style="color: white;">{:.2f}%</h2>
                    </div>
                """.format(avg_roi), unsafe_allow_html=True)

    # Charts section
    st.markdown("### Analytics")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # ROI Distribution with Plotly
        if not wallet_df.empty:
            fig_roi = px.histogram(
                wallet_df, 
                x='roi_clean',
                nbins=20,
                title='ROI Distribution',
                labels={'roi_clean': 'ROI (%)', 'count': 'Number of Transactions'},
                color_discrete_sequence=['#9945FF']
            )
            fig_roi.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF'
            )
            st.plotly_chart(fig_roi, use_container_width=True)

    with chart_col2:
        # Status breakdown with Plotly
        status_counts = wallet_df['status'].value_counts()
        if not status_counts.empty:
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title='Position Status',
                color_discrete_sequence=['#14F195', '#9945FF', '#FF3B3B']
            )
            fig_status.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF'
            )
            st.plotly_chart(fig_status, use_container_width=True)

    # Transactions table with modern styling
    st.markdown("### Recent Transactions")
    st.dataframe(
        wallet_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "roi_percentage": st.column_config.NumberColumn(
                "ROI",
                format="%.2f%%"
            ),
            "status": st.column_config.TextColumn(
                "Status",
                help="Current position status"
            )
        }
    )

def main():
    set_page_config()
    local_css()
    
    st.title("Solana Wallet Transaction Analyzer")
    
    # Load existing data
    df = load_data()
    existing_wallets = sorted(df['wallet_address'].unique()) if not df.empty else []
    
    # Create two columns with better proportions
    col1, col2 = st.columns([1, 4])
    
    # Left column for new wallet input
    with col1:
        st.markdown("### Add New Wallet")
        new_wallet = st.text_input(
            "Wallet Address (44 characters)",
            key="wallet_input",
            help="Enter a valid Solana wallet address"
        )
        fetch_button = st.button("🔍 Fetch Wallet Data")
        
        # Create a placeholder for status messages
        status_placeholder = st.empty()
        
        if fetch_button:
            if validate_wallet_address(new_wallet):
                try:
                    with st.spinner('🔄 Processing...'):
                        success = asyncio.run(fetch_new_wallet_data(new_wallet, status_placeholder))
                        if success:
                            time.sleep(1)
                            st.experimental_rerun()
                except Exception as e:
                    print(f"DEBUG: Error in main: {str(e)}")
                    status_placeholder.error("🚫 Service temporarily unavailable")
            else:
                status_placeholder.error("❌ Invalid wallet address format")
    
    # Right column for existing wallet data
    with col2:
        if existing_wallets:
            selected_wallet = st.selectbox(
                "Select Wallet Address",
                existing_wallets,
                index=0,
                help="Choose a wallet to view its transactions"
            )
            display_wallet_data(df, selected_wallet)
        else:
            st.info("💡 No wallet data available. Add a new wallet using the form on the left.")

if __name__ == "__main__":
    main() 
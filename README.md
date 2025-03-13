# Solana Wallet Transaction Analyzer

A Python application that fetches Solana wallet transaction data from a Telegram bot, stores it in a Supabase database, and visualizes it through an interactive dashboard.

## Features

- **Wallet Transaction Fetching**: Get transaction data for any Solana wallet address via Telegram bot
- **Data Storage**: Automatically stores transaction data in Supabase with wallet address tracking
- **Interactive Dashboard**: Visualize transaction data with:
  - Transaction metrics and statistics
  - ROI distribution charts
  - Status breakdown pie charts
  - Detailed transaction tables
  - Multi-wallet comparison support

## Prerequisites

- Python 3.7+
- Telegram API credentials (API_ID and API_HASH)
- Supabase account and project credentials
- Solana wallet address to analyze

## Installation

1. Clone the repository:3
bash
git clone <your-repo-url>
cd solana-wallet-analyzer

2. Install dependencies:
bash
pip install -r requirements.txt

3. Configure environment variables:

env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE_NUMBER=your_phone_number
BOT_USERNAME=walletx_solana_bot
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key


4. Run the application:
bash
python main.py        


## Usage

1. Run the main application:
bash
python main.py


2. Enter a valid Solana wallet address when prompted (44 characters)

3. The application will:
   - Connect to the Telegram bot
   - Download transaction data
   - Store it in Supabase
   - Launch the dashboard automatically

4. View your transaction data in the dashboard that opens in your browser

## Project Structure

- `main.py`: Main application entry point
- `telegram_bot_client.py`: Handles Telegram bot interactions
- `store_csv_to_supabase.py`: Manages data storage in Supabase
- `inspect_csv.py`: CSV file processing and validation
- `dashboard.py`: Streamlit dashboard for data visualization

## Database Schema

The Supabase database includes the following columns:
- `wallet_address`: The Solana wallet address
- `token_name`: Name of the token
- `token_address`: Token contract address
- `status`: Transaction status (Open/Closed)
- `roi_percentage`: Return on Investment
- `profit_sol`: Profit in SOL
- And more transaction details...

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Supabase](https://supabase.com/)
- [Streamlit](https://streamlit.io/)

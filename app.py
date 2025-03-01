import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import asyncio
from app.utils.price_fetcher import PriceFetcher
from app.utils.arbitrage_finder import ArbitrageFinder
from app.utils.blockchain_interface import BlockchainInterface
from app.components.dashboard import render_dashboard
from app.components.trade_executor import render_trade_executor
from app.components.settings import render_settings

st.set_page_config(
    page_title="Cross-Chain Arbitrage Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ArbitrageBot:
    def __init__(self):
        self.price_fetcher = PriceFetcher()
        self.arbitrage_finder = ArbitrageFinder()
        self.blockchain_interface = BlockchainInterface()
        
        if 'opportunities' not in st.session_state:
            st.session_state.opportunities = []
        if 'active_trades' not in st.session_state:
            st.session_state.active_trades = []
        if 'historical_trades' not in st.session_state:
            st.session_state.historical_trades = []

    def main(self):
        st.title("🤖 Cross-Chain Arbitrage Bot")
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Dashboard", "Trade Executor", "Settings"])
        
        if page == "Dashboard":
            render_dashboard(self)
        elif page == "Trade Executor":
            render_trade_executor(self)
        else:
            render_settings(self)

    async def scan_opportunities(self):
        """Scan for arbitrage opportunities across chains"""
        opportunities = await self.arbitrage_finder.find_opportunities()
        return opportunities

    async def execute_trade(self, opportunity):
        """Execute a cross-chain arbitrage trade"""
        return await self.blockchain_interface.execute_arbitrage(opportunity)

    def update_opportunities(self):
        """Update the list of current arbitrage opportunities"""
        opportunities = asyncio.run(self.scan_opportunities())
        st.session_state.opportunities = opportunities

if __name__ == "__main__":
    bot = ArbitrageBot()
    bot.main() 
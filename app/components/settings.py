import streamlit as st
from web3 import Web3
import json

def render_settings(bot):
    """Render the settings interface"""
    tab1, tab2, tab3 = st.tabs(["Wallet", "Networks", "Trading"])
    
    with tab1:
        render_wallet_settings(bot)
    
    with tab2:
        render_network_settings(bot)
    
    with tab3:
        render_trading_settings(bot)

def render_wallet_settings(bot):
    """Render wallet configuration settings"""
    st.subheader("🔑 Wallet Configuration")
    
    # Wallet connection
    wallet_address = st.text_input(
        "Wallet Address",
        value=st.session_state.get("wallet_address", ""),
        placeholder="0x..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        private_key = st.text_input(
            "Private Key",
            value=st.session_state.get("private_key", ""),
            type="password"
        )
    
    with col2:
        if st.button("Connect Wallet"):
            connect_wallet(bot, wallet_address, private_key)
    
    # Balances
    st.subheader("💰 Wallet Balances")
    render_wallet_balances(bot)

def render_network_settings(bot):
    """Render network configuration settings"""
    st.subheader("⛓️ Network Configuration")
    
    networks = {
        "Ethereum": {
            "rpc": st.text_input("Ethereum RPC URL", value=st.session_state.get("eth_rpc", "")),
            "enabled": st.checkbox("Enable Ethereum", value=True)
        },
        "BSC": {
            "rpc": st.text_input("BSC RPC URL", value=st.session_state.get("bsc_rpc", "")),
            "enabled": st.checkbox("Enable BSC", value=True)
        },
        "Polygon": {
            "rpc": st.text_input("Polygon RPC URL", value=st.session_state.get("polygon_rpc", "")),
            "enabled": st.checkbox("Enable Polygon", value=True)
        },
        "Avalanche": {
            "rpc": st.text_input("Avalanche RPC URL", value=st.session_state.get("avax_rpc", "")),
            "enabled": st.checkbox("Enable Avalanche", value=True)
        }
    }
    
    if st.button("Save Network Settings"):
        save_network_settings(bot, networks)

def render_trading_settings(bot):
    """Render trading configuration settings"""
    st.subheader("📊 Trading Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input(
            "Default Trade Size (USD)",
            min_value=100,
            max_value=1000000,
            value=st.session_state.get("default_trade_size", 1000),
            key="default_trade_size"
        )
        
        st.number_input(
            "Gas Price Multiplier",
            min_value=1.0,
            max_value=2.0,
            value=st.session_state.get("gas_multiplier", 1.1),
            step=0.1,
            key="gas_multiplier"
        )
    
    with col2:
        st.number_input(
            "Maximum Slippage (%)",
            min_value=0.1,
            max_value=5.0,
            value=st.session_state.get("max_slippage", 1.0),
            step=0.1,
            key="max_slippage"
        )
        
        st.number_input(
            "Minimum Profit Threshold (%)",
            min_value=0.1,
            max_value=10.0,
            value=st.session_state.get("min_profit", 0.5),
            step=0.1,
            key="min_profit"
        )
    
    # Flash loan settings
    st.subheader("⚡ Flash Loan Settings")
    
    st.checkbox(
        "Enable Flash Loans",
        value=st.session_state.get("enable_flash_loans", True),
        key="enable_flash_loans"
    )
    
    if st.session_state.enable_flash_loans:
        col3, col4 = st.columns(2)
        
        with col3:
            st.selectbox(
                "Flash Loan Provider",
                options=["Aave", "dYdX", "Uniswap V3"],
                index=0,
                key="flash_loan_provider"
            )
        
        with col4:
            st.number_input(
                "Maximum Flash Loan Size (USD)",
                min_value=1000,
                max_value=10000000,
                value=st.session_state.get("max_flash_loan", 100000),
                step=1000,
                key="max_flash_loan"
            )
    
    if st.button("Save Trading Settings"):
        save_trading_settings(bot)

def render_wallet_balances(bot):
    """Render wallet balances across chains"""
    if not st.session_state.get("wallet_address"):
        st.info("Connect wallet to view balances")
        return
    
    balances = get_wallet_balances(bot)
    
    for chain, tokens in balances.items():
        with st.expander(f"{chain} Balances", expanded=True):
            for token, amount in tokens.items():
                st.write(f"**{token}:** {amount}")

def connect_wallet(bot, address: str, private_key: str):
    """Connect and validate wallet"""
    try:
        # Validate address format
        if not Web3.is_address(address):
            st.error("Invalid wallet address format")
            return
        
        # Store wallet info securely
        st.session_state.wallet_address = address
        st.session_state.private_key = private_key  # In production, handle this more securely
        
        st.success("Wallet connected successfully!")
        
    except Exception as e:
        st.error(f"Error connecting wallet: {str(e)}")

def save_network_settings(bot, networks: dict):
    """Save network configuration"""
    try:
        # Update RPC endpoints
        for network, config in networks.items():
            if config["enabled"]:
                st.session_state[f"{network.lower()}_rpc"] = config["rpc"]
        
        st.success("Network settings saved successfully!")
        
    except Exception as e:
        st.error(f"Error saving network settings: {str(e)}")

def save_trading_settings(bot):
    """Save trading configuration"""
    try:
        # Settings are automatically saved in session_state
        st.success("Trading settings saved successfully!")
        
    except Exception as e:
        st.error(f"Error saving trading settings: {str(e)}")

def get_wallet_balances(bot) -> dict:
    """Get wallet balances across all chains"""
    # This would be implemented with actual blockchain queries
    # Placeholder implementation
    return {
        "Ethereum": {
            "ETH": "1.5 ETH",
            "USDT": "5000 USDT",
            "USDC": "5000 USDC"
        },
        "BSC": {
            "BNB": "10 BNB",
            "BUSD": "5000 BUSD"
        },
        "Polygon": {
            "MATIC": "1000 MATIC",
            "USDC": "5000 USDC"
        }
    } 
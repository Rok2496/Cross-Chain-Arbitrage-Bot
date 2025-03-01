import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

def render_trade_executor(bot):
    """Render the trade executor interface"""
    st.subheader("🔄 Active Trades")
    render_active_trades(bot)
    
    st.subheader("📝 Trade History")
    render_trade_history(bot)
    
    st.subheader("⚙️ Trade Settings")
    render_trade_settings(bot)

def render_active_trades(bot):
    """Render active trades table and controls"""
    if not st.session_state.active_trades:
        st.info("No active trades")
        return
    
    for idx, trade in enumerate(st.session_state.active_trades):
        with st.expander(f"Trade #{idx + 1}: {trade.token_pair[0]}/{trade.token_pair[1]}", expanded=True):
            cols = st.columns([2, 1, 1])
            
            # Trade details
            with cols[0]:
                st.write("**Route:**", f"{trade.source_chain} → {trade.target_chain}")
                st.write("**Status:**", "In Progress")
                progress = st.progress(0)
                
                # Simulate progress (this would be real progress in production)
                import time
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)
            
            # Profit calculation
            with cols[1]:
                st.metric(
                    "Expected Profit",
                    f"${trade.estimated_profit_usd:.2f}",
                    f"{trade.profit_percentage:.1f}%"
                )
            
            # Controls
            with cols[2]:
                if st.button("Cancel Trade", key=f"cancel_{idx}"):
                    cancel_trade(bot, idx)

def render_trade_history(bot):
    """Render historical trades table"""
    if not st.session_state.historical_trades:
        st.info("No historical trades")
        return
    
    # Convert historical trades to DataFrame
    history_data = []
    for trade in st.session_state.historical_trades:
        history_data.append({
            "Date": trade.get("timestamp", datetime.now()),
            "Pair": f"{trade['token_pair'][0]}/{trade['token_pair'][1]}",
            "Route": f"{trade['source_chain']} → {trade['target_chain']}",
            "Profit": f"${trade.get('actual_profit', 0):.2f}",
            "Status": trade.get("status", "Completed")
        })
    
    df = pd.DataFrame(history_data)
    st.dataframe(df, use_container_width=True)

def render_trade_settings(bot):
    """Render trade execution settings"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input(
            "Minimum Profit Threshold (%)",
            min_value=0.1,
            max_value=10.0,
            value=0.5,
            step=0.1,
            key="min_profit_threshold"
        )
        
        st.number_input(
            "Maximum Gas Price (Gwei)",
            min_value=1,
            max_value=500,
            value=100,
            step=1,
            key="max_gas_price"
        )
    
    with col2:
        st.number_input(
            "Maximum Trade Size (USD)",
            min_value=100,
            max_value=1000000,
            value=10000,
            step=100,
            key="max_trade_size"
        )
        
        st.number_input(
            "Slippage Tolerance (%)",
            min_value=0.1,
            max_value=5.0,
            value=0.5,
            step=0.1,
            key="slippage_tolerance"
        )
    
    st.checkbox("Enable Flash Loans", value=True, key="enable_flash_loans")
    st.checkbox("Auto-execute profitable trades", value=False, key="auto_execute")

def cancel_trade(bot, trade_idx):
    """Cancel an active trade"""
    try:
        trade = st.session_state.active_trades.pop(trade_idx)
        st.success(f"Trade cancelled successfully")
        
        # Add to history with cancelled status
        trade_dict = trade.__dict__
        trade_dict["status"] = "Cancelled"
        trade_dict["timestamp"] = datetime.now()
        st.session_state.historical_trades.append(trade_dict)
        
    except Exception as e:
        st.error(f"Error cancelling trade: {str(e)}")

def update_trade_progress(trade_idx: int, progress: float, status: str):
    """Update the progress of an active trade"""
    if 0 <= trade_idx < len(st.session_state.active_trades):
        st.session_state.active_trades[trade_idx].progress = progress
        st.session_state.active_trades[trade_idx].status = status 
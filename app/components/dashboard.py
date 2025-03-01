import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render_dashboard(bot):
    """Render the main dashboard"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Active Arbitrage Opportunities")
        render_opportunities_table(bot)
        
    with col2:
        st.subheader("📊 Performance Metrics")
        render_performance_metrics(bot)
    
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("📈 Profit History")
        render_profit_chart(bot)
        
    with col4:
        st.subheader("⛓️ Chain Activity")
        render_chain_activity(bot)

def render_opportunities_table(bot):
    """Render table of current arbitrage opportunities"""
    if not st.session_state.opportunities:
        st.info("No active arbitrage opportunities found")
        return

    # Convert opportunities to DataFrame
    opportunities_data = []
    for opp in st.session_state.opportunities:
        opportunities_data.append({
            "Source": f"{opp.source_chain} ({opp.source_dex})",
            "Target": f"{opp.target_chain} ({opp.target_dex})",
            "Pair": f"{opp.token_pair[0]}/{opp.token_pair[1]}",
            "Profit %": f"{opp.profit_percentage:.2f}%",
            "Est. Profit": f"${opp.estimated_profit_usd:.2f}",
            "Required Capital": f"${opp.required_capital:.2f}",
            "Action": "Execute"
        })
    
    df = pd.DataFrame(opportunities_data)
    
    # Add execute buttons
    for idx, row in df.iterrows():
        cols = st.columns([2, 2, 2, 1, 1, 1, 1])
        cols[0].write(row["Source"])
        cols[1].write(row["Target"])
        cols[2].write(row["Pair"])
        cols[3].write(row["Profit %"])
        cols[4].write(row["Est. Profit"])
        cols[5].write(row["Required Capital"])
        if cols[6].button("Execute", key=f"exec_{idx}"):
            execute_opportunity(bot, st.session_state.opportunities[idx])

def render_performance_metrics(bot):
    """Render key performance metrics"""
    metrics = calculate_performance_metrics(bot)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Profit", f"${metrics['total_profit']:.2f}")
    col2.metric("Success Rate", f"{metrics['success_rate']:.1f}%")
    
    col3, col4 = st.columns(2)
    col3.metric("Avg. Profit/Trade", f"${metrics['avg_profit_per_trade']:.2f}")
    col4.metric("Active Trades", metrics['active_trades'])

def render_profit_chart(bot):
    """Render profit history chart"""
    # Generate sample data for demonstration
    dates = pd.date_range(start='2024-01-01', end='2024-03-14', freq='D')
    profits = np.cumsum(np.random.normal(100, 30, size=len(dates)))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=profits,
        mode='lines',
        name='Cumulative Profit',
        line=dict(color='#00ff00', width=2)
    ))
    
    fig.update_layout(
        title="Cumulative Profit Over Time",
        xaxis_title="Date",
        yaxis_title="Profit (USD)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_chain_activity(bot):
    """Render chain activity metrics"""
    # Generate sample data for demonstration
    chains = ['Ethereum', 'BSC', 'Polygon', 'Avalanche']
    trades = [45, 32, 28, 15]
    
    fig = go.Figure(data=[
        go.Bar(
            x=chains,
            y=trades,
            marker_color=['#627EEA', '#F3BA2F', '#8247E5', '#E84142']
        )
    ])
    
    fig.update_layout(
        title="Trades by Chain",
        xaxis_title="Chain",
        yaxis_title="Number of Trades",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def calculate_performance_metrics(bot):
    """Calculate performance metrics"""
    # This would be implemented with actual trading data
    # Placeholder implementation
    return {
        "total_profit": 15420.50,
        "success_rate": 92.5,
        "avg_profit_per_trade": 154.20,
        "active_trades": len(st.session_state.active_trades)
    }

def execute_opportunity(bot, opportunity):
    """Execute an arbitrage opportunity"""
    with st.spinner("Executing trade..."):
        # This would execute the actual trade
        # For now, just add to active trades
        st.session_state.active_trades.append(opportunity)
        st.success("Trade executed successfully!") 
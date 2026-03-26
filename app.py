import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys

# Try importing anthropic with fallback
try:
    from anthropic import Anthropic
except ImportError:
    st.error("""
    ❌ **Anthropic library not installed**
    
    Streamlit Cloud is still installing dependencies. 
    Please wait 1-2 minutes and refresh the page.
    
    If this persists, try:
    1. Click "Settings" → "Secrets" in Streamlit
    2. Add your ANTHROPIC_API_KEY
    3. Go back and refresh
    """)
    st.stop()

# Initialize Streamlit page config
st.set_page_config(
    page_title="Inflation-Aware Budget Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get API key from secrets or user input
api_key = None
try:
    if "ANTHROPIC_API_KEY" in st.secrets:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = st.text_input(
        "Enter your Anthropic API Key",
        type="password",
        help="Get your API key from https://console.anthropic.com"
    )

if not api_key:
    st.warning("⚠️ Please enter your Anthropic API key to continue")
    st.stop()

# Initialize Anthropic client
try:
    client = Anthropic(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Anthropic client: {str(e)}")
    st.stop()

# Session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "budget_history" not in st.session_state:
    st.session_state.budget_history = []

# Title and description
st.title("💰 Inflation-Aware Budget Assistant")
st.markdown("""
This AI agent helps you adjust your spending budget based on real inflation trends.
Get personalized recommendations to maintain purchasing power in an inflationary environment.
""")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Settings")
    st.success("✅ API key configured" if api_key else "❌ No API key")
    
    st.divider()
    st.subheader("Budget Setup")
    
    monthly_budget = st.number_input(
        "Monthly Budget ($)",
        min_value=100.0,
        value=3000.0,
        step=100.0
    )
    
    inflation_rate = st.number_input(
        "Expected Annual Inflation Rate (%)",
        min_value=0.0,
        value=3.5,
        step=0.1,
        help="Current inflation rate to consider for budget adjustments"
    )
    
    st.divider()
    st.subheader("Budget Categories")
    
    categories = st.multiselect(
        "Select spending categories",
        options=[
            "Housing", "Food & Groceries", "Transportation",
            "Utilities", "Healthcare", "Insurance", "Entertainment",
            "Dining Out", "Shopping", "Subscriptions", "Education", "Other"
        ],
        default=["Housing", "Food & Groceries", "Transportation", "Utilities"]
    )


def get_inflation_data():
    """Fetch recent inflation data"""
    # This returns sample data - in production, use real API like Fred or World Bank
    base_date = datetime.now()
    months = []
    inflation_rates = []
    
    for i in range(12, -1, -1):
        date = base_date - timedelta(days=30*i)
        months.append(date.strftime("%B %Y"))
        # Simulated realistic inflation data
        inflation_rates.append(round(np.random.normal(3.5, 0.5), 2))
    
    return {"months": months, "rates": inflation_rates}


def calculate_adjusted_budget(original_budget, inflation_rate, months=1):
    """Calculate budget adjustment based on inflation"""
    monthly_rate = inflation_rate / 12 / 100
    adjusted = original_budget * ((1 + monthly_rate) ** months)
    return adjusted


def create_ai_agent_prompt(budget_data, inflation_data, categories):
    """Create a detailed prompt for the AI agent"""
    return f"""You are a financial AI agent specialized in helping people adjust their spending budgets based on inflation trends.

Current Budget Context:
- Monthly Budget: ${budget_data['monthly_budget']}
- Annual Inflation Rate: {budget_data['inflation_rate']}%
- Spending Categories: {', '.join(categories)}
- Current Date: {datetime.now().strftime('%B %d, %Y')}

Recent Inflation Trends:
{json.dumps(inflation_data, indent=2)}

Your responsibilities:
1. Analyze the impact of inflation on the user's budget
2. Provide specific category-by-category recommendations
3. Suggest budget adjustments to maintain purchasing power
4. Identify vulnerable spending areas most affected by inflation
5. Offer practical tips to optimize spending without reducing quality of life
6. Track historically what adjustments were made and their results

When responding:
- Be specific with dollar amounts and percentages
- Provide reasoning for each recommendation
- Consider the cumulative effect of inflation over time
- Suggest alternative strategies when possible
- Be encouraging and practical, not alarmist

Always maintain a conversational tone and ask clarifying questions when needed."""


def chat_with_agent(user_message, budget_data, inflation_data, categories):
    """Send message to Claude AI agent and get response"""
    system_prompt = create_ai_agent_prompt(budget_data, inflation_data, categories)
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Call Anthropic API using Claude 3.5 Sonnet
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=st.session_state.messages
        )
        
        assistant_message = response.content[0].text
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    except Exception as e:
        error_str = str(e)
        st.error(f"❌ Error: {error_str}")
        if "invalid_request_error" in error_str.lower() or "model" in error_str.lower():
            st.info("💡 The model may not be available. Try using 'claude-3-sonnet-20240229' instead.")
        return None


# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Budget Analysis
    st.header("📊 Your Budget Analysis")
    
    inflation_data = get_inflation_data()
    
    # Display inflation trends
    df_inflation = pd.DataFrame({
        "Month": inflation_data["months"],
        "Inflation Rate (%)": inflation_data["rates"]
    })
    
    st.subheader("Recent Inflation Trends")
    st.line_chart(df_inflation.set_index("Month"))
    
    # Calculate adjusted budget
    adjusted_budget = calculate_adjusted_budget(monthly_budget, inflation_rate, months=12)
    budget_increase = adjusted_budget - monthly_budget
    
    st.subheader("Annual Budget Adjustment")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Current Monthly Budget", f"${monthly_budget:.2f}")
    with col_b:
        st.metric("Inflation Rate", f"{inflation_rate}%")
    with col_c:
        st.metric(
            "Recommended Monthly Budget",
            f"${adjusted_budget:.2f}",
            delta=f"+${budget_increase:.2f}",
            delta_color="off"
        )

with col2:
    st.header("📈 Quick Stats")
    
    total_annual_increase = budget_increase * 12
    
    st.info(f"""
    **Annual Impact:**
    - Total increase needed: **${total_annual_increase:.2f}**
    - Monthly adjustment: **${budget_increase:.2f}**
    - Percentage increase: **{(budget_increase/monthly_budget)*100:.1f}%**
    """)
    
    st.success(f"""
    **Purchasing Power:**
    Without adjustment, you'd lose ~{inflation_rate}% of 
    purchasing power over the year.
    """)


# Category breakdown
st.divider()
st.subheader("💵 Budget by Category")

if categories:
    category_budgets = {}
    adjusted_category_budgets = {}
    
    cols = st.columns(len(categories))
    for idx, category in enumerate(categories):
        with cols[idx]:
            budget = st.number_input(
                f"{category}",
                min_value=0.0,
                value=monthly_budget / len(categories),
                step=50.0,
                key=f"cat_{idx}"
            )
            category_budgets[category] = budget
            adjusted_category_budgets[category] = calculate_adjusted_budget(
                budget, inflation_rate, months=1
            )
    
    # Display category adjustments
    df_categories = pd.DataFrame({
        "Category": list(category_budgets.keys()),
        "Current Budget": list(category_budgets.values()),
        "Adjusted Budget": list(adjusted_category_budgets.values()),
        "Adjustment": [adjusted_category_budgets[cat] - category_budgets[cat] 
                      for cat in category_budgets.keys()]
    })
    
    st.dataframe(df_categories, use_container_width=True)
else:
    st.info("Select budget categories in the sidebar to see breakdowns.")


# AI Chat Interface
st.divider()
st.header("🤖 AI Budget Advisor")
st.markdown("Chat with your AI budget assistant for personalized recommendations")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

# Chat input
user_input = st.chat_input("Ask about your budget, inflation impact, or get recommendations...")

if user_input:
    budget_data = {
        "monthly_budget": monthly_budget,
        "inflation_rate": inflation_rate,
        "categories": category_budgets if categories else {}
    }
    
    with st.spinner("🤔 Thinking..."):
        response = chat_with_agent(user_input, budget_data, inflation_data, categories)
    
    if response:
        st.rerun()


# Footer
st.divider()
st.markdown("""
---
**Disclaimer:** This tool provides general financial guidance based on inflation trends. 
Please consult with a financial advisor for personalized advice. 
Inflation rates and projections are estimates and may not reflect actual future conditions.
""")

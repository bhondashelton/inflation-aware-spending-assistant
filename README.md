# 💰 Inflation-Aware Spending Assistant

An AI-powered budget assistant that helps you adjust your spending based on real inflation trends. Built with Streamlit and Claude AI.

## Features

✨ **AI-Powered Budget Assistant**
- Real-time budget adjustments based on inflation rates
- Category-specific spending recommendations
- Conversational AI advisor for personalized guidance
- Historical tracking of budget adjustments

📊 **Comprehensive Budget Analysis**
- Visualize recent inflation trends
- Monitor purchasing power erosion
- Category-by-category budget breakdown
- Annual vs. monthly budget impact calculations

🎯 **Smart Recommendations**
- Identify vulnerable spending areas
- Suggest optimization strategies
- Maintain purchasing power in inflationary environments
- Track cumulative inflation effects

## Quick Start

### Prerequisites
- Python 3.8+
- Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/inflation-aware-spending-assistant.git
   cd inflation-aware-spending-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser and go to `http://localhost:8501`
   - Enter your Anthropic API key in the sidebar
   - Configure your budget and spending categories

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the root directory:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### Budget Settings

- **Monthly Budget**: Set your total monthly spending budget
- **Inflation Rate**: Enter the expected annual inflation rate
- **Categories**: Select and allocate budget across spending categories

## Deployment on Streamlit Cloud

### Step 1: Push to GitHub

1. Create a new GitHub repository
2. Add your files:
   ```bash
   git add .
   git commit -m "Initial commit: Inflation-aware budget assistant"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository and main branch
4. Set the main file path to `app.py`
5. Click "Deploy"

### Step 3: Add Secrets

1. In Streamlit Cloud dashboard, go to "Advanced settings"
2. Add your Anthropic API key as a secret:
   ```
   ANTHROPIC_API_KEY = your_api_key_here
   ```

Update `app.py` to use the secret:
```python
import streamlit as st
api_key = st.secrets.get("ANTHROPIC_API_KEY") or st.text_input("Enter your API key", type="password")
```

## How to Use

### Basic Workflow

1. **Set Up Your Budget**
   - Enter your monthly budget amount
   - Set the inflation rate
   - Select your spending categories
   - Allocate budget amounts per category

2. **View Analytics**
   - Check recent inflation trends
   - See recommended budget adjustments
   - Analyze impact by category

3. **Chat with AI Advisor**
   - Ask questions about your budget
   - Get personalized recommendations
   - Discuss inflation impact on specific categories
   - Explore optimization strategies

### Example Questions

- "How should I adjust my groceries budget?"
- "Which categories are most affected by inflation?"
- "What's the best way to maintain my lifestyle with rising prices?"
- "Can you recommend cost-saving strategies?"

## API Integration

### Anthropic Claude

This application uses Claude 3.5 Sonnet for intelligent budget recommendations:
- Conversational AI interface
- Context-aware suggestions
- Real-time budget analysis

### Future Integrations

- Federal Reserve inflation data (FRED API)
- World Bank inflation indicators
- Personal expense tracking APIs
- Bank account integrations

## Project Structure

```
inflation-aware-spending-assistant/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── .github/
    └── workflows/
        └── deploy.yaml   # GitHub Actions workflow
```

## Development

### Adding New Features

1. Create a new branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Test locally: `streamlit run app.py`
4. Commit and push: `git push origin feature/my-feature`
5. Create a Pull Request

### Local Testing

```bash
# Run the app
streamlit run app.py

# Test with different configs
streamlit run app.py -- --logger.level=debug
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### API Key Issues
- Ensure your Anthropic API key is valid
- Check you have sufficient credits
- Verify the key hasn't expired

### Streamlit Cloud Deployment
- Ensure all dependencies are in `requirements.txt`
- Check that `app.py` is in the root directory
- Verify secrets are properly configured

### Performance Issues
- Clear browser cache
- Restart the Streamlit app
- Check internet connection

## Disclaimer

This tool provides general financial guidance based on inflation trends and historical data. 
It is not professional financial advice. Please consult with a qualified financial advisor 
before making significant changes to your budget. Inflation rates and projections are estimates.

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: support@example.com
- 💬 Discussions: [GitHub Discussions](#)
- 🐛 Issues: [GitHub Issues](#)

## Roadmap

- [ ] User authentication and account persistence
- [ ] Historical budget tracking database
- [ ] Export budget reports to PDF/Excel
- [ ] Mobile app version
- [ ] Real-time FRED API integration
- [ ] Multi-currency support
- [ ] Budget sharing and collaboration features
- [ ] Expense receipt scanning
- [ ] Advanced forecasting models

---

Built with ❤️ using Streamlit and Anthropic Claude

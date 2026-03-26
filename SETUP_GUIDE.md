#!/usr/bin/env python3
"""
SETUP_GUIDE.md - Complete setup instructions for deployment
"""

# Inflation-Aware Spending Assistant - Setup Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [GitHub Repository Setup](#github-repository-setup)
3. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Step 1: Clone or Initialize Repository

**If cloning from GitHub:**
```bash
git clone https://github.com/YOUR-USERNAME/inflation-aware-spending-assistant.git
cd inflation-aware-spending-assistant
```

**If initializing new repository:**
```bash
cd inflation-aware-spending-assistant
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 2: Create Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_actual_api_key_here
```

Get your Anthropic API key from: https://console.anthropic.com/keys

### Step 5: Test Local Installation

```bash
# Verify all imports work
python -c "import streamlit, anthropic, pandas, numpy, requests; print('✅ All imports successful')"

# Run the app
streamlit run app.py
```

The app should open at: http://localhost:8501

## GitHub Repository Setup

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `inflation-aware-spending-assistant`
3. Description: `AI-powered budget assistant that adjusts spending based on inflation trends`
4. Choose: Public (for Streamlit Cloud deployment)
5. Check "Add a README file" ✅ (we'll replace it)
6. Add .gitignore: Python
7. Add license: MIT
8. Click "Create repository"

### Step 2: Add Files to Repository

```bash
# Navigate to project directory
cd inflation-aware-spending-assistant

# Initialize git (if not already done)
git init

# Add remote origin
git remote add origin https://github.com/YOUR-USERNAME/inflation-aware-spending-assistant.git

# Fetch main branch
git fetch origin main
git checkout main

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Inflation-aware budget assistant with Streamlit and Claude AI"

# Push to GitHub
git push -u origin main
```

### Step 3: Configure Repository Settings

**On GitHub:**

1. Go to Settings → General
   - Description: "AI-powered budget assistant that adjusts spending based on inflation trends"
   - Website: [your-app-url] (after deployment)

2. Go to Settings → Collaborators and teams
   - Add collaborators as needed

3. Go to Settings → Branches
   - Set default branch to `main`
   - Enable branch protection rules:
     - Require pull request reviews before merging
     - Require status checks to pass

## Streamlit Cloud Deployment

### Step 1: Connect GitHub to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Click "Sign in with GitHub" (if not already)
4. Authorize Streamlit
5. Grant repository access to your GitHub account

### Step 2: Deploy Application

1. On Streamlit Cloud dashboard, click "New app"
2. Provide the following:
   - **Repository**: YOUR-USERNAME/inflation-aware-spending-assistant
   - **Branch**: main
   - **Main file path**: app.py
3. Click "Deploy"

App will be available at: https://inflation-aware-spending-assistant.streamlit.app

### Step 3: Add Secrets

1. After app deploys, go to Settings (gear icon) → "Secrets"
2. Add your Anthropic API key:
   ```toml
   ANTHROPIC_API_KEY = "your_actual_api_key_here"
   ```
3. Click "Save"

**Alternative (Manual update in app.py):**
Replace this line in app.py:
```python
api_key = st.text_input("Enter your Anthropic API Key", type="password")
```

With:
```python
api_key = st.secrets.get("ANTHROPIC_API_KEY") or st.text_input("Enter your API Key", type="password")
```

### Step 4: Enable Auto-deployment

Settings → Deploy → Auto-deploy on push to main branch ✅

Now every push to `main` will automatically redeploy your app!

## Environment Configuration

### Local Development (.env)

```bash
ANTHROPIC_API_KEY=sk-ant-...
# DEBUG=true
# LOG_LEVEL=debug
```

### Streamlit Cloud (Secrets)

Settings → Secrets:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

### Streamlit Configuration (.streamlit/config.toml)

Already configured with:
- Theme colors (green theme)
- Server settings
- Browser analytics disabled
- Client error details enabled

## Authentication & Security

### Best Practices

1. **Never commit API keys** to repository
2. Use `.env.example` as template only
3. Add API keys only to:
   - Local `.env` file (in .gitignore)
   - Streamlit Cloud Secrets (encrypted)

4. **Rotate API keys** if compromised
5. Use environment-specific configurations

### Getting API Keys

**Anthropic:**
1. Go to https://console.anthropic.com
2. Navigate to API keys
3. Click "Create new API key"
4. Copy and paste into Streamlit Cloud Secrets

## Testing & Validation

### Run Tests Locally

```bash
# Run unit tests
python -m pytest test_budget_utils.py -v

# Or use unittest directly
python -m unittest test_budget_utils.py
```

### Manual Testing Checklist

- [ ] Start Streamlit app (`streamlit run app.py`)
- [ ] Enter API key in sidebar
- [ ] Set budget and inflation rate
- [ ] Select spending categories
- [ ] Chat with AI agent
- [ ] View budget analytics

### CI/CD Pipeline

GitHub Actions automatically runs on push:
- Syntax checking (pylint)
- Requirements validation
- Import verification

View results: Settings → Actions

## Continuous Development

### Adding Features

1. Create feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Make changes and test locally:
   ```bash
   streamlit run app.py
   ```

3. Commit changes:
   ```bash
   git add .
   git commit -m "Add: Description of feature"
   git push origin feature/new-feature
   ```

4. Create Pull Request on GitHub
5. After merge to main → Auto-deploy to Streamlit Cloud

### Updating Dependencies

```bash
# Update requirements
pip list --outdated

# Update specific package
pip install --upgrade streamlit

# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update: Python dependencies"
git push
```

## Troubleshooting

### Deployment Issues

**App won't deploy on Streamlit Cloud:**
- Check Settings → Logs
- Ensure `requirements.txt` exists and has all dependencies
- Verify `app.py` is in root directory
- Check Python version compatibility (3.8+)

**ModuleNotFoundError after deployment:**
- Add missing package to `requirements.txt`
- Push changes to main branch
- Streamlit will auto-redeploy

### Runtime Issues

**"Please enter your Anthropic API key":**
- On Streamlit Cloud: Add to Secrets
- Locally: Add to `.env` file
- Or paste API key in sidebar form

**"Error communicating with AI agent":**
- Verify API key is valid
- Check API key has sufficient credits
- Ensure internet connection is working
- Check Anthropic service status: https://status.anthropic.com

**App runs slow:**
- First run after deployment is slower (cold start)
- Clear browser cache
- Restart Streamlit app (Ctrl+C, then `streamlit run app.py`)

### Git Issues

**"Remote rejection" when pushing:**
```bash
# Pull latest changes first
git pull origin main

# Resolve any conflicts, then:
git push origin main
```

**"Permission denied" error:**
- Generate SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Add SSH key to GitHub account
- Or use Personal Access Token with HTTPS

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Anthropic API**: https://docs.anthropic.com
- **GitHub Help**: https://docs.github.com
- **Streamlit Community**: https://discuss.streamlit.io
- **Anthropic Community**: https://www.anthropic.com/community

## Next Steps

1. ✅ Complete local setup
2. ✅ Push to GitHub
3. ✅ Deploy to Streamlit Cloud
4. ✅ Add API keys to secrets
5. ✅ Test the application
6. 📝 Share with others and get feedback
7. 🚀 Plan additional features

---

Happy budgeting! Questions? Open an issue on GitHub.

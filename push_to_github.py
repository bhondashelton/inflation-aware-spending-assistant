#!/usr/bin/env python3
"""
Simple script to push changes to GitHub using GitHub API
Run this to automatically update your repository
"""

import os
import base64
import requests
import json

# Configuration
GITHUB_USERNAME = "bhondashelton"
REPO_NAME = "inflation-aware-spending-assistant"
GITHUB_TOKEN = None  # Will be set by user

# Files to upload
FILES_TO_UPDATE = [
    "app.py",
    "requirements.txt"
]

def get_github_token():
    """Get GitHub token from user"""
    print("\n🔐 GitHub Authentication Required")
    print("-" * 50)
    print("You need a GitHub Personal Access Token to push changes.")
    print("Create one here: https://github.com/settings/tokens")
    print("\nSteps:")
    print("1. Go to Settings → Developer settings → Personal access tokens")
    print("2. Click 'Generate new token'")
    print("3. Select 'repo' scope")
    print("4. Copy the token and paste below")
    print("-" * 50)
    
    token = input("\nEnter your GitHub Personal Access Token: ").strip()
    return token

def read_local_file(filepath):
    """Read local file content"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None

def get_file_sha(token, filename):
    """Get the SHA of an existing file"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filename}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["sha"]
    except Exception as e:
        print(f"Error getting SHA for {filename}: {e}")
    
    return None

def update_file_on_github(token, filename, content, message):
    """Update or create a file on GitHub"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filename}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get existing file SHA if it exists
    sha = get_file_sha(token, filename)
    
    # Encode content to base64
    encoded_content = base64.b64encode(content.encode()).decode()
    
    # Prepare data
    data = {
        "message": message,
        "content": encoded_content,
        "branch": "main"
    }
    
    if sha:
        data["sha"] = sha
    
    try:
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            print(f"✅ Successfully updated: {filename}")
            return True
        else:
            print(f"❌ Failed to update {filename}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating {filename}: {e}")
        return False

def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🚀 Inflation-Aware Budget Assistant")
    print("   GitHub Repository Updater")
    print("=" * 50)
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("\n❌ No token provided. Exiting.")
        return
    
    # Test authentication
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print("\n🔍 Testing GitHub authentication...")
    try:
        response = requests.get("https://api.github.com/user", headers=headers)
        if response.status_code == 200:
            user = response.json()["login"]
            print(f"✅ Authenticated as: {user}")
        else:
            print("❌ Authentication failed. Invalid token.")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Update files
    print(f"\n📁 Updating repository: {GITHUB_USERNAME}/{REPO_NAME}")
    print("-" * 50)
    
    local_dir = os.path.dirname(os.path.abspath(__file__))
    success_count = 0
    
    for filename in FILES_TO_UPDATE:
        filepath = os.path.join(local_dir, filename)
        content = read_local_file(filepath)
        
        if content:
            message = f"Update: {filename} - Fix deployment issues"
            if update_file_on_github(token, filename, content, message):
                success_count += 1
    
    # Summary
    print("-" * 50)
    print(f"\n📊 Summary: {success_count}/{len(FILES_TO_UPDATE)} files updated")
    
    if success_count == len(FILES_TO_UPDATE):
        print("\n✅ All files updated successfully!")
        print("🔄 Streamlit Cloud will redeploy in 2-3 minutes...")
        print(f"🌐 Check your app at:")
        print(f"   https://{REPO_NAME}.streamlit.app")
    else:
        print("\n⚠️  Some files failed to update. Please check the errors above.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()

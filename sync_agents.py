import requests
import json
import os
import sys
from git import Repo

# --- CONFIG ---
# Ensure you add 'BASE44_API_KEY' to your GitHub Repo Secrets
API_KEY = os.environ.get('BASE44_API_KEY')
APP_ID = '69a9ebdbd8823974680ee648' 
AGENT_LIST = [
    "lucky", "ghost", "oracle", "nexus", "cipher", "wraith", 
    "sage", "titan", "vex", "echo", "axiom", "sovereign_core"
]

def sync():
    url = f'https://api.base44.com/api/apps/{APP_ID}/entities/AIAgent'
    headers = {'api_key': API_KEY, 'Content-Type': 'application/json'}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching agents: {response.text}")
        return

    agents = response.json()
    repo = Repo('.') # Runs in the root of the GitHub repo

    for agent in agents:
        name = agent.get('name', '').lower()
        if name in AGENT_LIST:
            # Save directly to the main folder
            filename = f"{name}_framework.json"
            with open(filename, 'w') as f:
                json.dump(agent, f, indent=4)
            print(f"Updated: {filename}")

    # Push changes back to GitHub
    repo.git.add(A=True)
    if repo.is_dirty():
        repo.index.commit("Sovereign-Core: 15-min lethal framework sync")
        repo.remote(name='origin').push()
        print("Push complete.")
    else:
        print("No framework changes detected.")

if __name__ == "__main__":
    sync()

# 🎨 Kommander

Kommander is a Discord bot designed to streamline Kubernetes operations via custom commands. It enables users to manage Kubernetes clusters, handle resources, and execute DevOps tasks directly from Discord.

## 🔍 Features

- Execute `kubectl` commands from Discord.
- Manage Flux for reconciliation, resumption, and suspension.
- Describe and delete Kubernetes resources like pods and Helm releases.
- Display logs from specific pods.
- Handle rollout operations for deployments and statefulsets.
- Automatically assign roles to new guild members.

## Getting Started

### 📋 Prerequisites

- Python 3.7+
- Discord bot token
- Access to a Kubernetes cluster with `kubectl`
- Flux CLI installed
- Discord Bot added to a Discord Server

### ⚙️ How to Run the Bot - Local

1. **Set up environment variables:**
    ```bash
    export TIMEOUT="60"  # Timeout setting
    export CHANNEL_NAME="your_channel_name"  # Discord channel name
    export DISCORD_TOKEN="your_discord_bot_token"  # Discord bot token
    export GUILD_ID="your_guild_id"  # Discord guild ID
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Connect to your Kubernetes cluster:**
    ```bash
    aws sso login --profile hmg-dev  # Example command to authenticate with AWS SSO
    ```

4. **Run the bot:**
    ```bash
    /usr/local/bin/python3.11 /your-directory/devops-apps/kommander/app/main.py /your-directory/devops-apps/kommander/configs.yaml
    ```

## 📁 Folders Structure

```plaintext
─ app/
  │
  ├─ main.py            # Main application entry point
  │
  ├─ aux/               # Auxiliary functions
  │   │
  │   ├─ aux_func.py    # Auxiliary function definitions
  │   │
  │   └─ button.py      # Button-related functions
  │ 
  ├─ bot/               # Bot functionality
  │   │
  │   ├─ bot.py         # Bot main logic
  │   └─ config.py      # Bot configuration
  │       
  └─ command/           # Command handlers
      │
      ├─ flux.py        # Flux command handler
      │
      ├─ geral_command.py   # General command handler
      │
      ├─ kube_del.py    # Kubernetes delete command handler
      │
      ├─ kube_desc.py   # Kubernetes describe command handler
      │
      └─ kube_get.py    # Kubernetes get command handler
```
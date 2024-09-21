Sure! Here's a **simplified `README.md`** that covers only the steps for configuring the Gmail API, generating OAuth credentials, and placing the `credentials.json` file in the `/config` folder:

### Simplified `README.md` for Google API Setup:

```markdown
# Gmail API Setup Guide

This guide will walk you through configuring your Google Cloud project to access the Gmail API with **read-only** and **metadata** permissions. You will generate OAuth 2.0 credentials, download them as `credentials.json`, and store them in the `/config` folder of this project.

## Step 1: Enable the Gmail API and Create OAuth Credentials

1. **Go to the Google Cloud Console**:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).

2. **Create a New Project**:
   - In the top-left corner, click **Select a Project** > **New Project**.
   - Name your project (e.g., `gmail-ai-search`).
   - Click **Create**.

3. **Enable the Gmail API**:
   - In the Google Cloud Console, go to **APIs & Services** > **Library**.
   - Search for **Gmail API** and click **Enable**.

4. **Create OAuth 2.0 Credentials**:
   - Navigate to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** > **OAuth 2.0 Client IDs**.
   - Select **Desktop App** as the application type.
   - Give your credentials a name (e.g., `Gmail API Desktop Client`), and click **Create**.
   - After creation, click **Download** to download the `client_secret_XXX.json` file.

5. **Rename and Move the Credentials File**:
   - Rename the downloaded file to `credentials.json`.
   - Move the `credentials.json` file to the `/config` folder of this project.

## Step 2: Gmail API Scopes

This project uses the following Gmail API scopes:

- **Gmail Read-Only Scope**: Allows the app to read emails but not modify them.
  ```plaintext
  https://www.googleapis.com/auth/gmail.readonly
  ```

- **Gmail Metadata Scope**: Allows the app to access email metadata (such as subject, sender, and recipients) without the full message content.
  ```plaintext
  https://www.googleapis.com/auth/gmail.metadata
  ```

Once you've completed these steps, your project will be ready to use the Gmail API.
```

### Summary of Changes:
- This version focuses purely on the steps you take in the **Google Cloud Console** to enable the Gmail API, create OAuth credentials, and set the required Gmail API scopes.
- It omits any information about Python, running the app, or folder structure, as requested.

Let me know if you need any further adjustments!
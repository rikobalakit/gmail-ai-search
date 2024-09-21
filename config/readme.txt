Add "Credentials.json" in this folder. You can get this from the Google Cloud APIs & Services page.

Instructions (via ChatGPT)

The **`credentials.json`** file is essentially the **OAuth 2.0 client secrets file**, which is generated when you create your **OAuth 2.0 credentials** in the Google Cloud Console. It contains the **client ID** and **client secret** that your app needs to authenticate with the Gmail API.

Here's the step-by-step context to make sure you're getting the right file:

### How to Get `credentials.json` (OAuth 2.0 Client Secrets File):

1. **In the Google Cloud Console**:
   - Go to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** and select **OAuth 2.0 Client IDs**.
   - For **Application Type**, select **Desktop App** (since this is a local script).
   - Once the credentials are created, click **Download** to download the **client secret file**, which is the `credentials.json` file.

2. **Save the File**:
   - When you download the file, it will be named something like `client_secret_XXX.json`.
   - **Rename it to** `credentials.json` and place it in your project directory where your Python script is located (`gmail_fetch.py`).

### What’s Inside `credentials.json`:
The **`credentials.json`** file contains the following information:
```json
{
  "installed": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your-client-secret",
    "redirect_uris": [
      "http://localhost"
    ]
  }
}
```
- **`client_id`** and **`client_secret`** are the values your app uses to authenticate with Google’s servers.
- **`redirect_uris`** define where the user will be redirected after authentication (for a desktop app, it's usually `http://localhost`).

---

### Summary:
- **`credentials.json`** is indeed the **OAuth 2.0 client secret** file you downloaded when creating your OAuth credentials.
- Rename the downloaded file to `credentials.json` and place it in your project directory.
- This file is crucial for the OAuth flow, allowing your Python app to authenticate with the Gmail API.

Once the **`credentials.json`** is in place, running the script will prompt you to authenticate your Gmail account, and the tokens will be saved in the `token.json` file for future runs.

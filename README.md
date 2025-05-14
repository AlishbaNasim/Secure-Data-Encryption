# Secure Data Encryption System

🔐 A simple, user-friendly web application that allows users to encrypt and decrypt their data securely using a passkey. Built with Streamlit, this application ensures data security through password hashing, encryption, and a local storage system (no external database).

## Features

### User Registration & Authentication:
- Users can register with a unique username and password.
- Passwords are securely hashed and stored.
- Login with the registered credentials and get access to store or retrieve data.

### Data Encryption & Decryption:
- Users can store and encrypt their data using a custom passkey.
- Decrypt the stored data by providing the correct passkey.

### Secure Storage:
- All data is stored locally in a JSON file (no external database).
- Encrypted data is stored per user, and only the correct passkey can decrypt it.

### Lockout Mechanism:
- After 3 failed login attempts, the user will be locked out for a defined period (e.g., 60 seconds) to prevent brute-force attacks.

## Requirements
To run this application locally, you will need the following libraries:

- **Streamlit**: For building the web app interface.
- **Cryptography**: For encryption and decryption operations.
- **Hashlib**: For hashing passwords.
- **JSON**: For saving and loading user data.
- **OS**: For interacting with the file system.

You can install the required dependencies with the following command:

```bash
pip install -r requirements.txt
```
## Usage

### 1. Start the Application
Run the following command to start the Streamlit app:

```bash
streamlit run app.py
```
### 2. Register a New User

- Navigate to the Register page.
- Enter your desired username and password.
- If successful, the user will be registered and ready to login.

### 3. Login

- Navigate to the Login page.
- Enter your registered username and password.
- After logging in, you can store and retrieve encrypted data.

### 4. Store Data

- Navigate to the Store Data page.
- Enter the data you want to encrypt and a custom passkey.
- The data will be encrypted and stored.

### 5. Retrieve Data

- Navigate to the Retrieve Data page.
- Enter the correct passkey to decrypt and view your data.

### Lockout Mechanism:

After 3 failed login attempts, the user will be locked out for a predefined time (60 seconds). This mechanism prevents brute-force login attempts.

### How to Contribute

- Fork the repository.
- Clone your fork locally.
- Make your changes in a new branch.
- Test your changes.
- Create a pull request with a description of your changes.

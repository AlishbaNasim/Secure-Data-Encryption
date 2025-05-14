import streamlit as st
import hashlib #used for password hashing.
import json # Used for reading and writing JSON data
import os # Provides a way to interact with the file system 
import time #Used to manage the lockout duration
from cryptography.fernet import Fernet #A cryptography library for encrypting and decrypting data.
from base64 import urlsafe_b64encode # CONVERT BINARY CODE INTO URL
from hashlib import pbkdf2_hmac # HASHING ALGORITM USE FOR PASSWORD SECURE

# === Constants ===
DATA_FILE = "secure_data.json"  # Path to the file where user data will be saved
SALT = b"secure_salt_value"  # A constant value used to make password hashing more secure
LOCKOUT_DURATION = 60  # Lockout duration (in seconds) after multiple failed login attempts


# === Session State Initialization ===
# YE TRACK KRE KA VARIABLE KO ACROSS WITH 3 STEPS
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None  # Tracks the authenticated user

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0  # Tracks the number of failed login attempts

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0  # Tracks the time of lockout


# === Data Load/Save Functions ===
def load_data():
    if os.path.exists(DATA_FILE):  # Checks if the data file exists
        with open(DATA_FILE, "r") as f:
            return json.load(f)  # Reads and returns the data in the file
    return {}  # If the file doesn't exist, returns an empty dictionary

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)  # Saves the data to the file


# === Crypto Utilities ===
def generate_key(passkey):  # Generates a key from the user's passkey
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)  # Applies hashing to passkey
    return urlsafe_b64encode(key)  # Encodes the key into a safe URL format

def hash_password(password):  # Hashes the user's password for secure storage
    return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000).hex()  # Returns hashed password in hexadecimal format

def encrypt_text(text, key):  # Encrypts the provided text using the passkey
    cipher = Fernet(generate_key(key))  # Creates an encryption object with the generated key
    return cipher.encrypt(text.encode()).decode()  # Encrypts the text and returns it as a decoded string

def decrypt_text(encrypted_text, key):  # Decrypts the provided encrypted text
    try:
        cipher = Fernet(generate_key(key))  # Creates a decryption object with the generated key
        return cipher.decrypt(encrypted_text.encode()).decode()  # Decrypts and returns the decoded text
    except Exception:  # In case of an error (e.g., incorrect passkey), it returns None
        return None

stored_data = load_data()  # Loads the stored data from the file into memory


# === Navigation Bar ===
st.title("🔐 Secure Data Encryption System")  # Sets the title of the Streamlit app
menu = ["🏠 Home", "📝 Register", "🔐 Login", "💾 Store Data", "📂 Retrieve Data"]  # Defines the navigation menu options
choice = st.sidebar.selectbox("🔎 Navigation", menu)  # Displays the menu and stores the user's choice


# === Home Page ===
if choice == "🏠 Home":
    st.subheader("Welcome to the Secure Data Encryption System! 🛡️")  # Displays the subheading
    st.markdown("""  ### Description of the app's functionality
    - 🔑 Users can **store** data using a unique **passkey**
    - 🔓 Users can **decrypt** the data using the correct passkey
    - 🔁 Multiple failed attempts result in **forced re-login**
    - ⚙️ All data is stored **locally** in memory (no external DB)
    """)


# === Register Page ===
elif choice == "📝 Register":
    st.subheader("Register New User 🧾")  # Displays the Register section
    username = st.text_input("Choose Username")  # User inputs a username
    password = st.text_input("Choose Password", type="password")  # User inputs a password

    if st.button("Register 🟢"):  # When the Register button is pressed
        if username in stored_data:
            st.warning("⚠️ User already exists.")  # If username already exists, show warning
        elif not username or not password:
            st.error("❗ Both fields are required.")  # Show error if any field is empty
        else:
            stored_data[username] = {
                "password": hash_password(password),  # Hash the password before saving
                "data": []  # Initialize an empty list for user data
            }
            save_data(stored_data)  # Save the new data
            st.success("✅ User registered successfully!")  # Show success message


# === Login Page ===
elif choice == "🔐 Login":
    st.subheader("User Login 🔐")  # Displays the Login section

    if time.time() < st.session_state.lockout_time:  # If the user is locked out
        remaining = int(st.session_state.lockout_time - time.time())  # Calculates remaining lockout time
        st.error(f"⏳ Too many failed attempts. Please wait {remaining} seconds.")  # Shows the remaining wait time
    else:
        username = st.text_input("Username")  # User inputs a username
        password = st.text_input("Password", type="password")  # User inputs a password

        if st.button("Login 🔑"):  # When the Login button is pressed
            if username in stored_data and stored_data[username]["password"] == hash_password(password):  # Check if credentials match
                st.session_state.authenticated_user = username  # Set the user as authenticated
                st.session_state.failed_attempts = 0  # Reset failed attempts
                st.success(f"👋 Welcome, {username}!")  # Display success message
            else:
                st.session_state.failed_attempts += 1  # Increment failed attempts
                st.error("❌ Invalid credentials.")  # Display error message
                if st.session_state.failed_attempts >= 3:  # Lock user after 3 failed attempts
                    st.session_state.lockout_time = time.time() + LOCKOUT_DURATION  # Set lockout time
                    st.session_state.failed_attempts = 0  # Reset failed attempts


# === Store Data Page ===
elif choice == "💾 Store Data":
    if not st.session_state.authenticated_user:  # If no user is logged in
        st.warning("⚠️ Please login first.")  # Show warning
    else:
        st.subheader("Store Encrypted Data 🔐")  # Display Store Data section
        data = st.text_area("Enter your data here 📝")  # User inputs data to encrypt
        passkey = st.text_input("Passkey (for encryption) 🔑", type="password")  # User inputs passkey for encryption

        if st.button("Encrypt and Save 💾"):  # When the Encrypt and Save button is pressed
            if data and passkey:  # If both fields are filled
                encrypted = encrypt_text(data, passkey)  # Encrypt the data
                stored_data[st.session_state.authenticated_user]["data"].append(encrypted)  # Store the encrypted data
                save_data(stored_data)  # Save the updated data to the file
                st.success("✅ Data encrypted and saved!")  # Success message
            else:
                st.error("❗ All fields are required.")  # Error if any field is empty


# === Retrieve Data Page ===
elif choice == "📂 Retrieve Data":
    if not st.session_state.authenticated_user:  # If no user is logged in
        st.warning("⚠️ Please login first.")  # Show warning
    else:
        st.subheader("Retrieve Your Data 🔍")  # Display Retrieve Data section
        user_data = stored_data[st.session_state.authenticated_user]["data"]  # Get the user's stored data
        if not user_data:  # If no data is stored
            st.info("📭 No data stored.")  # Show info message
        else:
            passkey = st.text_input("Enter your passkey to decrypt 🔑", type="password")  # User inputs passkey to decrypt data
            if st.button("Decrypt Data"):  # When the Decrypt button is pressed
                if passkey:  # If passkey is entered
                    for i, item in enumerate(user_data, 1):  # Loop through the user's data
                        decrypted = decrypt_text(item, passkey)  # Try to decrypt the data
                        if decrypted:
                            st.success(f"📄 Data {i}: {decrypted}")  # Show decrypted data
                        else:
                            st.error(f"🔒 Data {i}: Incorrect passkey or corrupted data.")  # Show error if decryption fails
                else:
                    st.error("❗ Passkey is required.")  # Error if no passkey is provided

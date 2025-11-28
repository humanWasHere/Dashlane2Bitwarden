# File to transfert Dashlane credentials to Bitwarden
import pandas as pd
from pathlib import Path

# Extract
ask_valid_input = True
while ask_valid_input:
    user_dashlane_file_path = Path(input("Enter the path to the Dashlane credential CSV file: "))
    if not user_dashlane_file_path.is_file():
        print("Error: File does not exist. Please provide a valid file path.")
        continue
    try:
        dashlane_credential_df = pd.read_csv(user_dashlane_file_path, encoding='utf-8')
        ask_valid_input = False
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        print("Please ensure the file is a valid CSV file.")

# Transform
dashlane_credential_df = dashlane_credential_df.replace(["null", "", "NaN", "NA"], None)

# Validate that essential columns exist
missing_columns = [col for col in ["title", "password"] if col not in dashlane_credential_df.columns]
if missing_columns:
    raise ValueError(f"Error: Required Dashlane columns are missing: {', '.join(missing_columns)}")

# Validate that essential columns have no empty values
for col in ["title", "password"]:
    if dashlane_credential_df[col].isna().any():
        empty_count = dashlane_credential_df[col].isna().sum()
        raise ValueError(f"Error: Column '{col}' has {empty_count} empty row(s). All entries must have a {col}.")

# Load
# DASHLANE COLUMNS : user_name, user_name_2, user_name_3, title, password, note, url, category, otp
# BITWARDEN COLUMNS : folder, favorite, type, name, notes, fields, reprompt, login_uri, login_username, login_password, login_totp

username_cols = ["user_name", "user_name_2", "user_name_3"]
existing_username_cols = [col for col in username_cols if col in dashlane_credential_df.columns]
dashlane_credential_df["merged_login_username"] = dashlane_credential_df[existing_username_cols].apply(
    lambda row: " / ".join(row.dropna().astype(str)), axis=1
)

mapper_dashlane_to_bitwarden = {
    "category": "folder",  # VALID
    # "XXX": "favorite",
    "title": "name",  # VALID
    "note": "notes",  # VALID
    # "XXX": "fields",
    # "XXX": "reprompt",
    "url": "login_uri",  # VALID
    "merged_login_username": "login_username",
    "password": "login_password",  # VALID
    "otp": "login_totp",  # VALID
}

# Create the Bitwarden DataFrame by renaming columns and enforcing the schema
bitwarden_columns = [
    "folder", "favorite", "type", "name", "notes", "fields", 
    "reprompt", "login_uri", "login_username", "login_password", "login_totp"
]

bitwarden_credential_df = dashlane_credential_df.rename(columns=mapper_dashlane_to_bitwarden).reindex(columns=bitwarden_columns)
bitwarden_credential_df["type"] = "login"

if Path("credentials_exported_to_bitwarden.csv").is_file():
    overwrite = input("Existing export file found. Overwrite (y/n)? ")
    if overwrite.lower() != 'y':
        print("Export cancelled.")
        exit()
bitwarden_credential_df.to_csv("credentials_exported_to_bitwarden.csv", index=False, sep=',', encoding='utf-8')
export_file_path = Path("credentials_exported_to_bitwarden.csv").resolve()
if export_file_path.is_file():
    print(f"Bitwarden export file created at: {export_file_path}")
    print(f"Total credentials exported: {len(bitwarden_credential_df)}")
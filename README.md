# IMAP Password Checker

A small Python utility to **verify IMAP passwords safely**.  
It helps confirm whether your stored passwords are still valid on the mail server without saving them to disk.  

This is useful if you:
- Use multiple mail clients (Apple Mail, Thunderbird, etc.).
- Store your passwords in a manager (e.g., 1Password).
- Want to quickly confirm a password is correct after changing it.

---

## Features

- Supports **SSL (993)**, **STARTTLS (143)**, and **plain (143)** IMAP.
- Interactive, secure password prompt (no echo).
- Works on **single accounts** or a **CSV list of accounts**.
- Clear success/failure messages (wrong password vs. network/TLS issues).
- Exit codes:
  - `0` = all checks succeeded
  - `2` = one or more checks failed

---

## Requirements

- Python 3.7+  
- Standard library only (no extra pip installs needed)

---

## Usage

### 1. Clone or copy

```bash
git clone https://github.com/rcaservices/check_imap_passwords.git
cd check_imap_passwords

### 2. Run on a single account

./check_imap_passwords.py \
  --server imap.gmail.com \
  --username user@example.net \
  --security ssl \
  --port 993

### 3. Run on multiple accounts

#### prepare an accounts.csv file:

cp accounts.csv.example accounts.csv

####  Edit the accounts.csv file

server,username,port,security,label
imap.gmail.com,user@example.com,993,ssl,Personal Gmail
mail.examplehosting.com,me@mydomain.com,993,ssl,My Domain Mailbox
outlook.office365.com,user@company.com,993,ssl,Work O365

#### then run:

./check_imap_passwords.py --csv accounts.csv

####  you’ll be prompted for each account’s password in turn.

### Security Notes

Passwords are never stored to disk.

The script only attempts login and reports success/failure.

For Gmail, iCloud, Yahoo, and some others, you may need an App Password if 2FA is enabled.

For Office365/Outlook, basic auth may be disabled by your org; if so, this script will show failed authentication even with the right password.


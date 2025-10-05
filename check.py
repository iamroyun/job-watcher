import requests, hashlib, os, smtplib
from email.message import EmailMessage

# --- List of pages to monitor ---
URLS = {
    "altsound": "https://altsound.io",
}

HASH_DIR = "hashes"
os.makedirs(HASH_DIR, exist_ok=True)

# --- Email Setup ---
EMAIL_FROM = "janreddd@gmail.com"
EMAIL_TO = "iamroyun@gmail.com"
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(title, url):
    msg = EmailMessage()
    msg.set_content(f"The page '{title}' has changed:\n{url}")
    msg["Subject"] = f"🔔 Job Page Updated — {title}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASS)
        smtp.send_message(msg)

# --- Check each page ---
for title, url in URLS.items():
    print(f"Checking {title}...")
    r = requests.get(url)
    r.raise_for_status()
    new_hash = hashlib.sha256(r.text.encode("utf-8")).hexdigest()

    hash_file = os.path.join(HASH_DIR, f"{title.replace(' ', '_')}.txt")

    if os.path.exists(hash_file):
        with open(hash_file) as f:
            old_hash = f.read()
    else:
        old_hash = ""

    if new_hash != old_hash:
        print(f"⚡ Change detected on {title}!")
        send_email(title, url)
        with open(hash_file, "w") as f:
            f.write(new_hash)
    else:
        print(f"No change detected for {title}.")

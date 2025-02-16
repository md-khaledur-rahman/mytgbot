from telethon import TelegramClient, events
import re
import schedule
import time as t
import os
import sys
import asyncio
import subprocess
import shlex
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from datetime import datetime,timezone, time

# Replace these with your own values
API_ID = '20703704'  # Get from https://my.telegram.org
API_HASH = 'ea0ed8aa881ecc8c573a5a0fd989ec89'  # Get from https://my.telegram.org
PHONE_NUMBER = '+8801960486882'  # Your Telegram account's phone number
TELEGRAM_BOT_TOKEN = "7856272302:AAHtYfagxfNHQQfMJ0SCphxd5SmeoYlCAco"

# Channel usernames
SOURCE_CHANNEL = '@AutoUdemy'  # Channel to monitor
TARGET_CHANNEL = '@free_course_udemy_online'  # Your channel to forward messages to
MSOFFICE_TARGET_CHANNEL = '@msofficecourses'  # Additional channel to forward messages to
PYTHON_TARGET_CHANNEL = '@pythonlearnerss'  # Additional channel to forward messages to
WEB_TARGET_CHANNEL = '@webdesignlrn'  # Additional channel to forward messages to
SPECIAL_CHANNEL = '@online_premium_courses_free'

# File to store headings
HEADINGS_FILE = 'headings.txt'

# LinkedIn API Credentials
def get_linkedin_credentials():
    current_time = datetime.now(timezone.utc).time()
    if time(0, 0) <= current_time <= time(9, 0):
        return {  #Details for first page - Free Online Courses with Certificate
            "LINKEDIN_CLIENT_ID": "77mvys501xj2cc",
            "LINKEDIN_CLIENT_SECRET": "WPL_AP1.UZRuv0IgRx7N2AxJ.l+Yh3A==",
            "LINKEDIN_ACCESS_TOKEN": "AQU5PGh9_4sQEcLoW7Xd0q5E0EVwmeO7j-30_1YlQd0pn2gMoFtOnP36v8w7dD2X6CrZITuF2rsvcfYmgypdDSPYMV16Ch9jXQ_K7fw0uIH46LuSb1F4IpFXaYPBiB6z40cgftVw4DoIw7lxBBiO0N14d3euZi11JARRE0cWlqVS9lwP8GH3nwV1CQ6DXWb2XiGG-CbA_q6z2Dt6VjVQVsV3htErGuF5qAEy2KwL3ufrZMJNHIntu4P5f2mrIls6uqvHkjAWKfAOZH6a4LU8amgDDL2wC4uyZAmXxyXQxLDvLQ2AVovUiD5m_6uAWOrHmSPghFtQWQrg1lXuuPwO57vG_PQPmw",
            "LINKEDIN_URN": "urn:li:organization:105818491"
        }
    else:
        return {  #Details for second page - Free Online Courses
            "LINKEDIN_CLIENT_ID": "782eyho8suoltk",
            "LINKEDIN_CLIENT_SECRET": "WPL_AP1.SO2Em0vEjfahwu6h.se5poQ==",
            "LINKEDIN_ACCESS_TOKEN": "AQXJjIa0JGLx0d_KAlwJzzhqMDS9Kk5b0xztPTTCKSXOCfcpuWzE2QhKlSS3bgov9N4bB8cRyRqkrDdNwqhcrwVHJEjv8bjxK0Hhav-duD6kGMnL0Ro_SkI7H--XphvCCsmZwBmhZYatGWBEpHi7zP6oMG1c139vcdMnkPlaN49jfxNJ6YQxDNvojXGgi6EmG7jT8UHEZfRgah7ASX_cJmrhjYjPQ44_n0c8-vrwSCAgAa3WJ2-IT8xYbtEc7ZQie81mHFEUJm_H-irGJ2YNFOn1EKyvom2dv97A1_S6jbuZmfd77KwKulEzlNU5vLP6APPk1fBwCpIBzWmRfeKHeaY4AWIGDA",
            "LINKEDIN_URN": "urn:li:organization:106329110"
        }


# LinkedIn API Endpoint
LINKEDIN_API_URL = "https://api.linkedin.com/v2/ugcPosts"

# Create the client
client = TelegramClient('butterfly_tg_bot_login_session', API_ID, API_HASH)

# Function to extract details and format the message
def format_message(message_text, button_url):
    # Extract details using regex or string manipulation
    title_match = re.search(r'\*\*(.*?)\*\*', message_text)
    description_match = re.search(r'__(.*?)__', message_text)
    course_length_match = re.search(r'Content: `(.*?)`', message_text)
    language_match = re.search(r'Language: #(\w+)', message_text)

    # Extract values
    title = title_match.group(1) if title_match else "Unknown Title"
    description = description_match.group(1) if description_match else "No Description"
    course_length = course_length_match.group(1) if course_length_match else "Unknown Length"
    language = language_match.group(1) if language_match else "Unknown Language"

    # Format the message
    formatted_message = (
        f"**{title}**\n"
        "———————————————————\n"
        f"__{description}__\n"
        "———————————————————\n"
        "✳️ 100% Free\n"
        "❇️ **Certificate:** Yes\n"
        "✳️ **Lifetime Free Access after Enrollment**\n"
        f"🕒 **Course Length:** {course_length}\n"
        f"📗 **Language:** {language}\n"
        "———————————————————\n"
        f"🔴 **Expiry:**  Few Hours Left\n"
        f"⚠️ **Only Few Coupons Left | Enroll Fast**\n"
        "———————————————————\n\n"
        f"**🎫 Enroll Now:**\n"
        f"{button_url}\n\n"
        "———————————————————\n"
        "**For More Courses ➛** https://t.me/free_course_udemy_online\n\n"
        "**MS Office Courses ➛** https://t.me/msofficecourses\n"
        "**Python Courses ➛** https://t.me/pythonlearnerss\n"
        "**Web Development Courses ➛** https://t.me/webdesignlrn\n\n"
        "**Join for more updates!**"
    )

    linkedin_message = (
        f"{title}\n"
        "———————————————————\n"
        f"{description}\n"
        "———————————————————\n"
        "✳️ 100% Free\n"
        "❇️ Certificate: Yes\n"
        "✳️ Lifetime Free Access after Enrollment\n"
        f"🕒 Course Length: {course_length}\n"
        f"📗 Language: {language}\n"
        "———————————————————\n"
        f"🔴 Expiry:  Few Hours Left\n"
        f"⚠️ Only Few Coupons Left | Enroll Fast\n"
        "———————————————————\n"
        f"🎫 Enroll Now:\n"
        f"{button_url}\n"
        "———————————————————\n"
        "For More Courses ➛ https://t.me/free_course_udemy_online\n"
        # "For MS Office Courses ➛ https://t.me/msofficecourses\n"
        # "For Python Programming Courses ➛ https://t.me/pythonlearnerss\n"
        # "For Web Development Courses ➛ https://t.me/webdesignlrn\n\n"
        "Everyday we post hundreds of free courses of several categories in our telegram Channel. Join our telegram for more updates\n\n"
        "———————————————————\n"
        "Follow for More Updates\n\n"
        "#onlinecourse #database #it #informationtechnology #php #mysql #java #c #python #SQL #AWS #GoogleCloud #javascript #frontend #backend #webdevelopment #programming #word #excel #powerpoint #Office #photoshop #illustrator #adobe #canva #udemy #freeonlinecourses #premium #course #onlione #free"
    )

    facebook_post = (
        f"**{title}**\n"
        "———————————————————\n"
        f"{description}\n"
        "———————————————————\n"
        "✳️ 100% Free\n"
        "❇️ Certificate: Yes\n"
        "✳️ Lifetime Free Access after Enrollment\n"
        f"🕒 Course Length: {course_length}\n"
        f"📗 Language: {language}\n"
        "———————————————————\n"
        f"🔴 Expiry:  Few Hours Left\n"
        f"⚠️ Only Few Coupons Left | Enroll Fast\n"
        "———————————————————\n"
        f"✅✅✅ For Enroll Link please check first comment. ✅✅✅\n"
        "———————————————————\n"
        "Everyday we post hundreds of free courses of several categories in our telegram Channel. Join our telegram for more updates\n\n"
        "———————————————————\n"
        "#onlinecourse #database #it #informationtechnology #php #mysql #java #c #python #javascript #frontend #backend #webdevelopment #programming #word #excel #powerpoint #Office #photoshop #illustrator #adobe #udemy #freeonlinecourses #premium #course #onlione #free"
    )

    facebook_comment = (
        f"🎫 Enroll Link:\n"
        f"{button_url}\n"
        "———————————————————\n"
        "For More Courses Join ➛ https://t.me/free_course_udemy_online\n"
    )

    special_message = (
        f"**{title}**\n\n"

        f"**Description: ** __{description}__\n\n"

        "❇️ **Certificate:** After completion of the course\n"
        "✳️ **100% Free and Lifetime Free Access after Enrollment**\n\n"
        f"🕒 **Course Length:** {course_length}\n"
        f"📗 **Language:** {language}\n\n"

        f"🔴 **Only Few Coupons Left | Enroll Fast**\n\n"

        f"**🎫 Enroll Now:**\n"
        f"{button_url}\n\n"

        "**For More Courses ➛** https://t.me/online_premium_courses_free\n\n"
        "**Join our channel for unlimited free courses**"
    )

    return formatted_message, title, linkedin_message, facebook_post, facebook_comment, special_message

# Function to check if a heading is already in the file
def is_heading_already_posted(heading):
    try:
        with open(HEADINGS_FILE, 'r', encoding='utf-8') as file:
            headings = file.read().splitlines()
        return heading in headings
    except FileNotFoundError:
        return False

# Function to add a heading to the file
def add_heading_to_file(heading):
    with open(HEADINGS_FILE, 'a', encoding='utf-8') as file:
        file.write(f"{heading}\n")

# Function to post to LinkedIn
def post_to_linkedin(text):
    credentials = get_linkedin_credentials()
    headers = {
        "Authorization": f"Bearer {credentials['LINKEDIN_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": credentials["LINKEDIN_URN"],
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(LINKEDIN_API_URL, headers=headers, json=payload)
    return response.status_code, response.json()

# Function to process a message
async def process_message(message):
    try:
        # Get the message text
        message_text = message.text

        t.sleep(2)

        # Extract the button URL (enrollment link) from the button with text "🔗 Enroll Course 🔗"
        button_url = None
        buttons = message.buttons

        if buttons:
            for row in buttons:
                for button in row:
                    if 'Enroll' in button.text and button.url:
                        button_url = button.url
                        break

        if button_url:
            # Format the message
            formatted_message, title, linkedin_message, facebook_post, facebook_comment, special_message = format_message(message_text, button_url)

            # Check if the heading is already posted
            if not is_heading_already_posted(title):
                # Send the formatted message to the target channel
                await client.send_message(TARGET_CHANNEL, formatted_message, link_preview=False)
                # Add the heading to the file
                add_heading_to_file(title)
                print(f"Formatted message with title --{title}-- forwarded to {TARGET_CHANNEL}.")
                # Post the message to LinkedIn
                status_code, response = post_to_linkedin(linkedin_message)
                if status_code == 201:
                    print("Successfully posted to LinkedIn!")
                else:
                    print(f"Failed to post to LinkedIn. Error: {response}")

                # Check if the heading contains 'excel' and forward to the additional channel
                msofficekeywords = ['ms word', 'microsoft word', 'excel', 'powerpoint', 'google slide']
                if any(keyword in title.lower() for keyword in msofficekeywords):
                    await client.send_message(MSOFFICE_TARGET_CHANNEL, formatted_message, link_preview=False)

                pythonkeywords = ['python']
                if any(keyword in title.lower() for keyword in pythonkeywords):
                    await client.send_message(PYTHON_TARGET_CHANNEL, formatted_message, link_preview=False)
                
                webkeywords = ['web development','html','html5','css','css3','bootstrap', 'wordpress']
                if any(keyword in title.lower() for keyword in webkeywords):
                    await client.send_message(WEB_TARGET_CHANNEL, formatted_message, link_preview=False)               

                facebookpost = ['ms word', 'microsoft word', 'excel', 'powerpoint', 'google slide', 'python', 'web development','html','html5','css','css3','bootstrap', 'adobe', 'photoshop', 'illustrator','digital marketing','canva']                
                if any(keyword in title.lower() for keyword in facebookpost):
                    await client.send_message('@mdkhaledurbd', facebook_post)
                    await client.send_message('@mdkhaledurbd', facebook_comment) 
                
                special_tg = ['ms word', 'microsoft word', 'excel', 'powerpoint', 'google slide', 'python', 'web development','html','html5','css','css3','bootstrap', 'adobe', 'photoshop', 'illustrator','digital marketing','canva','jave','cyber security','wordpress','javascript','mysql','php','angularjs','ethical hacking','linux','figma','ui ux','ux ui']
                if any(keyword in title.lower() for keyword in special_tg):
                    await client.send_message(SPECIAL_CHANNEL, special_message, link_preview=False)
                
                demochannelpost = msofficekeywords + webkeywords
                demochannels = ['@free_online_premium_course','@online_premium_course','@freeonlinecoursescertificate','@netflix_premum','@deepseek_ai_updates','@coursesfreeee']
                if any(keyword in title.lower() for keyword in demochannelpost):
                    for channel in demochannels:
                        await client.send_message(channel, formatted_message, link_preview=False)


            else:
                print(f"Message with title '{title}' already posted. Skipping.")
        else:
            print("No 'Enroll' button found in the message.")
    except Exception as e:
        print(f"Failed to process message: {e}")

# Function to fetch and process the last 10 messages
async def fetch_last_10_messages():
    # Fetch the last 10 messages from the source channel
    messages = await client.get_messages(SOURCE_CHANNEL, limit=51)

    for message in messages:
        await process_message(message)

# Event handler for new messages in the source channel
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    await process_message(event.message)

# Function to restart the program
def restart_program():
    print("Restarting the program...")
    python = sys.executable
    script = os.path.abspath(sys.argv[0])
    # Properly quote the Python executable and script path
    command = f'"{python}" "{script}"'
    print(f"Running command: {command}")
    subprocess.Popen(command, shell=True)
    sys.exit(0)

# Schedule the program to restart every 2 minutes
schedule.every(2).minutes.do(restart_program)

# Main function to run the client
async def main():
    await client.start(PHONE_NUMBER)
    # print(f"Fetching last 50 messages from {SOURCE_CHANNEL}...")----------------------------------
    await fetch_last_10_messages()
    # print(f"Listening for new messages in {SOURCE_CHANNEL}...")----------------------------------

    # Run the client in a non-blocking way
    client_task = asyncio.create_task(client.run_until_disconnected())

    # Keep the program running to check for scheduled tasks
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Run the client
with client:
    client.loop.run_until_complete(main())
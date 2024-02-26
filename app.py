from flask import Flask, request, jsonify
from yowsup.stacks import YowStack
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_chatstate.protocolentities import MessageTextProtocolEntity
from yowsup.layers.protocol_media.media_download_request import DownloadRequestIqProtocolEntity
from yowsup.layers.protocol_media.media_upload_request import UploadRequestIqProtocolEntity
from PIL import Image
import os
import requests
import ytdl-core

app = Flask(__name__)

# Replace these values with your actual credentials and session ID
PHONE_NUMBER = "your_phone_number"
SESSION_ID = "your_session_id"
BOT_NAME = "🅼🆁 🆂🅴🅽🅰🅻"
BOT_LOGO_URL = "https://telegra.ph/file/f2be313fe820b56b47748.png"

# Create a media directory if it doesn't exist
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

def on_message_received(stack, event):
    if event.ack:
        return
    message = event.get_data()
    sender = event.get_from()
    if isinstance(message, MessageTextProtocolEntity):
        handle_text_message(message, sender)
    elif isinstance(message, MessageMediaDownloadableProtocolEntity):
        handle_media_message(message, sender)
    elif isinstance(message, MessageProtocolEntity):
        handle_group_message(message, sender)

def handle_text_message(message, sender):
    text = message.getBody().lower()
    if text.startswith(".song"):
        send_message(sender, "🎧")
        download_song_details(message, sender)
    elif text.startswith(".video"):
        send_message(sender, "🎬")
        download_video_details(message, sender)
    elif text.startswith(".apk"):
        send_message(sender, "💾")
        download_apk_details(message, sender)
    elif text.startswith(".menu"):
        send_menu_message(sender)
    else:
        # Handle other text messages
        pass

def download_song_details(message, sender):
    songName = message.getBody().split(" ")[1]
    # Use YouTube API to search for the song and get details
    # Send details back to the user
    send_message(sender, f"Downloading details for song: {songName}...")

    # Ask for confirmation
    send_message(sender, "ඔයාට ඕනිද මේක ඩවුන්ලෝඩ් කරන්න 😇🧐  yes or no")

def download_video_details(message, sender):
    videoName = message.getBody().split(" ")[1]
    # Use YouTube API to search for the video and get details
    # Send details back to the user
    send_message(sender, f"Downloading details for video: {videoName}...")

    # Ask for confirmation
    send_message(sender, "ඔයාට ඕනිද මේක ඩවුන්ලෝඩ් කරන්න 😇🧐  yes or no")

def download_apk_details(message, sender):
    appName = message.getBody().split(" ")[1]
    # Use Play Store API to search for the app and get details
    # Send details back to the user
    send_message(sender, f"Downloading details for app: {appName}...")

    # Ask for confirmation
    send_message(sender, "ඔයාට ඕනිද මේක ඩවුන්ලෝඩ් කරන්න 😇🧐  yes or no")

def send_menu_message(sender):
    message = (
        "▂▃▅▇█▓▒░ THIS IS MENU FOR Mr SENAL ░▒▓█▇▅▃▂\n\n"
        "01 Song Downloader ➡️ .song\n"
        "02 Video Downloader ➡️ .video\n"
        "03 App Downloader ➡️ .apk\n"
        "04 Sticker Downloader ➡️ .sticker\n\n"
        "ɢᴇɴᴇʀᴀᴛᴇ ʙʏ ᴍʀ ꜱᴇɴᴀʟ"
    )
    send_message(sender, message)

def send_message(receiver, message):
    stack = YowStack.get_instance()
    stack.broadcast(YowLayerEvent(MessageTextProtocolEntity(message), to=receiver))

if __name__ == "__main__":
    stack_builder = YowStack.builder()
    stack = stack_builder.push_default_layers(True).build()

    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, "s.whatsapp.net:443")
    stack.setProp(YowNetworkLayer.PROP_USER, PHONE_NUMBER)
    stack.setProp(YowNetworkLayer.PROP_SESSION_ID, SESSION_ID)

    stack.set_callback("message_received", on_message_received)

    stack.start()
    app.run(port=8080, debug=True)

import os
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# In kiểm tra token
print(f"✅ Đang dùng TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10]}...")
print(f"✅ Đang dùng OPENROUTER_API_KEY: {OPENROUTER_API_KEY[:10]}...")

# Hàm gửi yêu cầu tới OpenRouter
def chat_with_openrouter(message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  # dùng đúng định danh
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý AI tên là Tiểu Thiên, nói tiếng Việt, thân thiện và thông minh."},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return reply.strip()
    else:
        print("⚠️ Lỗi khi gọi API OpenRouter:")
        print("Status:", response.status_code)
        print("Response:", response.text)
        return "😥 Xin lỗi, Tiểu Thiên không thể trả lời lúc này."

# Hàm xử lý tin nhắn người dùng
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    ai_reply = chat_with_openrouter(user_message)
    update.message.reply_text(ai_reply)

# Hàm khởi động bot
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Đăng ký handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("🤖 Tiểu Thiên đã khởi động!")
    updater.idle()

if __name__ == "__main__":
    main()

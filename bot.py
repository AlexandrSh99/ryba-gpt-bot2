import os
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

if not BOT_TOKEN or not OPENAI_API_KEY:
    print("❌ BOT_TOKEN или OPENAI_API_KEY не найдены в .env")
    exit()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Привет! Я GPT-бот по рыбалке 🎣 Задай вопрос!")

@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Ты опытный рыбак. Отвечай просто и по делу."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message["content"]
        await message.reply(reply)
    except Exception as e:
        print(f"❌ Ошибка при запросе к OpenAI: {e}")
        await message.reply("Ошибка при обращении к GPT. Попробуй позже.")

if __name__ == "__main__":
    print("✅ Бот запущен на Render!")
    executor.start_polling(dp)

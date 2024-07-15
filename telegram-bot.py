import logging
import os
from chatgpt_client import request_chat_gpt
import requests
# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle
# import matplotlib.pyplot as plt
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)
from    custom_persona import custom_persona

GPT_BASE_URL = "https://app.customgpt.ai/api/v1/projects/37096/conversations/"
session_id = ""


load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Good morning Mike! please talk to me!")

    payload = { "name": "new_question" }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer 4378|hU0E3IRkNysYzHI5oNSNBKEKKEDdoK9gD9H7g7op34cfff59"
    }

    response = requests.post(GPT_BASE_URL, json=payload, headers=headers)
    
    # Get the session id, to keep talking in the same converstion until new "/start"
    global session_id
    session_id = response.json()["data"]["session_id"]

async def send_msg_to_custom_gpt(message):
    """ Send a message to our custom gpt and get it's response """
    
    global session_id

    url = GPT_BASE_URL + session_id + "/messages?stream=false&lang=en"
    payload = {
        "prompt": message,
        "response_source": "openai_content", # "own_content"
        "custom_persona": custom_persona,
        "chatbot_model": "gpt-4-o"
    }
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "authorization": "Bearer 4378|hU0E3IRkNysYzHI5oNSNBKEKKEDdoK9gD9H7g7op34cfff59"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        res_text = response.json()["data"]["openai_response"]
        return res_text
    except:
        print("Error in send_msg_to_custom_gpt: ")
        print(response.json())

    


async def send_to_telegrem(update: Update, context: ContextTypes.DEFAULT_TYPE, message):
    """ Function that sends a message bacl to telegrem """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    # await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("./assets/david.png", 'rb'))
    # await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("assets/david.png", 'rb'))
    # await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/assets/david.png", 'rb'))


async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await send_msg_to_custom_gpt(update.message.text)
    await send_to_telegrem(update, context, response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    new_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_new_message)
    application.add_handler(start_handler)
    application.add_handler(new_message_handler)

    application.run_polling()


# # LaTeX expression
# latex = r'$\int_{a}^{b} x^2 \mathrm{d}x$'

# # Create figure and axis
# fig, ax = plt.subplots()

# # Set limits to ensure the whole LaTeX expression is shown
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)

# # Render LaTeX expression
# ax.text(0.5, 0.5, latex, va='center', ha='center', fontsize=16)

# # Hide axes
# ax.axis('off')

# # Save the figure as an image
# plt.savefig('latex_expression.png', dpi=300, bbox_inches='tight')

# # Show the plot (optional)
# plt.show()

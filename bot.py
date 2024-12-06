from dotenv import load_dotenv
import os
import telebot
import requests


# Load environment variables
load_dotenv("C:/Users/Kunal Sharma/Downloads/BOT/bot1.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")


#this is just a loop to test if the bot token is loaded or not 
if not BOT_TOKEN:
    print("Error: BOT_TOKEN not found!")
    exit()

print("Bot token loaded")   
bot = telebot.TeleBot(BOT_TOKEN)

# Debug log for bot start
print("Bot is running... Waiting for messages.")


#the bot will respond with this message after start and hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print(f"Received command: {message.text} from {message.chat.username}")
    bot.reply_to(message, "Holla MOFO, What's happening")

# #this function is used to print back the message sent to the bot 
# @bot.message_handler(func=lambda msg: True)
# def echo_back(message):
#     print(f"Received message: {message.text} from {message.chat.username}")
#     bot.reply_to(message, message.text)

def get_daily_horoscope(sign: str, day: str) -> dict:
    """
    This function fetches the daily horoscope for a given sign and day from the API
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()

# this is the fuction for the /horoscope command 
@bot.message_handler(commands= ['horoscope'])
def ask_sign(message):
    """
    Handles the /horoscope command by asking the user about their zodiac sign
    """
    text = "What's you zodiac sign?\nChoose one of the these: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces* "
    sent_message  = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_message, day_handler)


# This function handles the day of the requested hororsocpe
def day_handler(message):
    """
    Handles the user's request for a horoscope by asking which day's horoscope
    they want to know. Sends a message prompting for the day and registers the
    next step handler to fetch the horoscope based on the user's input.

    """
    sign = message.text
    text = "Which day's horoscope do you want to know: *Today*,*Tomorrow*,*Yesterday* or you can type the date YYYY-MM-DD."
    sent_message = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_message, fetch_horoscope, sign.capitalize())


# This here fecthes the horoscope form the api and sends it to the user 
def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Your horoscope is the worst for the next year, nah just kidding,here is the real horoscope")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")



#Exception for the infinity pooling 
while True:
    try:
        print("Polling for updates...")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Error occurred: {e}")

import telebot
from ai import get_scenario_list, ChatState
from bot_internal import get_record, update_record, process_prompt
from bot_token import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

scenario = [
    {'id': 0, 'prompts': ['Update ID', 'ID expired', 'How to change ID', 'ID is lost'],
        'nextPrompt': 1, 'type': 'initial', 'confirm': 'Do you need help with your ID?'},
    {'id': 1, 'label': 'What happend to your previous ID?', 'prompts': ['ID is lost', 'ID is expired', 'Getting id first time'], 'type': 'choose', 'action': [
        'New ID instruction', 'Update ID instruction', 'First ID instruction'], 'confirm': ['Is your ID lost?', 'Is your ID expired?', 'Do you want to get ID for the first time?']},
    {'id': 2, 'prompts': ['Tax info', 'Get my taxes'], 'type': 'initial',
        'action': 'Get tax info', 'confirm': 'Do you want to find out info about your taxes?'},
    {'id': 3, 'prompts': ['Get docs info', 'ID info', 'My profile info', 'My documents info'],
        'nextPrompt': 4, 'type': 'initial', 'confirm': 'Do you want to see your documents info?'},
    {'id': 4, 'label': 'What document info do you want to get?', 'prompts': ['ID', 'Driver License', 'Medical insurance'], 'type': 'choose', 'action': [
        'Getting ID info...', 'Getting Driver License info...', 'Getting medical insurance info...'], 'confirm': ['Do you want to get ID info', 'Do you want to get driver license info?', 'Do you want to get medical unsurance info?']},
    {'id': 5, 'prompts': ['Family info', 'Siblings info', 'Mother or father info', 'Kids info'], 'type': 'initial',
        'action': 'Getting info about your family...', 'confirm': 'Do you want to find out info about your family?'},
    {'id': 6, 'prompts': ['Appointment at the hospital', 'Get medical help'],
    'action': 'Setting an appointment for you...', 'type': 'initial', 'confirm': 'Do you need to get an ppointment at the hospital?'},
]
scenario_prompts = get_scenario_list(scenario)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi! This is a demo of a chatbot, which can recognise your text prompts 
and map them to some certain scenarios. Try it!
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['text'])
def echo_message(message):
    chat_id = message.chat.id
    record = get_record(chat_id)
    if record is None:  # first message, create record
        update_record(chat_id, ChatState.INITIAL, None)

    process_prompt(bot, scenario, scenario_prompts, message)


bot.infinity_polling()

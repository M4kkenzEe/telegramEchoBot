import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
from random import randint, choice
from glob import glob
from emoji import emojize

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text(f'Че каво {smile()}\n'
                              'Вводи /waifu пока световой меч не отсохнет!!!))))\n'
                              'Список команд: /help\n')


def talk_to_me(update, context):
    print('Сообщение зеркало')
    text = update.message.text
    print(text)
    update.message.reply_text(text, f'{smile()}')


def smile():
    smilee = choice(settings.USER_EMOJI)
    return emojize(smilee, use_aliases=True)


def play_random_numbers(user_number):
    print('Вызов команды /guess')
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число: {user_number}, мое число: {bot_number}\nвы выиграли!'
    elif user_number == bot_number:
        message = f'Ваше число: {user_number}, мое число: {bot_number}\nНичья...'
    else:
        message = f'Ваше число: {user_number}, мое число: {bot_number}\nЯ победил, а ты проиграл))'
    return message


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите число'
    update.message.reply_text(message)


def send_girl_pic(update, context):
    print('Вызов команды /waifu')
    cat_photos_list = glob('datacat/*.*')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def rules(update, context):
    update.message.reply_text('1. Сыграй с ботом в игру загадай число и введи /guess "твоё число"\n'
                              '2. Найди свою вайфу /waifu\n---------------------------------\n'
                              'Также напиши что то свое и бот за тобой повторит)')


def main():
    mybot = Updater(settings.API_KEY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', rules))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('waifu', send_girl_pic))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()


main()

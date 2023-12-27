import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

questions = [
    {"question": "Сколько планет в Солнечной системе?", "options": ["A) 8", "B) 9", "C) 10", "D) 7"], "correct": "A"},
    {"question": "Какое самое большое озеро в мире?", "options": ["A) Байкал", "B) Каспийское море", "C) Онтарио", "D) Виктория"], "correct": "A"},
    {"question": "Какой год основания Рима?", "options": ["A) 753 до н.э.", "B) 500 до н.э.", "C) 200 до н.э.", "D) 100 н.э."], "correct": "A"},
    {"question": "Какой химический элемент обозначается как 'O'?", "options": ["A) Оксиген", "B) Олово", "C) Оловян", "D) Орегано"], "correct": "A"},
    {"question": "Какой язык программирования самый популярный?", "options": ["A) Python", "B) Java", "C) C++", "D) JavaScript"], "correct": "A"}
]

user_scores = {}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("A", callback_data='A'), InlineKeyboardButton("B", callback_data='B'))
    markup.row(InlineKeyboardButton("C", callback_data='C'), InlineKeyboardButton("D", callback_data='D'))

    current_question = user_scores.get(message.from_user.id, 0)
    current_options = questions[current_question]["options"]
    current_question_text = f"{questions[current_question]['question']}\n"
    current_question_text += "\n".join(current_options)

    await message.reply(current_question_text, reply_markup=markup)


@dp.callback_query_handler(lambda c: True)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    answer = callback_query.data
    user_id = callback_query.from_user.id

    if user_id not in user_scores:
        user_scores[user_id] = 0

    current_question = user_scores[user_id]

    if answer == questions[current_question]["correct"]:
        user_scores[user_id] += 1

    if current_question < len(questions) - 1:
        user_scores[user_id] += 1
        next_question = questions[current_question + 1]
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("A", callback_data='A'), InlineKeyboardButton("B", callback_data='B'))
        markup.row(InlineKeyboardButton("C", callback_data='C'), InlineKeyboardButton("D", callback_data='D'))

        next_question_text = f"{next_question['question']}\n"
        next_question_text += "\n".join(next_question["options"])

        await bot.send_message(user_id, f"Правильно! Твой текущий счет: {user_scores[user_id]}.\n\n{next_question_text}",
                               reply_markup=markup)
    else:
        await bot.send_message(user_id, f"Викторина завершена! Твой итоговый счет: {user_scores[user_id]}.")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)

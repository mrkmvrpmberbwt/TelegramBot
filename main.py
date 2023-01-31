from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


TOKEN_API = '5936465870:AAGWKVN4llqT7Kv5jr7bk1dHKwGY3J7zVa0'
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

users={}
allInterest=[]
allComand=['Добавить новые интересы', 'Посмотреть Людей', 'Редактировать интересы']

def createBtn(btns):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for i in btns:
        kb.add(KeyboardButton(i))
    return kb

@dp.message_handler(commands=['start'])
async def start_comand(message: types.Message):
    users[message.chat.id] = {
        "action_type": 0,
        "select_action": [],
        "action_type1": 0
    }
    kb = createBtn(allComand)
    await message.answer(text='саламалееееееееееееееееееееееееееееейкум ИИИИИИИИИИИИИИИИУУУУУУУУУУ суита на связи есть жи да уууууууууууууу', reply_markup=kb)

@dp.message_handler()
async def main(message: types.Message):
    msgText= message.text
    userId=message.chat.id
    actType = users[userId]['action_type']
    if msgText in allComand or actType != 0:
        if actType == 0:
            if msgText == 'Добавить новые интересы':
                kb = createBtn(['Вписать новые интересы', 'Выбрать интерес который уже вводили другие пользователи'])
                await message.answer(text='Выберите:', reply_markup=kb)
                users[userId]['action_type1'] = 1

                if users[userId]['action_type1'] == 1 and msgText == 'Вписать новые интересы':
                    await message.answer(text='Введите свои интересы')
                    users[userId]['action_type'] = 1

                elif users[userId]['action_type1'] == 1 and msgText == 'Выбрать интерес который уже вводили другие пользователи':
                    for i in allInterest:
                        kb = createBtn (i)
                    await message.answer(text='Нажмите на интерес который хотите добавить', reply_markup=kb)
                    users[userId]['action_type'] = 2
######################################################################################################################




    else:
            if users[userId]['action_type'] == 1: # Добавление своего интереса
                texts = (message.text.lower().translate({ord(','): None})).split()
                for i in texts:
                    users[userId]['select_action'].append(i)
                    allInterest.append(i)
                users[userId]['action_type'] = 0
                kb = createBtn(allComand)
                await message.answer(text='Выши статьи сохранены.', reply_markup=kb)

            if users[userId]['action_type'] == 2: #Выбар интереса из списка
                users[userId]['select_action'].append(msgText)
                kb = createBtn(allComand)
                await message.answer(text='Новый интерес был добавлен', reply_markup=kb)
                users[userId]['action_type'] = 0



if __name__ == '__main__':
    executor.start_polling(dp)
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(os.getenv("TOKEN_API"))
dp = Dispatcher(bot)

spam=[]
editInteres=[]
chooseInteres=[]
getInteres=[]
writeInteres=[]
users = {}
test='test'
allInteres=[]
allComand = ['Добавить новые интересы', 'Посмотреть Людей', 'Редактировать интересы']

def createBtn(btns):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for i in btns:
        kb.add(KeyboardButton(i))
    return kb

@dp.message_handler(commands=['start'])
async def start_comand(message: types.Message):
    userName= message['chat']['first_name']
    users[message.chat.id] = {
        "select_interes": [],
        'name': userName,
        'general':0,
        'spam':0
    }
    print(users[message.chat.id])
    kb = createBtn(allComand)
    await message.answer(text='саламалееееееееееееееееееееееееееееейкум ИИИИИИИИИИИИИИИИУУУУУУУУУУ суита на связи есть жи да уууууууууууууу', reply_markup=kb)


@dp.callback_query_handler()
async def callback (callback: types.CallbackQuery):
    print(callback)
    idUser = callback['from']['id']
    texts = callback['data']
    userInteres=users[idUser]['select_interes']
    #pawait bot.delete_message(chat_id=, message_id=,)
    if callback.data in userInteres and len(chooseInteres)==0 :
        if 'choose' in editInteres:
            await callback.answer(text='Перед тем как открывать меню убедитесь, что вы закрыли прошлое меню')
        elif texts != 'choose' and texts != 'back':
            print('frec')
            await callback.answer(text='Тема была удалена')
            users[idUser]['select_interes'].remove(texts)
            print(users[idUser]['select_interes'])
            ikb = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
            ib1 = types.InlineKeyboardButton(text='Назад', callback_data='back')
            for i in userInteres:
                ib = types.InlineKeyboardButton(text=i, callback_data=i)
                ikb.add(ib)
            ikb.add(ib1)
            await callback.message.edit_reply_markup(reply_markup=ikb)

    elif callback.data =='choose':
        users[idUser]['spam']=0
        editInteres.append("choose")
        if 'edit' in editInteres:
            editInteres.remove('edit')
        if len(allInteres) == 0:
            kb = createBtn(allComand)
            await callback.answer(text='В даный момент добавленых интересов нет')
        else:
            print('a')
            kb = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
            mk = types.InlineKeyboardButton(text='Назад', callback_data='back1')
            for i in allInteres:
                write = types.InlineKeyboardButton(text=i, callback_data=i)
                kb.add(write)
            kb.add(mk)
            editMessage=await callback.message.edit_text(text='Нажмите на интерес, что бы добавить его к себе.')
            await callback.message.edit_reply_markup(reply_markup=kb)
            chooseInteres.append(idUser)

    elif idUser in chooseInteres:
        users[idUser]['spam'] = 0
        if "edit" in editInteres:
            await callback.answer(text='Перед тем как открывать меню убедитесь, что вы закрыли прошлое меню')
        elif texts!= 'choose' and texts!='back':
            if texts in userInteres:
                await callback.answer(text='Эта статья была добавлена раньше')
                chooseInteres.remove(idUser)
                #await callback.message.delete()

            else:
                print('fgrdsv')
                userInteres.append(texts)
                print(userInteres)
                await callback.answer(text='Интерес был добавлен')
                chooseInteres.remove(idUser)

    elif callback.data == 'write':
        users[idUser]['spam'] = 0
        await callback.answer (text='Введите интересы через запятую')
        await callback.message.delete()
        writeInteres.append(idUser)

    if callback.data =='back':
        users[idUser]['spam'] = 0
        if 'edit' in editInteres:
            editInteres.remove('edit')
        await callback.message.delete()

    if callback.data == 'back1':
        users[idUser]['spam'] = 0
        if 'choose' in editInteres:
            editInteres.remove('choose')
        if idUser in chooseInteres:
            chooseInteres.remove(idUser)
        await callback.message.delete()

@dp.message_handler()
async def main(message: types.Message):
    msg=message.text
    userId=message.chat.id
    userInteres= users[message.chat.id]["select_interes"]

    if msg == 'Добавить новые интересы':
        users[userId]['spam']+=1
        ikb = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        im1 = types.InlineKeyboardButton(text="Вписать новые интересы", callback_data="write")
        im2 = types.InlineKeyboardButton(text="Выбрать интерес из списка", callback_data="choose")
        im3 = types.InlineKeyboardButton(text="Закрыть", callback_data="back")
        ikb.add(im1, im2, im3)

        spaam=await message.answer(text='Выберите, как вы хотите добавить интересы', reply_markup=ikb)
        if users[userId]['spam']>1:
            next_id = spaam.message_id
            await bot.delete_message(chat_id=userId, message_id=next_id)
            await message.delete()



    elif userId in writeInteres:# написать интерес
        texts = (message.text.lower().translate({ord(','): None})).split()
        for i in texts:
            if i in userInteres:
                print(i)
                userInteres.remove(i)
            if i in allInteres:
                allInteres.remove(i)
            print(i)
            userInteres.append(i)
            allInteres.append(i)
        kb = createBtn(allComand)
        await message.answer(text='интересы были добавлены', reply_markup=kb)
        writeInteres.remove(userId)
        return


    elif msg=='Редактировать интересы':
        if len(userInteres)==0:
            await message.answer(text='В даный момент у вас не выбраны интересные вам темы')
        else:
            editInteres.append('edit')
            ikb = types.InlineKeyboardMarkup (resize_keyboard=True, row_width=2)
            for i in userInteres:
                im=types.InlineKeyboardButton(text=i,callback_data=i)
                ikb.add(im)
            ib1 = types.InlineKeyboardButton(text='Назад', callback_data='back')
            ikb.add(ib1)

            await message.answer(text='нажмите на интерес который хотите удалить', reply_markup=ikb)

    elif msg=='Посмотреть Людей':
        print('fwefw')
        general=users[userId]["general"]
        answer={}
        for i in users:
            usersInteres=users[i]["select_interes"]
            userName=users[i]['name']
            print(usersInteres)
            if i!=userId:
                for i in usersInteres:
                    if i in userInteres:
                        general+=1
                if general>0:
                    await message.answer(text=f'С пользователем @{userName}, у вас {general} общие темы')
                    general=0
                if general<0:
                    await message.answer(text='На даный момент нет пользователей с такимиже интересами.')
    elif msg== 'Назад':
        kb=createBtn(allComand)
        await message.answer(text='', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# tools for teacher

teachBtn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть ключи 🔑', callback_data='viewDB')],
    [InlineKeyboardButton(text='Добавить 🔄', callback_data='addData'), 
     InlineKeyboardButton(text='Удалить ❌', callback_data='deleteData')]
])

onlyAdd = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить 🔄', callback_data='addData')]
])

addMessage = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='backData')]
])

deleteMessage = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да ✅', callback_data='confirmData'),
    InlineKeyboardButton(text='Нет ❌', callback_data='backData')]
])



# tools for students
def testKeyboard(unique_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='A', callback_data=f'answer_A_{unique_id}'),
         InlineKeyboardButton(text='B', callback_data=f'answer_B_{unique_id}'),
         InlineKeyboardButton(text='C', callback_data=f'answer_C_{unique_id}'),
         InlineKeyboardButton(text='D', callback_data=f'answer_D_{unique_id}')]
    ])


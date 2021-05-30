import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import quote_html
logging.basicConfig(level=logging.INFO)

bot = Bot('', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def guide_cmd(message: types.Message):
    await message.reply(
        quote_html(
            "Here's what I can do:\n\n"
            "/btns <count:int> <text> - create a new keyboard\n"
            "/rm - clear the keyboard"
        )
    )


@dp.message_handler(commands=["btns"])
async def buttons_cmd(message: types.Message):
    user = message.from_user
    chat = message.chat

    args = message.get_args()
    chats: dict = ... # your db
    data: list = chats[chat.id]

    if chat.type == "private":
        return await message.answer("I only work in chat")

    markup = types.ReplyKeyboardMarkup(row_width=10)

    try:
        check_user = await chat.get_member(user.id)
        if check_user.status == "creator" or user.id in data:
            rn = int(args.split()[0])
            text = args.split(maxsplit=1)[1]
            b = types.KeyboardButton(text)
            if rn >= 11:
                return await message.reply("<b>RANGE</b> must be from 1 to 10")

            for _ in range(rn):
                markup.add(b, b, b, b, b, b, b, b, b, b)
            return await message.reply("Done!", reply_markup=markup)

    except (IndexError, ValueError):
        try:
            b = types.KeyboardButton(args or "No arguments.")
            for _ in range(10):
                markup.add(b, b, b, b, b, b, b, b, b, b)
            return await message.reply("Done!", reply_markup=markup)

        except Exception as e:
            return await message.reply(f"Error: {e}")

    except Exception as e:
        return await message.reply(f"Error: {e}")


@dp.message_handler(commands=["rm"])
async def rmButtons_cmd(message: types.Message):
    user =  message.from_user
    chat = message.chat

    if chat.type == "private":
        return await message.answer("I only work in chat")

    chats: dict = ... # your db
    data: list = chats[chat.id]

    check_user = await chat.get_member(user.id)
    if check_user.status == "creator" or user in data:
        return await message.reply("All buttons removed.", reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
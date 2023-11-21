"""
Weather bot for telegram
"""
import asyncio
import datetime
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import tg_token, open_weather_token


bot = Bot(tg_token)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: Message):
    """
    This is start button
    :param message:
    :return:
    """
    await message.answer(f"Привіт {message.from_user.first_name} !")
    await message.answer('Напишіть назву міста і я розкажу вам яка погода ')


@dp.message()
async def get_weather(message: Message):
    """
    the main functionality of the bot
    :param message:
    :return:
    """
    # weather pictures
    get_icon = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}'
            f'&appid={open_weather_token}'
            f'&units=metric&')
        data = req.json()
        city = data["name"]
        weather_description = data["weather"][0]["main"]
        if weather_description in get_icon:
            wd = get_icon[weather_description]
        else:
            wd = "Глянь у вікно "
        # weather parameters
        cur_weather = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        day_length = (datetime.datetime.fromtimestamp(data["sys"]["sunset"]) -
                      datetime.datetime.fromtimestamp(data["sys"]["sunrise"]))
        await message.answer(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                             f"Погода в місті {city}\n\n"
                             f"Температура {cur_weather}С° {wd}\n"
                             f"Відчувається як {feels_like}С°\n"
                             f"Вологість {humidity}%\n"
                             f"Атмосферний тиск {pressure} мм.рт.ст\nВітер {wind}м/c\n"
                             f"Світанок о {sunrise_timestamp} годині\n"
                             f"Захід сонця о {sunset_timestamp} годині\n"
                             f"Тривалість дня {day_length} годин\n\n"
                             f"Нехай проблеми на незгоди, не роблять Вам в житті погоди! "
                             f"Нехай щастить і гарного дня!")
    except NameError:
        await message.answer('Некоректна назва міста\nСпробуйте ще раз')


async def main():
    """
    this function launches a bot in Telegram
    :return:
    """
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

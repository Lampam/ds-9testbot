import pyowm
from pyowm.utils.config import get_default_config
import config
import telebot
import os
from  os import environ
from flask import Flask, request

owm = pyowm.OWM(config.token_owm)
bot = telebot.TeleBot(config.token_bot)
APP_URL = f'https://ds-9testbot.herokuapp.com//{config.token_bot}'
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, 'Привет, ' + str(message.from_user.first_name) + ', я "недобот", пытающийся дать прогноз погоды \n/help - команды бота')

@bot.message_handler(commands=['author'])
def author(message):
	bot.send_message(message.chat.id, 'Каюков Д.В. ds-9\n/help - команды бота\nДля получения прогноза напишите в чат название города')


@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, '/start - начальное меню\n/help - команды бота\n/author\nЧтобы узнать погоду напишите в чат название города')

@bot.message_handler(content_types=['text'])
def test(message):
	try:
		place = message.text

		config_dict = get_default_config()
		config_dict['language'] = 'ru'


		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather

		t = w.temperature("celsius")
		t1 = t['temp']
		t2 = t['feels_like']
		t3 = t['temp_max']
		t4 = t['temp_min']

		wi = w.wind()['speed']
		humi = w.humidity
		cl = w.clouds
		st = w.status
		dt = w.detailed_status
		ti = w.reference_time('iso')
		pr = w.pressure['press']
		vd = w.visibility_distance

		bot.send_message(message.chat.id, "В городе " + str(place) + " температура " + str(t1) + " °C" + "\n" +
				"Максимальная температура " + str(t3) + " °C" +"\n" +
				"Минимальная температура " + str(t4) + " °C" + "\n" +
				'Ощущается как ' + str(t2) + " °C" + "\n" +
				"Скорость ветра " + str(wi) + " м/с" + "\n" +
				"Давление " + str(pr) + " мм.рт.ст" + "\n" +
				"Влажность " + str(humi) + " %" + "\n" +
				"Видимость " + str(vd) + "  метров" + "\n" +
				"Описание "  + str(dt))

	except:

		bot.send_photo(message.chat.id, 'https://disk.yandex.ru/i/gXH9SlA1I_Q7tA')

@server_route('/' + config.token_bot, methods = ['POST'])
def get_message():
	json_string = request.get_data().decode('utf-8')
	update = telebot.types.Update.de_json(json_string)

@server_route('/')
def webhook():
	bot.remote_webhook()
	bot.set_webhook(url=APP_URL)
	return '!',200

#if __name__='__main__':
#	server.run(host=!'0.0.0.0', port - int(os.environ.get('PORT', 5000)))

bot.polling(none_stop=True, interval=0)

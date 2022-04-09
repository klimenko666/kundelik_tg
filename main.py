import selenium, validators, telebot, os
from telebot import types
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

token = 'bot_token'
bot = telebot.TeleBot(token)
lp = []


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Скриншот kundelik.kz\n\nЧтобы начать напишите /register\nПри не правильном вводе ваших данных - скриншот будет пустым")



@bot.message_handler(commands=['register'])
def log(message):
	bot.send_message(message.chat.id, "Введите логин: ")
	bot.register_next_step_handler(message, pas)

def pas(message):
	lp.append(message.text)
	bot.send_message(message.chat.id, "Введите пароль: ")
	bot.register_next_step_handler(message, logpas)

def chromee(message):
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")
	options.add_experimental_option("excludeSwitches", ["enable-logging"])
	options.add_experimental_option("excludeSwitches", ['enable-automation'])
	service = Service(executable_path=ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=options)
	try:
		uid = message.chat.id
		driver.get("https://login.kundelik.kz/login")
		login = driver.find_element(By.NAME, 'login')
		login.send_keys(lp[0]) #LOGIN
		password = driver.find_element(By.NAME, 'password')
		password.send_keys(lp[1]) #PASSWORD
		sumbit = driver.find_element(By.CLASS_NAME, 'login__submit')
		sumbit.click()
		bot.send_message(message.chat.id, "Выполняется вход...")
		sleep(3)
		photo_path = str(uid) + '.png'
		driver.set_window_size(1280, 720)
		driver.get("https://kundelik.kz/user/user.aspx")
		driver.save_screenshot(photo_path)
		bot.send_photo(uid, photo = open(photo_path, 'rb'), caption="t.me/aziz_klimenko666")
		driver.quit()
		lp.clear()
		os.remove(photo_path)
	except Exception as err:
		print(err)
		lp.clear()
		sleep(30)
		driver.quit()

def logpas(message):
	lp.append(message.text)
	print(lp)
	sleep(5)
	chromee(message)

if __name__ == '__main__':
	print("STARTED")
	bot.infinity_polling()
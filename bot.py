#########################################################
from config import bot
import config
from time import sleep
import re
from telebot import types
#########################################################
# Aquí vendrá la implementación de la lógica del bot  
#Comando: /start
@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.send_message(
        message.chat.id,
        "Hola, soy un \U0001F916, ¿cómo *estás*? \U0001F61C",
        parse_mode="Markdown")

#Ayuda
@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*sumar {valor1} y {valor2}* - Calcula la suma de dos valores\n"
        #"*restar {valor1} y {valor2}* - Calcula la resta de dos valores\n"
        #"*multiplicar {valor1} y {valor2}* - Calcula la multiplicación de dos valores\n"
        "*dividir {valor1} y {valor2}* - Calcula la división de dos valores\n"
        )
    bot.send_message(
        message.chat.id,
        response,
        parse_mode="Markdown")    

#Menu
@bot.message_handler(commands=['menu'])
def on_command_menu(message):
    # Using the ReplyKeyboardMarkup class
    # It's constructor can take the following optional arguments:
    # - resize_keyboard: True/False (default False)
    # - one_time_keyboard: True/False (default False)
    # - selective: True/False (default False)
    # - row_width: integer (default 3)
    # row_width is used in combination with the add() function.
    # It defines how many buttons are fit on each row before continuing on the next row.
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/imc')
    itembtn2 = types.KeyboardButton('/help')
    
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Selecciona una opción del menú:",
        reply_markup=markup)      

#IMC (Indice Masa Muscular)
@bot.message_handler(commands=['imc'])
def on_command_imc(message):
    response = bot.reply_to(message, "¿Cuál es tu estatura en metros?")
    bot.register_next_step_handler(response, process_height_step)

#Recibe el valor de on_command_imc (estatura)
def process_height_step(message):
    try:
        height = float(message.text) #estatura

        record = Record()
        record.height = height

        bot_data[message.chat.id] = record

        response = bot.reply_to(message, '¿Cuál es tu peso en kilogramos?')

        bot.register_next_step_handler(response, process_weight_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

#recibe el valor de  process_height_step (peso)    
def process_weight_step(message):
    try:
        weight = float(message.text)

        record = bot_data[message.chat.id]
        record.weight = weight

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        markup.add('Male', 'Female')
        response = bot.reply_to(message, '¿Cuál es tu género?',
            reply_markup=markup)

        bot.register_next_step_handler(response, process_gender_step)        
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")   

#recibe el valor de  process_gender_step (genero)      
def process_gender_step(message):
    gender = message.text

    record = bot_data[message.chat.id]
    record.gender = gender
    
    imc(message)     

#Implementamos la funcion IMC
def imc(message):
    record = bot_data[message.chat.id]

    imc = record.weight / pow(record.height, 2)

    clasificacion = "";
    if imc<18:
        clasificacion = "Peso bajo";
    elif imc>18 or imc<25:
        clasificacion = "Normal";
    elif imc>=25 or imc<30:
        clasificacion = "Sobrepeso";           
    elif imc>=30:
        clasificacion = "Obesidad";
    
    answer = f"Data = (Height: {record.height}, Weight: {record.weight}, Gender:{record.gender})\nIMC = {imc}, clasificacion: {clasificacion}"
    
   



    bot.reply_to(message, answer)

#########################################################
# Persistencia a Datos
bot_data = {}

class Record:
    def __init__(self):
        self.height = None
        self.weight = None
        self.gender = None   

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")      
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()  

#########################################################

#Default
@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.reply_to(
        message,
        "\U0001F63F Ups, no entendí lo que me dijiste.")        

######################################################### 
#Hace el llamado a Telegram c/20 segundos para ver si hay mensajes
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################
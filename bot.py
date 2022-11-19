#########################################################
from config import bot
import config
from time import sleep
import re
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
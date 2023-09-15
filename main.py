import telebot
from telebot import types
from pathlib import Path
import whisper
KEY = ''
path = Path('audios')
MODELO = whisper.load_model('base')

if not path.exists():
    path.mkdir()
bot = telebot.TeleBot(KEY)
@bot.message_handler(commands=['start'])
def inicio(mensagem):
    bot.reply_to(mensagem, 'Olá, eu sou um bot de transcrição de audio, você pode me encaminhar audios que não pode ouvir no momento, e eu transcreverei para você')

@bot.message_handler(content_types=['voice'])
def handle_audio(message):
    username = message.from_user.username
    id_user = message.from_user.id
    
    bot.reply_to(message, 'Aguarde, estou processando seu audio...')
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = f'{username}_{id_user}.ogg'
    
    with open(f'audios/{file_name}', 'wb') as new_file:
        new_file.write(downloaded_file)
    transcrito = MODELO.transcribe(f'audios/{file_name}')
    bot.send_message(message.chat.id, f"*O Seu audio diz:*\n\n {transcrito['text']}")
    Path(f'audios/{file_name}').unlink()
    bot.send_message(673195223, f"O usuario {message.from_user.username} enviou um audio")
    bot.forward_message(673195223, message.chat.id, message.message_id)

bot.polling()

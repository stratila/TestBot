import requests
import time
import json

bot_url = "https://api.telegram.org/bot488314055:AAGQgobG5aDZ87JcjJEX32QrGaD_AdkgMMs/"

def getUpdates(offset = None):
    pr = {'timeout' : 100, 'offset' : offset }
    conn = requests.get(bot_url+'getUpdates',params = pr)
    return conn.json()
    

def sendMessage(chat_id,text):
    replyKeyboardHide = json.dumps({'hide_keyboard' : True})
    pr = {'chat_id' : chat_id, 'text' : text, 'reply_markup' :replyKeyboardHide}
    requests.get(bot_url+'sendMessage',params = pr)

def sendSticker(chat_id,sticker):
    pr = {'chat_id' : chat_id, 'sticker' : sticker}
    requests.get(bot_url+'sendSticker',params = pr)
 

def last_update(update_json):
    data = update_json['result']
    index = len(data)-1
    return data[index]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def get_message(update):
    mess = update['message']
    return mess

def sendKeyboard(chat_id):
    reply_keyboard =  {'keyboard' : \
                       [ \
                           [{'text': '\U00002669'},{'text' : '\U0000266A'}, {'text': '\U0000266B'},{'text' : '\U0000266C'} ], \
                           [{'text': '\U00002776'},{'text' : '\U00002777'}, {'text': '\U00002778'},{'text' : '\U00002779'} ] \
                       ]}
  
    reply_keyboard_json = json.dumps(reply_keyboard)  #serialization to json string
    pr = {'chat_id' : chat_id, 'text' : 'There is keyboard here!', 'reply_markup' : reply_keyboard_json}
    conn = requests.get(bot_url+'sendMessage',params = pr)
    print(conn.json())
    


if __name__ == '__main__':
    prev_update_id = 0
    offset = int()
    while True:
        if prev_update_id != last_update(getUpdates(offset))['update_id']:
            u = last_update(getUpdates(offset)) 
            offset = prev_update_id = u['update_id']
            chat_id = get_chat_id(u)
            message = get_message(u)
            if message.get('text')!= None:
                if message['text'] == '/keyboard':
                    sendKeyboard(chat_id)
                else:
                    sendMessage(chat_id,'I can say the same: '+message['text'])
            elif message.get('sticker')!= None:
                sticker = message['sticker']['file_id']
                sendSticker(chat_id,sticker)
        time.sleep(1)
                
                
            
    





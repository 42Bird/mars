# tg bot API 5549838211:AAFOBdRyPbbM0OV_-xiSEvFdEyMlugmJJrU

###################################################### Libraries
import telebot
from bs4 import BeautifulSoup
import requests
from telebot import types
import hashlib
import os
import sys
###################################################### Libraries




PAGE_NUMBERS = []
# Создаем экземпляр бота
bot = telebot.TeleBot('6243379302:AAE0bZN3v32-V58wrge8c5ziALrVdX_Ue1c')

MAX_RETIES = 20
PASSWORD = '123'

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message: str, res=False) -> str:
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)         
            bot.send_message(message.chat.id, text="Информационно-поисковая система 'Марс'", reply_markup=markup)            
            bot.send_photo(message.chat.id, photo=open('plakat14.jpg', 'rb'))          
    
            with open('id.txt', 'r') as f:
                    is_id_present = False
                    for line in f:
                        if str(message.from_user.id) in line:
                            is_id_present = True
                            bot.send_message(message.chat.id, text="Ваш ID есть в базе! Добро пожаловать!")
                            bot.send_message(message.chat.id, text="""/surname - Поиск по фамилии 👁
/name - Поиск по фамилии и имени 👥
/number - Поиск по номеру телефона 📱
/address - Поиск по адресу жительства 🏠
/structure - Поиск по подразделению 🛂
/birth - Поиск по дате рождения 🎂
/mail - Поиск по почте 📧
/drfo - Поиск по ДРФО 🏢
/passport - Поиск по паспорту 👤
/photo - Поиск по фото 🔍
/speech - Голосовой поиск 💬""")   
                            bot.send_message(message.chat.id, text="Выберите опцию ⚙️")
                            break
                
                    if not is_id_present:
                        bot.send_message(message.chat.id, text="Введите пароль!")
                
                        @bot.message_handler(content_types=["text"])
                        def password(message: str, res=False) -> str:
                            PASSWORD_MD5 = '7c6a180b36896a0a8c02787eeafb0e4c'
                
                            message.text = bytes(message.text, encoding='utf-8')
                            password_test = hashlib.md5()
                            password_test.update(message.text)
                            password_test = password_test.hexdigest()
                
                            if password_test == PASSWORD_MD5:
                                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                bot.send_message(message.chat.id, text="Добро пожаловать!")
                                id_data = open('id.txt', 'w')
                                id_data.write(str(message.from_user.id))
                                id_data.close()
                                bot.send_message(message.chat.id, text="""/surname - Поиск по фамилии 👁
/name - Поиск по фамилии и имени 👥
/number - Поиск по номеру телефона 📱
/address - Поиск по адресу жительства 🏠
/structure - Поиск по подразделению 🛂
/birth - Поиск по дате рождения 🎂
/mail - Поиск по почте 📧
/drfo - Поиск по ДРФО 🏢
/passport - Поиск по паспорту 👤
/photo - Поиск по фото 🔍
/speech - Голосовой поиск 💬""", reply_markup=markup)
                                bot.send_message(message.chat.id, text="Выберите опцию ⚙️")
                                
                            else:
                                bot.send_message(message.chat.id, text="ДОСТУП ЗАПРЕЩЕН! ⛔️")
    
            
                    
            os.system("pm2 restart main")
                  
                    

        
@bot.message_handler(commands=["surname"])
def surname(message: str, res=False) -> str:
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, text="Введите фамилию. Пример ввода - Захарчук, Измайлов, Луговой", reply_markup=markup)
            
            @bot.message_handler(content_types=["text"])
            def surname(message: str, res=False) -> str:
                
                name = message.text
                
                def nemezida_f(man:str, *args, **kwargs) -> str:        
                
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
                    name = message.text
                               
                    ### nemezida
                            
                    url = f"https://nemez1da.ru/page/1/?s={man}"
                    
                            
                    response = requests.get(url, allow_redirects = True,headers={
                            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                            })
    
    
                   
                    soup = BeautifulSoup(response.text, 'lxml')
                    
                    
                    
                    for page in soup.find_all('a', class_='page-numbers'):                    
                            PAGE_NUMBERS.append(page.text)
                            
                    
                    if man == b'password1':
                         return     
                    
                    for i in range (1,  40):           
                        url = f"https://nemez1da.ru/page/{i}/?s={man}"
                        print(url)
                        
                        response = requests.get(url, allow_redirects = True,headers={
                                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                })
                        
                        WORDS = man.split()
                        
                        NUM_WORDS = len(WORDS)
                        
                        if NUM_WORDS == 1:
    
                            soup = BeautifulSoup(response.text, 'lxml')
                                    
                            links = []
        
                            for link in soup.find_all('a', class_='simple-grid-grid-post-thumbnail-link'):
                                                    links.append(link.get('href'))
                            if not links:
                                                    bot.send_message(message.chat.id, text="Больше не найдено! Базы дополняются и обновляются", reply_markup=markup)    
                                                    break
        
                            import random
                            ID = random.randint(100000000,500000000)
        
                                            
                            for link in links:
                                                    response = requests.get(link, allow_redirects = True, headers={
                                            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                            })
        
                                                    soup = BeautifulSoup(response.text, 'lxml')
                                                    
                                                    name_tag = soup.find('h1')
                                                    name = name_tag.text
                                                    if (WORDS[0] in str(name)):
                                                    
        
                                                        category_tag = soup.find(rel = 'category tag')
                                                     
                                                        
                                                        info_tag = soup.find('div', class_ = 'entry-content simple-grid-clearfix')
            
                                                        
                                                        ### html
            
                                                        
                                                        #f = open(f'{name} {category_tag.text}.html', 'w',  encoding="utf-8")
                                                        
                                                        f = open(f'Отчет_{ID}.html', 'a+',  encoding="utf-8")
                                                        css_code = """
                                                        
                                                                                        
                                                                                         
                                                                    <html>
                                                                    <head>
                                                                      <meta charset="UTF-8">
                                                                      <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                                                      <title>{man}</title>
                                                                      <style>
                                                                        * {
                                                                          margin: 0;
                                                                          padding: 0;
                                                                          box-sizing: border-box;
                                                                          font-family: Arial, sans-serif;
                                                                        }
                                                                        body {
                                                                          background-color: #f1f1f1;
                                                                        }
                                                                        .container {
                                                                          max-width: 800px;
                                                                          margin: 0 auto;
                                                                          background-color: #fff;
                                                                          border-radius: 10px;
                                                                          padding: 20px;
                                                                          box-shadow: 0px 0px 20px rgba(0,0,0,0.2); 
                                                                        }
                                                                        h1 {
                                                                          text-align: center;
                                                                          color: #673ab7;
                                                                          margin-bottom: 20px;
                                                                        }
                                                                        .source {
                                                                          background-color: #673ab7;
                                                                          color: #fff;
                                                                          padding: 10px;
                                                                          border-radius: 5px;
                                                                          margin-bottom: 10px;
                                                                          text-align: center;
                                                                        }
                                                                        .row {
                                                                          display: flex;
                                                                          justify-content: space-between;
                                                                          margin-bottom: 10px;
                                                                        }
                                                                        .row-title {
                                                                          flex-basis: 50%;
                                                                          font-weight: bold;
                                                                        }
                                                                        .row-result {
                                                                          flex-basis: 50%;
                                                                        }
                                                                        p {
                                                                          margin-bottom: 10px;
                                                                        }
                                                                        .info {
                                                                          background-color: #f7f7f7;
                                                                          border-radius: 5px;
                                                                          padding: 10px;
                                                                          margin-bottom: 20px;
                                                                          line-height: 1.5;
                                                                        }
                                                                        
                                                        
                                                        
                                                        """
                                                        html_template_new = css_code + f"""
                                                                                                            </style>
    </head>
    <body>
      <div class="container">
        <h1>{man}</h1>
        <div class="source"><p>ИНФОРМАЦИЯ О ЗАПРОСЕ</p></div>
        <div class="row">
          <div class="row-title">НАЙДЕНО: </div>
          <div class="row-result">{name} {category_tag.text}</div>
        </div>
        <div class="row">
          <div class="row-title"><p>Google Dorks (ChatGPT): </p></div>
          <div class="row-result">https://www.google.com/search?q='{name}%20intext:'ВСУ'</div>
        </div>
        <div class="row">
          <div class="row-title"><p>Фото: </p></div>
          <div class="row-result"><img src="img.jpg"></div>
        </div>
        <div class="source"><p>Данные:</p></div>
        <div class="info">{info_tag.text}</div>
      </div>
    </body>
    </html>
                                                                                        """
                                                        f.write(html_template_new)
                                                        f.close()
                                                        #bot.send_document(message.chat.id, document = open(f'{name} {category_tag.text}.html','rb'))
                                                        
            
                                                        ### html
                                                        
                                                        # Загружаем картинки
                                                        pictures = []
            
                                                        try:
                                                                img = soup.find("div", {"class": "photos_single_place"}).find("img")
                                                                print(img["data-src"])
                                                                pictures.append(img["data-src"])
                                                        except:
                                                                pass
                                                        
                                                        try:
                                                                p = requests.get(pictures[0], allow_redirects = True,headers={
                                                                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                                                })
                                                                out = open("img.jpg", "wb")
                                                                out.write(p.content)
                                                                bot.send_photo(message.chat.id, photo=open('img.jpg', 'rb'))
                                                               
                                                                        
                                                                out.close()
                                                        except:
                                                                pass
            
                                                        try:
                                                                p = requests.get(pictures[1], allow_redirects = True,headers={
                                                                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                                                })
                                                                out = open("img.jpg", "wb")
                                                                out.write(p.content)
                                                                bot.send_photo(message.chat.id, photo=open('img.jpg', 'rb'))
                                                                        
                                                                out.close()
                                                        except:
                                                                pass
                                                    else:
                                                        break
                        
                        else:
                            bot.send_message(message.chat.id, text="Введите только фамилию!", reply_markup=markup)
                            return
                        try:
                            bot.send_document(message.chat.id, document = open(f'Отчет_{ID}.html','rb'))
                        except:
                            bot.send_message(message.chat.id, text="Больше не найдено! Базы дополняются и обновляются", reply_markup=markup)
                            
                nemezida_f(name)  
                bot.send_message(message.chat.id, text="Нажмите /restart для обновления данных")
            os.system("pm2 restart main")
                           
                                        
                
                
                
@bot.message_handler(commands=["name"])
def name(message: str, res=False) -> str:
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, text="Введите имя и фамилию. Пример ввода - Алексей Захарчук, Сергей Измайлов, Борис Луговой", reply_markup=markup)
            @bot.message_handler(content_types=["text"])
            def name(message: str, res=False) -> str:
                
                name = message.text
                
                def nemezida_name(man:str, *args, **kwargs) -> str:        
                
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
                    name = message.text
                               
                    ### nemezida
                            
                    url = f"https://nemez1da.ru/page/1/?s={man}"
                    
                            
                    response = requests.get(url, allow_redirects = True,headers={
                            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                            })
    
    
                   
                    soup = BeautifulSoup(response.text, 'lxml')
                    
                    
                    
                    for page in soup.find_all('a', class_='page-numbers'):                    
                            PAGE_NUMBERS.append(page.text)
                     
                    import random
                    ID = random.randint(10000000,500000000)
                    
                    if man == b'password1':
                         return     
                    
                    for i in range (1,  40):           
                        url = f"https://nemez1da.ru/page/{i}/?s={man}"
                        print(url)
                        
                        response = requests.get(url, allow_redirects = True,headers={
                                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                })
                        
                        WORDS = man.split()
                        NUM_WORDS = len(WORDS)
                        
                        if NUM_WORDS == 2:
    
                            soup = BeautifulSoup(response.text, 'lxml')
                                    
                            links = []
        
                            for link in soup.find_all('a', class_='simple-grid-grid-post-thumbnail-link'):
                                                    links.append(link.get('href'))
                            if not links:
                                                   bot.send_message(message.chat.id, text="Больше не найдено! Базы дополняются и обновляются", reply_markup=markup)    
                                                   break    
        
                            
        
                                            
                            for link in links:
                                                    response = requests.get(link, allow_redirects = True, headers={
                                            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                            })
        
                                                    soup = BeautifulSoup(response.text, 'lxml')
                                                    
                                                    
                                                    name_tag = soup.find('h1')
                                                    name = name_tag.text
                                                    if (WORDS[0] in str(name) and WORDS[1] in str(name)):
        
                                                        category_tag = soup.find(rel = 'category tag')
                                                     
                                                        
                                                        info_tag = soup.find('div', class_ = 'entry-content simple-grid-clearfix')
            
                                                        
                                                        ### html
            
            
                                                        f = open(f'Отчет_{ID}.html', 'a+',  encoding="utf-8")
                                                        css_code = """
                                                        
                                                                                        
                                                                                         
                                                                    <html>
                                                                    <head>
                                                                      <meta charset="UTF-8">
                                                                      <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                                                      <title>{man}</title>
                                                                      <style>
                                                                        * {
                                                                          margin: 0;
                                                                          padding: 0;
                                                                          box-sizing: border-box;
                                                                          font-family: Arial, sans-serif;
                                                                        }
                                                                        body {
                                                                          background-color: #f1f1f1;
                                                                        }
                                                                        .container {
                                                                          max-width: 800px;
                                                                          margin: 0 auto;
                                                                          background-color: #fff;
                                                                          border-radius: 10px;
                                                                          padding: 20px;
                                                                          box-shadow: 0px 0px 20px rgba(0,0,0,0.2); 
                                                                        }
                                                                        h1 {
                                                                          text-align: center;
                                                                          color: #673ab7;
                                                                          margin-bottom: 20px;
                                                                        }
                                                                        .source {
                                                                          background-color: #673ab7;
                                                                          color: #fff;
                                                                          padding: 10px;
                                                                          border-radius: 5px;
                                                                          margin-bottom: 10px;
                                                                          text-align: center;
                                                                        }
                                                                        .row {
                                                                          display: flex;
                                                                          justify-content: space-between;
                                                                          margin-bottom: 10px;
                                                                        }
                                                                        .row-title {
                                                                          flex-basis: 50%;
                                                                          font-weight: bold;
                                                                        }
                                                                        .row-result {
                                                                          flex-basis: 50%;
                                                                        }
                                                                        p {
                                                                          margin-bottom: 10px;
                                                                        }
                                                                        .info {
                                                                          background-color: #f7f7f7;
                                                                          border-radius: 5px;
                                                                          padding: 10px;
                                                                          margin-bottom: 20px;
                                                                          line-height: 1.5;
                                                                        }
                                                                        
                                                        
                                                        
                                                        """
                                                        html_template_new = css_code + f"""
                                                                                                            </style>
    </head>
    <body>
      <div class="container">
        <h1>{man}</h1>
        <div class="source"><p>ИНФОРМАЦИЯ О ЗАПРОСЕ</p></div>
        <div class="row">
          <div class="row-title">НАЙДЕНО: </div>
          <div class="row-result">{name} {category_tag.text}</div>
        </div>
        <div class="row">
          <div class="row-title"><p>Google Dorks (ChatGPT): </p></div>
          <div class="row-result">https://www.google.com/search?q='{name}%20intext:'ВСУ'</div>
        </div>
        <div class="row">
          <div class="row-title"><p>Фото: </p></div>
          <div class="row-result"><img src="img.jpg"></div>
        </div>
        <div class="source"><p>Данные:</p></div>
        <div class="info">{info_tag.text}</div>
      </div>
    </body>
    </html>
                                                                                        """
                                                        
                                                        f.write(html_template_new)
                                                        f.close()
                                                        bot.send_document(message.chat.id, document = open(f'Отчет_{ID}.html','rb'))
            
            
                                                        ### html
                                                        
                                                        # Загружаем картинки
                                                        pictures = []
            
                                                        try:
                                                                img = soup.find("div", {"class": "photos_single_place"}).find("img")
                                                                print(img["data-src"])
                                                                pictures.append(img["data-src"])
                                                        except:
                                                                pass
                                                        
                                                        try:
                                                                p = requests.get(pictures[0], allow_redirects = True,headers={
                                                                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                                                })
                                                                out = open("img.jpg", "wb")
                                                                out.write(p.content)
                                                                bot.send_photo(message.chat.id, photo=open('img.jpg', 'rb'))
                                                               
                                                                        
                                                                out.close()
                                                        except:
                                                                pass
            
                                                        try:
                                                                p = requests.get(pictures[1], allow_redirects = True,headers={
                                                                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                                                })
                                                                out = open("img.jpg", "wb")
                                                                out.write(p.content)
                                                                bot.send_photo(message.chat.id, photo=open('img.jpg', 'rb'))
                                                                        
                                                                out.close()
                                                        except:
                                                                pass
                        else:
                            bot.send_message(message.chat.id, text="Введите только имя и фамилию!", reply_markup=markup)
                            return         
                nemezida_name(name)
                bot.send_message(message.chat.id, text="Нажмите /restart для обновления данных")
            os.system("pm2 restart main")
                                                                               
        
        
@bot.message_handler(commands=["number"])
def number(message: str, res=False) -> str:
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, text="Введите номер телефона. Пример ввода - 380962391128, 79256789456", reply_markup=markup)
            @bot.message_handler(content_types=["text"])
            def number(message: str, res=False) -> str:
                
                name = message.text
                
                def nemezida_number(man:str, *args, **kwargs) -> str:        
                
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
                    name = message.text
                               
                    ### nemezida
                            
                    url = f"https://nemez1da.ru/page/1/?s={man}"
                    
                            
                    response = requests.get(url, allow_redirects = True,headers={
                            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                            })
    
    
                   
                    soup = BeautifulSoup(response.text, 'lxml')
                    
                    
                    
                    for page in soup.find_all('a', class_='page-numbers'):                    
                            PAGE_NUMBERS.append(page.text)
                            
                    
                    if man == b'password1':
                         return     
                    import random
                    ID = random.randint(10000000,5000000000)
                    for i in range (1,  40):           
                        url = f"https://nemez1da.ru/page/{i}/?s={man}"
                        print(url)
                        
                        response = requests.get(url, allow_redirects = True,headers={
                                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                })
                        
                        WORDS = man.split()
                        NUM_WORDS = len(WORDS)
                        
                        if (NUM_WORDS == 1 and man.isnumeric() == True):
    
                            soup = BeautifulSoup(response.text, 'lxml')
                                    
                            links = []
        
                            for link in soup.find_all('a', class_='simple-grid-grid-post-thumbnail-link'):
                                                    links.append(link.get('href'))
                            if not links:
                                                 bot.send_message(message.chat.id, text="Больше не найдено! Базы дополняются и обновляются", reply_markup=markup)    
                                                 break  
        
                            
        
                                            
                            for link in links:
                                                    response = requests.get(link, allow_redirects = True, headers={
                                            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                            })
        
                                                    soup = BeautifulSoup(response.text, 'lxml')
                                                    
                                                    
                                                    name_tag = soup.find('h1')
                                                    name = name_tag.text
                                                    
        
                                                    category_tag = soup.find(rel = 'category tag')
                                                     
                                                        
                                                    info_tag = soup.find('div', class_ = 'entry-content simple-grid-clearfix')
                                                    
                                                        
                                                        ### html
            
            
                                                  
                                                    f = open(f'Отчет_{ID}.html', 'a+',  encoding="utf-8")
                                                    css_code = """
                                                        
                                                                                        
                                                                                         
                                                                    <html>
                                                                    <head>
                                                                      <meta charset="UTF-8">
                                                                      <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                                                      <title>{man}</title>
                                                                      <style>
                                                                        * {
                                                                          margin: 0;
                                                                          padding: 0;
                                                                          box-sizing: border-box;
                                                                          font-family: Arial, sans-serif;
                                                                        }
                                                                        body {
                                                                          background-color: #f1f1f1;
                                                                        }
                                                                        .container {
                                                                          max-width: 800px;
                                                                          margin: 0 auto;
                                                                          background-color: #fff;
                                                                          border-radius: 10px;
                                                                          padding: 20px;
                                                                          box-shadow: 0px 0px 20px rgba(0,0,0,0.2); 
                                                                        }
                                                                        h1 {
                                                                          text-align: center;
                                                                          color: #673ab7;
                                                                          margin-bottom: 20px;
                                                                        }
                                                                        .source {
                                                                          background-color: #673ab7;
                                                                          color: #fff;
                                                                          padding: 10px;
                                                                          border-radius: 5px;
                                                                          margin-bottom: 10px;
                                                                          text-align: center;
                                                                        }
                                                                        .row {
                                                                          display: flex;
                                                                          justify-content: space-between;
                                                                          margin-bottom: 10px;
                                                                        }
                                                                        .row-title {
                                                                          flex-basis: 50%;
                                                                          font-weight: bold;
                                                                        }
                                                                        .row-result {
                                                                          flex-basis: 50%;
                                                                        }
                                                                        p {
                                                                          margin-bottom: 10px;
                                                                        }
                                                                        .info {
                                                                          background-color: #f7f7f7;
                                                                          border-radius: 5px;
                                                                          padding: 10px;
                                                                          margin-bottom: 20px;
                                                                          line-height: 1.5;
                                                                        }
                                                                        
                                                        
                                                        
                                                        """
                                                    html_template_new = css_code + f"""
                                                                                                            </style>
    </head>
    <body>
      <div class="container">
        <h1>{man}</h1>
        <div class="source"><p>ИНФОРМАЦИЯ О ЗАПРОСЕ</p></div>
        <div class="row">
          <div class="row-title">НАЙДЕНО: </div>
          <div class="row-result">{name} {category_tag.text}</div>
        </div>
        <div class="row">
          <div class="row-title"><p>Google Dorks (ChatGPT): </p></div>
          <div class="row-result">https://www.google.com/search?q='{name}%20intext:'ВСУ'</div>
        </div>
        <div class="row">
          <div class="row-title"><p>Фото: </p></div>
          <div class="row-result"><img src="img.jpg"></div>
        </div>
        <div class="source"><p>Данные:</p></div>
        <div class="info">{info_tag.text}</div>
      </div>
    </body>
    </html>
                                                                                        """
                                               
                                                    f.write(html_template_new)
                                                    f.close()
                                                    bot.send_document(message.chat.id, document = open(f'Отчет_{ID}.html','rb'))
                
                
                                                            ### html
                                                            
                                                            # Загружаем картинки
                                                    pictures = []
                
                                                    try:
                                                                    img = soup.find("div", {"class": "photos_single_place"}).find("img")
                                                                    print(img["data-src"])
                                                                    pictures.append(img["data-src"])
                                                    except:
                                                                    pass
                                                            
                                                    try:
                                                                    p = requests.get(pictures[0], allow_redirects = True,headers={
                                                                    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                                                    })
                                                                    out = open("img.jpg", "wb")
                                                                    out.write(p.content)
                                                                    bot.send_photo(message.chat.id, photo=open('img.jpg', 'rb'))
                                                                   
                                                                            
                                                                    out.close()
                                                    except:
                                                                    pass
                
                                                    try:
                                                                    p = requests.get(pictures[1], allow_redirects = True,headers={
                                                                    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
                                                                    })
                                                                    out = open("img.jpg", "wb")
                                                                    out.write(p.content)
                                                                    bot.send_photo(message.chat.id, photo=open('img.jpg', 'rb'))
                                                                            
                                                                    out.close()
                                                    except:
                                                                    pass
                                                                
                        else:
                            bot.send_message(message.chat.id, text="Введите номер телефона!", reply_markup=markup)
                            return         
                nemezida_number(name)   
                bot.send_message(message.chat.id, text="Нажмите /restart для обновления данных")
            os.system("pm2 restart main")
           
            

@bot.message_handler(commands=['restart'])
def restart(message):
    bot.send_message(message.chat.id, text="Обновление данных...")
    # Перезапуск бота
    os.system("pm2 restart main")

                
# Запускаем бота
bot.polling(none_stop=True, interval=0)

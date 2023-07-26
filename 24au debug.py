# -*- coding: utf-8 -*-
from grab import Grab
import random
from Tkinter import *
import time
import datetime
import pickle
import os


g = Grab()
g.setup(headers={'Accept-Encoding': 'gzip, deflate',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
	'Keep-Alive': ''
})

def auth(logpass):
	try:
		g.go('http://krsk.24au.ru/')
		uname = logpass[0]
		g.set_input_by_id('UserName', uname)
		pwd =  logpass[1] + '              '
		g.set_input_by_id('Password', pwd)
		g.submit()
		console_menu_announcer(u'Авторизован аккаунт ' + g.xpath('//*[@id="stickytopbar"]/div[1]/div/div/div[1]/div/div[4]/div[3]/div[1]/div/a[1]').text)
	except:
		report = u'Ошибка авторизации'		
		try:
			console_menu_announcer(report + u' (уже авторизован как ' + g.xpath('//*[@id="stickytopbar"]/div[1]/div/div/div[1]/div/div[4]/div[3]/div[1]/div/a[1]').text + u', нажмите "Выход")')
		except:
			console_menu_announcer(report)

def auth_master():
	console_menu_announcer('Выполняется авторизация...')
	root.update()
	logpass = ['', '']
	logpass[0] = Entry_login.get()
	logpass[1] = Entry_passw.get()
	auth(logpass)
	remember_exec()



def auth_closer():
	check1.deselect()
	Entry_login.delete("0", "end")
	Entry_passw.delete("0", "end")
	root.update()
	try:
		check = g.xpath('//*[@id="stickytopbar"]/div[1]/div/div/div[1]/div/div[4]/div[3]/div[1]/div/a[1]').text
		logged = True
	except:
		logged = False
	config_file = open('config.pkl', 'wb')
	config_variable = {}
	config_variable['login'] = ''
	config_variable['password'] = ''
	pickle.dump(config_variable, config_file)		
	config_file.close()
	g.go('http://krsk.24au.ru/')
	g.clear_cookies()
	g.go('http://common.24au.ru/logout/?returnUrl=http://krsk.24au.ru/')
	if logged == True:		
		console_menu_announcer('Авторизация отменена, работа со списком невозможна')
	else:
		console_menu_announcer('Не авторизован')


def remember_exec():
	config_file = open('config.pkl', 'wb')
	config_variable = {}
	if remember.get() == 1:
		try:
			config_variable['login'] = Entry_login.get()
			config_variable['password'] = Entry_passw.get()
		except:
			pass
	else:
		try:
			config_variable['login'] = ''
			config_variable['password'] = ''
		except:
			pass
	pickle.dump(config_variable, config_file)		
	config_file.close()

	

def auth_giver():
	try:
		config_file = open('config.pkl', 'rb')
		config_variable = pickle.load(config_file)
		login = config_variable['login']
		password = config_variable['password']
		Entry_login.insert(1,login)
		Entry_passw.insert(1,password)
		if len(login) > 1:
			check1.select()
			auth_master()
		else:
			check1.deselect()
	except:
		pass

def pages_counter(request_page):
	page = 1
	quantity = 0
	g.go(request_page)
	while page < 200:
		try:
			postfix = '?page='
			if page == 1:
				postfix = ''
			else :
				postfix += str(page)
			curent_page = request_page + postfix
			g.go(curent_page)
			attr = g.xpath('//tr[contains(@class, "lot")][1]/@id')
			quantity += 1
			page += 1						
		except:
			page += 1
			break
	return quantity

def scraper(current_page):
	global lot_id_scrap
	counter = 1
	g.go(current_page)
	while counter < 32:
		try:
			attr = g.xpath('//tr[contains(@class, "lot")][' + str(counter) + ']/@id')
			lot_id_scrap.append(int(attr))
			counter += 1
		except:
			break		
		

def scraper_paginator(category):
	console_announcer('Выполняется поиск лотов...')
	root.update()
	global lot_id_scrap
	lot_id_scrap = []
	page = 1
	pages = pages_counter(category)
	while page <= pages:
		postfix = '?page='
		if page == 1:
			postfix = ''
		else :
			postfix += str(page)
		curent_page = category + postfix
		scraper(curent_page)
		page += 1
	page_type = ''
	if category.endswith('/none/'):
		page_type = ' "Все лоты" : '
	elif category.endswith('/active/'):
		page_type = ' "Активные лоты" : '
	else:
		page_type = ' "Завершенные лоты" : '
	console_announcer('Обнаружено лотов в категории' + page_type + str(len(lot_id_scrap)))
	list_announcer(lot_id_scrap)

def all_paginator():
	scraper_paginator('http://24au.ru/user/me/lots/none/')
def active_paginator():
	scraper_paginator('http://24au.ru/user/me/lots/active/')
def closed_paginator():
	scraper_paginator('http://24au.ru/user/me/lots/closed/')






def list_saver():
	global lot_id_scrap
	if len(lot_id_scrap) > 0:
		try:
			list_file = open('list.pkl', 'wb')
			list_variable = []
			list_variable = lot_id_scrap[ : ]
			console_announcer('Текущий список сохранен в файл списка list.pkl')
			pickle.dump(list_variable, list_file)
			list_file.close()
		except:
			console_announcer('Нет доступа к файлу списка list.pkl')
	else:
		console_announcer('Задан пустой список')


def list_opener():
	global lot_id_scrap
	try:
		list_file = open('list.pkl', 'rb')
		list_variable = pickle.load(list_file)
		lot_id_scrap = list_variable
		console_announcer('Текущий список заменен списком из файла list.pkl')
		list_announcer(lot_id_scrap)
		list_file.close()
	except:
		console_announcer('Нет доступа к файлу списка list.pkl')
		list_announcer(lot_id_scrap)		

def list_adder():
	global lot_id_scrap
	try:
		scrap = Entry_adder.get()
		lot_id_scrap.append(int(scrap))
		console_announcer('Лот добавлен в список')
		list_announcer(lot_id_scrap)
	except:
		console_announcer('Ошибка добавления лота в список, введите числовой ID лота')
	Entry_adder.delete("0", "end")

def list_subtracter():
	global lot_id_scrap
	try:
		scrap = Entry_subtracter.get()
		lot_id_scrap.remove(int(scrap))
		console_announcer('Лот удален из списка')
		list_announcer(lot_id_scrap)
	except:
		console_announcer('Ошибка удаления лота из списка, введите числовой ID лота из списка')
	Entry_subtracter.delete("0", "end")

def withdraw_lot(lot_id):
	global lot_id_scrap_passed
	remark = random.randint(1,10000)
	g.setup(post={'deleteRemark': remark})
	g.go('http://krsk.24au.ru/' + str(lot_id) + '/Close/')
	try:
		tester = g.xpath('//title').text
		if tester  == '500':
			lot_id_scrap_passed.append(lot_id)
		else:
			pass
	except:
		pass

def withdraw_list():
	global lot_id_scrap_passed
	tries = 3
	console_announcer('Выполняется снятие лотов...')	
	root.update()
	for id in lot_id_scrap:
		withdraw_lot(id)
	if len(lot_id_scrap_passed)	> 0:
		console_announcer('Повторный проход...')
		root.update()
		random.shuffle(lot_id_scrap_passed)
		passed = lot_id_scrap_passed[ : ]
		while tries > 0:
			for id in passed:
				withdraw_lot(id)
				tries -= 1
		console_announcer('Лоты из списка сняты с торгов')			
	else:
		console_announcer('Лоты из списка сняты с торгов')
	lot_id_scrap_passed = []
              
def publish_lot(lot_id):
	g.go('http://24au.ru/user/me/lots/off/')
	g.go('http://24au.ru/action.ashx?action=repeat_selected_lots&listlot=' + str(lot_id) + ';')

def publish_list():
	console_announcer('Выполняется выставление лотов на торги...')
	root.update()
	for id in lot_id_scrap:
		publish_lot(id)	
	console_announcer('Лоты из списка выставлены на торги')	


def publish_all(category):
	scraper_paginator(category)
	for id in lot_id_scrap:
		publish(id)

def console_announcer(console_text):
	descr12["text"] = console_text

def console_menu_announcer(console_text):
	descr_menu["text"] = console_text

def list_announcer(list_value):
	button_list["text"] = len(list_value)

def list_cleaner():
	global lot_id_scrap
	lot_id_scrap = []
	list_announcer(lot_id_scrap)
	console_announcer('Список очищен')

def list_modal():
    win = Toplevel()
    win.title('Сформированный список')
    win.geometry('800x500')
    win.resizable(True, True)
    win["background"]="#E8E6EC"
    information=Label(win,text='После изменения списка в главном окне переоткройте это. Выделите ID и нажмите CTRL+C для копирования.',width=500,height=1,bg='#000',fg='#f0fe58',font='arial 9 bold')
    information.pack()
    lister=Text(win,wrap=WORD,width=500,height=80,bg='#efedf3',font='tahoma 10 bold',selectbackground='#ffbb04',selectforeground='#333')
    lister.pack()
    root.update()
    win.update()
    formator(lister)


def formator(lister):
	global lot_id_scrap	
	for ids in lot_id_scrap:
		g.go('http://krsk.24au.ru/' + str(ids) + '/')
		try:
			titler = g.xpath('//h1').text + '\n'
			user = u'> ' + g.xpath("//*[@id='card_user_form']/div/div/div[1]/div/a[1]").text + u' <  '
			try:
			 	check = g.xpath("//*[@class='status-info-text']").text
			 	status = u'    Снят с торгов' + u'\n'
			except:
				status = u'    Активен' + u'\n'		 	
		except:
			titler = u'Ошибка получения описания лота. Проверьте корректность ID и состояние интернет соединения.\n'
			user = u''
			status = u'Активен'
		ids_n = str(ids)
		lister.insert(1.0,status)
		lister.insert(1.0,ids_n)
		lister.tag_add(status, "1.11", "1.40")
		lister.tag_config(status,foreground="#8577a0")		
		lister.tag_add(ids_n, "1.0", "1.10")
		lister.tag_config(ids_n,foreground="blue")
		lister.insert(1.0,titler)			
		lister.insert(1.0,user)
		root.update()


def helper():
	win = Toplevel()
	win.title('Поддержка')
	win.geometry('500x500')
	win.resizable(False, False)
	win["background"]="#E8E6EC"
	information=Label(win,text='Алгоритм работы с 24au Helper:\n1. Начало сессии работы посредством авторизации программы\n на аукционе\n2. Создание списка из лотов, имеющихся на вашем профиле аукциона\n3. Ручная (разово) или автоматическая (циклически) обработка списка\n лотов ',width=60,height=6,justify='left',bg='#E8E6EC',fg='#333',font='arial 9 bold')
	information.place(x=0,y=0)
	lister=Entry(win,width=50,bg='#fff',font='tahoma 10 bold',selectbackground='#ffbb04',selectforeground='#333')
	lister.place(x=20,y=200)
	lister.insert(1,'https://www.youtube.com/watch?v=OLUkYEivJL8')

def bot():
	global timer
	global bot_flag
	global ticker_flag
	timer_show.after_cancel(ticker_flag)
	auto_timer()
	bot_flag = descr1.after(timer, bot)
	withdraw_list()
	publish_list()
	console_announcer('Автоматическое перевыставление по времени запущено')

def bot_starter():
	buttons_locker()
	auto_timer()
	descr1.after_idle(bot)
	
def bot_stopper():
	global bot_flag
	global ticker_flag
	buttons_unlocker()
	descr1.after_cancel(bot_flag)
	timer_show.after_cancel(ticker_flag)
	timer_show['text'] = '00:00:00'
	timer_show['fg'] = '#9393a1'
	console_announcer('Автоматическое перевыставление отключено')

def auto_timer():
	global curr_time
	global target_time
	curr_time = int(time.time()*1000)
	cycle_time = float(scale1.get())*360
	cycle_time = int(cycle_time) * 10000
	target_time = curr_time + cycle_time
	timer_show.after_idle(remain_time_ticker)


def remain_time_ticker():
	global ticker_flag
	curr_time = int(time.time()*1000)
	remain_time = target_time - curr_time
	ticker_flag = timer_show.after(500, remain_time_ticker)
	ticker_hours = remain_time / 3600000
	if ticker_hours < 10:
		ftd_hours = '0' + str(ticker_hours)
	else:
		ftd_hours = str(ticker_hours)
	ticker_mins = (remain_time % 3600000) / 60000
	if ticker_mins < 10:
		ftd_mins = '0' + str(ticker_mins)
	else:
		ftd_mins = str(ticker_mins)
	ticker_secs = ((remain_time % 3600000) % 60000) / 1000
	if ticker_secs < 10:
		ftd_secs = '0' + str(ticker_secs)
	else:
		ftd_secs = str(ticker_secs)
	timer_formatted = ftd_hours + ':' + ftd_mins + ':' + ftd_secs
	timer_show['text'] = str(timer_formatted)
	timer_show['fg'] = '#6f6fbc'



curr_time = 0
target_time = 0
lot_id_scrap = []
lot_id_scrap_passed = []
ticker_flag = 0
bot_flag = 0
timer = 0.5

def refresh_choise(get):
	global timer
	timer = float(scale1.get())*360
	timer = int(timer) * 10000
	if float(get) <= 9.5:
		hours = '0' + get[0] + ':'
	else:
		hours = get[0:2] + ':'
	if get[len(get)-1] == '5':
		mins = '30'
	else:
		mins = '00'
	descr16["text"] = hours+mins
	root.update()

def buttons_locker():
	button8['state'] = DISABLED
	buttonin['state'] = DISABLED
	buttonout['state'] = DISABLED
	button1['state'] = DISABLED
	button2['state'] = DISABLED
	button3['state'] = DISABLED
	button4['state'] = DISABLED
	button4_1['state'] = DISABLED
	button5['state'] = DISABLED
	button6['state'] = DISABLED
	button7['state'] = DISABLED
	button11['state'] = DISABLED
	button10_1['state'] = DISABLED

def buttons_unlocker():
	button8['state'] = NORMAL
	buttonin['state'] = NORMAL
	buttonout['state'] = NORMAL
	button1['state'] = NORMAL
	button2['state'] = NORMAL
	button3['state'] = NORMAL
	button4['state'] = NORMAL
	button4_1['state'] = NORMAL
	button5['state'] = NORMAL
	button6['state'] = NORMAL
	button7['state'] = NORMAL
	button11['state'] = NORMAL
	button10_1['state'] = NORMAL

root=Tk()
root.title('24au helper')
root.geometry('650x705')
root.resizable(False, False)
root["background"]="#E8E6EC"
root.iconbitmap('favicon.ico')
remember=IntVar()

descr1=Label(root,text='Авторизация на аукционе',width=75,height=1,bg='#A3A0A8',fg='#333',font='arial 10 bold')
descr1.place(relx=0.5,y=10,anchor='center')
descr2=Label(root,text='Пользователь',height=1,fg='#5d5d66',bg="#E7E8E8",justify='left',font='arial 10 bold')
descr2.place(x=12,y=30)
Entry_login=Entry(root,width=20,font='arial 9 bold',fg='#444')
Entry_login.place(x=141,y=32)
descr3=Label(root,text='Пароль',height=1,fg='#5d5d66',bg="#E7E8E8",justify='left',font='arial 10 bold')
descr3.place(x=12,y=58)
Entry_passw=Entry(root,width=20,show='*',font='arial 9 bold',fg='#444')
Entry_passw.place(x=141,y=62)
buttonin=Button(root,text='Войти',command=auth_master,width=15,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
buttonin.place(x=368,y=32)
buttonout=Button(root,text='Выйти',command=auth_closer,width=15,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
buttonout.place(x=509,y=32)
check1=Checkbutton(root,text='Запомнить',variable=remember,onvalue=1,offvalue=0,font='arial 8 bold',fg='#5d5d66',bg="#E7E8E8",activeforeground='#5d5d66',activebackground='#E7E8E8')
check1.place(x=363,y=63)
check1.deselect()

descr4=Label(root,text='Формирование списка лотов для обработки',width=75,height=1,bg='#A3A0A8',fg='#333',font='arial 10 bold')
descr4.place(relx=0.5,y=129,anchor='center')

frame1=Frame(root,width=280,heigh=200,bg='#D3D0D8')
frame1.place(x=0,y=141)
descr5=Label(frame1,text='Автоматический сбор',height=1,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr5.place(relx=0.5,y=15,anchor='center')
descr6=Label(frame1,text='Создает новый список, \nзаменяя текущий',height=2,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr6.place(x=13,y=170,anchor='w')
button1=Button(frame1,text='Выбрать все лоты',command=all_paginator,width=26,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 9 bold')
button1.place(x=11,y=35)
button2=Button(frame1,text='Выбрать активные лоты',command=active_paginator,width=26,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 9 bold')
button2.place(x=11,y=75)
button3=Button(frame1,text='Выбрать завершенные лоты',command=closed_paginator,width=26,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 9 bold')
button3.place(x=11,y=115)

frame2=Frame(root,width=300,heigh=200,bg='#D3D0D8')
frame2.place(x=350,y=142)
descr7=Label(frame2,text='Пользовательский ввод',width=21,height=1,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr7.place(relx=0.5,y=15,anchor='center')
descr8=Label(frame2,text='Вносит лот в список путем \nдобавления его ID через форму \nID указан в ссылке лота, пример: \nhttp://krsk.24au.ru/',height=5,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr8.place(x=12,y=152,anchor='w')
descr9=Label(frame2,text='1234567   <--- ID',height=1,fg='#6f6fbc',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr9.place(x=145,y=179,anchor='w')
descr10=Label(frame2,text='/',height=1,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr10.place(x=211,y=179,anchor='w')
Entry_adder=Entry(frame2,width=14,font='arial 10 bold',fg='#555',justify='center')
Entry_adder.place(x=16,y=39)
button4=Button(frame2,text='Добавить',command=list_adder,width=12,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
button4.place(x=179,y=50,anchor='w')
Entry_subtracter=Entry(frame2,width=14,font='arial 10 bold',fg='#555',justify='center')
Entry_subtracter.place(x=16,y=77)
button4_1=Button(frame2,text='Исключить',command=list_subtracter,width=12,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
button4_1.place(x=179,y=88,anchor='w')

frame4=Frame(root,width=650,heigh=50,bg='#c1bdc7')
frame4.place(x=0,y=341)
button5=Button(frame4,text='Восстановить список',command=list_opener,width=22,height=1,bg='#727685',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
button5.place(x=11,y=11)
button6=Button(frame4,text='Очистить список',command=list_cleaner,width=22,height=1,bg='#727685',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
button6.place(x=223,y=11)
button7=Button(frame4,text='Сохранить список',command=list_saver,width=22,height=1,bg='#727685',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
button7.place(x=453,y=11)

frame3=Frame(root,width=70,heigh=200,bg='#c1bdc7')
frame3.place(x=280,y=141)
button_list=Button(frame3,command=list_modal,text='0',width=4,height=2,bg='#4C5866',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 15 bold')
button_list.place(relx=0.5,rely=0.5,anchor='center')

cons_top_frame=Frame(root,width=650,heigh=25,bg='#000')
cons_top_frame.place(x=0,y=92)
descr_menu=Label(cons_top_frame,text=' ',height=1,bg='#000',fg='#f0fe58',font='arial 9 bold')
descr_menu.place(x=13,y=0,anchor='nw')

consframe=Frame(root,width=650,heigh=25,bg='#000')
consframe.place(x=0,y=390)
descr12=Label(consframe,text='Авторизуйтесь, сформируйте список, затем переходите к управлению',height=1,bg='#000',fg='#f0fe58',font='arial 9 bold')
descr12.place(x=13,y=0,anchor='nw')

descr13=Label(root,text='Управление лотами из сформированного списка',width=75,height=1,bg='#A3A0A8',fg='#333',font='arial 10 bold')
descr13.place(relx=0.5,y=425,anchor='center')

frame5=Frame(root,width=280,heigh=200,bg='#D3D0D8')
frame5.place(x=0,y=437)
descr14=Label(frame5,text='По времени (час:мин)',height=1,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr14.place(relx=0.5,y=15,anchor='center')
descr15=Label(frame5,text='Перевыставлять каждые:',height=1,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr15.place(x=16,y=25)
descr16=Label(frame5,text='0:0',height=1,fg='#6f6fbc',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr16.place(x=225,y=25)
scale1 = Scale(frame5,troughcolor='#d5d7e0',command=refresh_choise,fg='#444',sliderlength=27,bd=0,bg="#f0f0f0",orient=HORIZONTAL,length=244,from_=0.5,to=24,tickinterval=0.5, resolution=0.5,font='arial 9 bold')
scale1.place(x=16,y=55)
descrx=Label(frame5,text=' ',width=46,height=2,bg='#D3D0D8',fg='#333',font='arial 6 bold')
descrx.place(relx=0.5,y=112,anchor='center')
button8=Button(frame5,text='Запустить',command=bot_starter,width=12,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
button8.place(x=16,y=109)
button9=Button(frame5,text='Отключить',command=bot_stopper,width=12,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 8 bold')
button9.place(x=156,y=109)
descr17=Label(frame5,text='Циклически перевыставляет \nлоты из списка',height=2,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr17.place(x=13,y=170,anchor='w')

frame6=Frame(root,width=250,heigh=200,bg='#D3D0D8')
frame6.place(x=400,y=438)
descr18=Label(frame6,text='Вручную',height=1,fg='#5d5d66',bg="#D3D0D8",justify='left',font='arial 10 bold')
descr18.place(relx=0.5,y=15,anchor='center')
button10_1=Button(frame6,text='Выставить лоты на торги',command=publish_list,width=22,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 9 bold')
button10_1.place(relx=0.5,y=50,anchor='center')
button11=Button(frame6,text='Снять лоты с торгов',command=withdraw_list,width=22,height=1,bg='#5D606E',activeforeground='#222',activebackground='#dce2e7',fg='#fff',font='arial 9 bold')
button11.place(relx=0.5,y=90,anchor='center')

timer_show=Label(root,text='00:00:00',height=2,fg='#9393a1',bg="#E7E8E8",justify='left',font='arial 10 bold')
timer_show.place(x=2300,y=474,anchor='w')

button10=Button(root,text='Помощь',command=helper,width=15,height=2,bg='#a8acbc',activeforeground='#222',activebackground='#dce2e7',fg='#444',font='arial 9 bold')
button10.place(x=499,y=649)

auth_giver()
root.mainloop()

from tkinter import *
from tkinter.filedialog import asksaveasfile
import tkinter.ttk as ttk
from tkinter.font import Font 
import pandas as pd 
from tkcalendar import Calendar, DateEntry
import calendar, datetime 
from time import strftime
import numpy as np
from tkinter import scrolledtext, Scrollbar
import sys
import os
sys.path.append(os.path.dirname(os.getcwd())+'/src/waktu_shalat')
sys.path.append(os.path.dirname(os.getcwd())+'/src/lintang_ekstrem')
from WaktuShalat import WaktuSholat
from LintangEkstrem import LintangEkstrem

class Window:

	def __init__(self, master):
		'''Inisialisasi window'''

		self.master = master
		self.init_window()
		
	def init_window(self):
		'''Mengabungkan semua method dalam satu window'''

		self.master.title("Kalkulator Waktu Sholat")
		self.fontstyle = Font(family='Times New Roman', size=12)
		self.fontstyle2 = Font(family='Times New Roman', size=11)
		self.fontstyle3 = ('Times New Roman', 12, 'bold')
		self.fontstyle4 = ('Times New Roman', 17, 'bold')
		self.menus()
		self.make_frame() 
		self.title()
		self.get_date()
		self.frame_1()
		self.frame_2()
		self.convert_button()
		self.frame_3()
		

	def menus(self):
		'''Membuat menu'''

		menu = Menu(self.master)
		self.master.config(menu=menu)

		file = Menu(menu)
		file.add_command(label='Save As..', command=self.save_file)
		file.add_command(label='Exit', command=self.exit_program)

		view = Menu(menu)
		view.add_command(label='Show Credit', command=self.show_credit)
		view.add_command(label='Hide Credit', command=self.hide_credit)

		helps = Menu(menu)
		helps.add_command(label='About', command=self.about)

		menu.add_cascade(label='File', menu=file)
		menu.add_cascade(label='View', menu=view)
		menu.add_cascade(label='Help', menu=helps)

	def exit_program(self):
		'''Perintah untuk keluar dari program'''

		exit()

	def show_credit(self):
		'''Menampilkan credit pada bagian bawah window'''

		self.lbl_version = Label(self.master, text='Program Kalkulator Waktu Shalat Version 1.5 - ', font=self.fontstyle, fg='black')
		self.lbl_credit = Label(self.master, text='Created by Adh : i_alimurrijal@student.ub.ac.id', font=self.fontstyle, fg='black')
		self.lbl_version.place(x=20, y=620)
		self.lbl_credit.place(x=315, y=620)

	def hide_credit(self):
		'''Menyembuyikan credit pada bagian bawah window setelah dipanggil menggunakn show_credit()'''

		self.lbl_credit.place_forget()
		self.lbl_version.place_forget()

	def make_frame(self):
		'''Membuat widget frame pada jendela window'''

		self.frame1 = Frame(height=210, width=550, bg='#f0f8ff', borderwidth=3, relief=GROOVE)
		self.frame2 = Frame(height=210, width=360, bg='#7eb593', borderwidth=3, relief=GROOVE)
		self.frame3 = Frame(height=390, width=925, bg='#c0d6e4', borderwidth=3, relief=GROOVE)
		self.frame1.place(x=10, y=10)
		self.frame2.place(x=575, y=10)
		self.frame3.place(x=10, y=230)

	def title(self):
		'''Membuat judul program/aplikasi -- diletakkan di bagian atas window'''

		title = Label(self.frame2, text="KALKULATOR WAKTU \nSHALAT", font=self.fontstyle4, fg='darkgreen', bg='#7eb593')
		title.place(x=50, y=5)

	def get_date(self):
		'''Menampilkan kalender'''

		self.kalender = Calendar(self.frame1, font=self.fontstyle2, selectmode='day', cursor='hand1')
		self.kalender.place(x=260, y=0)
		selected_date=None

	def about(self):
		'''Membuat jendela about'''

		about = Toplevel()
		about.title('About')
		about.geometry('300x115')
		about.resizable(0,0)
		icon_photo = PhotoImage(file='cal_logo.ico')
		about.iconphoto(False, icon_photo)

		title = Label(master=about, text="KALKULATOR WAKTU\nSHALAT", font=self.fontstyle3, justify='center', fg='green')
		email = Label(master=about, text="Adh : i_alimurrijal@student.ub.ac.id", font=self.fontstyle, justify='center')
		version = Label(master=about, text="Version 1.5 - @2020", font=self.fontstyle, justify='center')
		title.pack()
		email.pack()
		version.pack()

	def dataset(self):
		'''Memuat dataset yang digunakan pada perhitungan waktu sholat'''

		dataset = pd.read_csv(os.path.dirname(os.getcwd())+'/data/KOTA_DATABASE_COMPLETE.csv', sep=';')
		negara = dataset.Country
		negara = negara.drop_duplicates()

		return negara, dataset

	def frame_1(self): 
		'''Frame - 1'''

		title = Label(self.frame1, text="Masukkan Input", font=(self.fontstyle), fg='darkgreen', bg='#f0f8ff')
		title.place(x=75, y=5)
		#Style
		style = ttk.Style()
		style.theme_use('clam')

		#Label
		lbl_negara = Label(self.frame1, text='Negara 	    : ', font=self.fontstyle, bg='#f0f8ff')
		tanggal = Label(self.frame1, text='Tanggal 	    : ', font=self.fontstyle, bg='#f0f8ff')
		lbl_kota = Label(self.frame1, text='Kota    	    :', font=self.fontstyle, bg='#f0f8ff')
		lbl_tanggalVar = StringVar()
		lbl_tanggal = Label(self.frame1, text=self.kalender.selection_get(), font=self.fontstyle, width=15, justify='center', bg='lightgreen')

		def select_date():
			'''Memilih tanggal pada kalendar'''

			date = self.kalender.selection_get()
			lbl_tanggal.configure(text=date)

		#Tombol OK
		ok_button = Button(self.frame1, text='OK', font=self.fontstyle2, width=2, command=select_date)
		ok_button.place(x=515, y=170)

		#Combobox Negara dan Kota
		style.map('TCombobox', fieldbackground=[('readonly', 'lightgreen')])
		style.map('TCombobox', background=[('readonly', 'lightgreen')])
		style.map('TCombobox', foreground=[('readonly', 'black')])
		cmb_negaraVar = StringVar()
		self.cmb_negara = ttk.Combobox(self.frame1, textvariable='cmb_negaraVar', font=self.fontstyle, width=15, justify='center')
		
		cmb_kotaVar = StringVar()
		self.cmb_kota = ttk.Combobox(self.frame1, textvariable='cmb_kotaVar', font=self.fontstyle, width=15, justify='center')
		
		negara, dataset = self.dataset()
		value_negara = ['Pilih Negara']
		for country in negara:
			value_negara.append(country)
		
		self.cmb_negara['values'] = value_negara
		self.cmb_negara['state'] = 'readonly'
		self.cmb_negara.current(0)

		#Place
		lbl_negara.place(x=5, y=32)
		tanggal.place(x=5, y=100)
		self.cmb_negara.place(x=100, y=32)
		lbl_tanggal.place(x=100, y=100)
		lbl_kota.place(x=5, y=68)
		self.cmb_kota.place(x=100, y=65)

	def frame_2(self):
		'''Frame - 2'''

		#Mengammbil tanggal hari ini
		hari_ini = datetime.datetime.now()
		hari = hari_ini.weekday()
		nama_hari = calendar.day_name[hari]

		harii = '{}, {} {} {}'.format(nama_hari, hari_ini.day, hari_ini.strftime('%B'), hari_ini.year)

		def time():
			'''Konfigurasi lbl_jam denga format H:M:S'''

			string = strftime('%H:%M:%S')
			lbl_jam.config(text = string)
			lbl_jam.after(1000, time)

		lbl_hari = Label(self.frame2, text=harii, font=self.fontstyle, bg='#7eb593')
		lbl_jam = Label(self.frame2, font=('Times New Roman', 50), bg='#7eb593')
		time()

		lbl_hari.place(x=100, y=70)
		lbl_jam.place(x=70, y=95)

	def take_city_value(self):
		'''Mengambil value dari Combobox berupa negara dan kota'''

		negara, dataset = self.dataset()
		negara_pilih = self.cmb_negara.current()

		def callback(eventObject):
			'''Event handling, jika terjadi event pada combobox Negara, akan menambilkan
				daftar kota paa combobox Kota'''

			pilihan_negara = eventObject.widget.get()
			print(eventObject.widget.get()) #Negara yang dipilih User
			negara_mask = dataset["Country"].values == pilihan_negara
			kota = dataset["City"].loc[negara_mask]

			self.value_kota = []
			for city in kota:
				self.value_kota.append(city)

			self.cmb_kota['values'] = self.value_kota
			self.cmb_kota['state'] = 'readonly'
			self.cmb_kota.current(0)
		
		#Bind callback ke combobox
		self.cmb_negara.bind("<<ComboboxSelected>>", callback)

		kota_cmb = self.cmb_kota.get()
		negara_cmb = self.cmb_negara.get()
		print(kota_cmb) #Kota yang dipilih User
		nama_kota = dataset.loc[dataset['City'] == kota_cmb]
		
		return nama_kota, kota_cmb, negara_cmb

	def hitung_waktu_shalat(self):
		'''Menghitung waktu sholat dengan menggunakan module Waktu Sholat'''
		
		nama_kota, kota_cmb, negara_cmb = self.take_city_value()
		
		#Untuk pertama kali, nilai lintang dll harus ada nilainya,
		#sehingga perlu diinisialisasi
		try:
			lintang = float(nama_kota.Latitude.values[0])
			bujur = float(nama_kota.Longitude.values[0])
			ketinggian = nama_kota.Elevation.values[0]
			zona_waktu = nama_kota.Time_zone.values[0]
		except IndexError:	
			lintang =  0
			bujur = 0
			ketinggian = 50
			zona_waktu = 0
			
		tahun = self.kalender.selection_get().year
		bulan = self.kalender.selection_get().month
		tanggal = self.kalender.selection_get().day
	

		#Menambahkan tanda + pada zona waktu tertentu
		if int(zona_waktu) > 0:
			get_time_zone = '+'+str(zona_waktu)
		else:
			get_time_zone = str(zona_waktu)

		nama_bulanDict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
		no_bulan = list(nama_bulanDict.keys())
		nama_bulan = list(nama_bulanDict.values())
		jumlah_hari = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

		#Menempatkan nama kota, lintang, bujur dan zona waktu pada frame 2
		#nilainya akan diupdate setiap tombol hitung waktu sholat ditekan
		sign_lat = 'N'
		if lintang < 0:
			sign_lat = 'S'

		sign_lng = 'E'
		if bujur < 0:
			sign_lng = 'W'

		lbl_desc1 = Label(self.frame3, text=("{}").format(kota_cmb), width=20, font=('Times New Roman', 12, 'bold'), bg='#c0d6e4', fg='blue', justify='center')
		lbl_desc2 = Label(self.frame3, text=("{}\N{DEGREE SIGN} {}  -  {}\N{DEGREE SIGN} {}").format(abs(lintang), sign_lat, abs(bujur), sign_lng), width=20, font=('Times New Roman', 12, 'bold'), bg='#c0d6e4', fg='blue', justify='center')
		lbl_desc3 = Label(self.frame3, text=("GMT {}").format(get_time_zone), width=7, font=('Times New Roman', 12, 'bold'), bg='#c0d6e4', fg='blue', justify='center')
		lbl_desc1.place(x=720, y=60)
		lbl_desc2.place(x=720, y=83)
		lbl_desc3.place(x=783, y=103)

		#Jika user menyimpan file
		self.file_to_save1 = "\t\t\t\t\t\tJADWAL SHALAT BULANAN {}, {} - BULAN {} TAHUN {}\n".format(kota_cmb, negara_cmb, bulan, tahun)
		self.file_to_save2 = "\t\t\t\t\t\t\tLintang : {}\N{DEGREE SIGN} {}, Bujur : {}\N{DEGREE SIGN} {}, GMT : {}\n\n\n".format(abs(lintang), sign_lat, abs(bujur), sign_lng, get_time_zone)

		def isLeap(tahun):
			'''Menentukan apakah tahun kabisat atau tidak'''

			kabisat = 28
			if tahun % 4 == 0:
				if tahun % 100 == 0:
					if tahun % 400 == 0:
						kabisat = 29
					else:
						kabisat = 28
				else:
					kabisat = 29
			else:
				kabisat = 28
			return kabisat

		if bulan == 2:
			jumlah_hari[1] = isLeap(tahun)

		month = []
		date = 0
		for i in range(0, len(no_bulan)+1):
			if bulan == no_bulan[i-1]:
				month.append(nama_bulan[i-1])
			if i == bulan:
				date = (jumlah_hari[i-1])
		
		#List kosong jadwal sholat	
		subuh_list = []
		terbit_list = []
		zuhur_list = []
		ashar_list = []
		maghrib_list = []
		isya_list = []

		for day in range(1, int(date)+1):
			#Jika value error (untuk lintang ekstrem) akan menghitung waktu sholat
			#dengan menggunakan class LintangEkstrem
			#kekurangan --> tanggal terkhir tidak dihitung / listnya kosong
			try:
				jadwal_shalat = WaktuSholat(tahun, bulan, day, lintang, bujur, zona_waktu, ketinggian)
				subuh, terbit, zuhur, ashar, maghrib, isya = jadwal_shalat.show_result()
				subuh_list.append(subuh)
				terbit_list.append(terbit)
				zuhur_list.append(zuhur)
				ashar_list.append(ashar)
				maghrib_list.append(maghrib)
				isya_list.append(isya)

			except ValueError:
				try:
					jadwal_shalat = LintangEkstrem(tahun, bulan, day, lintang, bujur, zona_waktu, ketinggian)
					subuh, terbit, zuhur, ashar, maghrib, isya = jadwal_shalat.result()
					subuh_list.append(subuh)
					terbit_list.append(terbit)
					zuhur_list.append(zuhur)
					ashar_list.append(ashar)
					maghrib_list.append(maghrib)
					isya_list.append(isya)
				except IndexError:
					continue
				continue

		self.lbl_date = Label(self.frame3, text='{} {} {}'.format(tanggal, month[0], tahun), width=10, font=self.fontstyle3, bg='#c0d6e4', justify="center", fg='green')
		self.lbl_date.place(x=770, y=35)

		return date, month, subuh_list, terbit_list, zuhur_list, ashar_list, maghrib_list, isya_list

	def convert_button(self):
		'''Membuat button / tombol konversi'''

		style = ttk.Style()
		style.configure('TButton', font=self.fontstyle2, bg='dark green', width=10)
		btn_convert = ttk.Button(self.frame1, text='Hitung Waktu Sholat', style='TButton', width=20, command=self.take_value)
		btn_convert.place(x=60, y=160)

	def take_value(self):
		'''Perintah mengambil nilai'''

		print("Proccesing . . . .")
		date, month, subuh, terbit, zuhur, ashar, maghrib, isya = self.hitung_waktu_shalat()
		tanggal = self.kalender.selection_get().day
		print("Finished. . . ")
		self.scr_jadwal.delete(1.0, END)
		x_tanggal = 3
		x_subuh = x_tanggal+135
		x_terbit = x_subuh+135
		x_zuhur = x_subuh+135
		x_ashar = x_zuhur+135
		x_maghrib = x_ashar+135
		x_isya = x_maghrib+135
		y_size = 30

		for i in range(0, date):
			if i+1 < 10:
				self.scr_jadwal.state = NORMAL
				self.scr_jadwal.insert(END, '  0{} {}           \t{}         \t{}           \t{}          \t {}           \t  {}        \t  {}\n'.format(i+1, str(month[0]), subuh[i],
								terbit[i], zuhur[i], ashar[i], maghrib[i], isya[i]))
				self.scr_jadwal.state = DISABLED
			else:
				self.scr_jadwal.state = NORMAL
				self.scr_jadwal.insert(END, '  {} {}           \t{}         \t{}           \t{}          \t {}           \t  {}        \t  {}\n'.format(i+1, str(month[0]), subuh[i],
								terbit[i], zuhur[i], ashar[i], maghrib[i], isya[i]))
				self.scr_jadwal.state = DISABLED

			if tanggal == i+1:
				lbl_subuh = Label(self.frame3, text=subuh[i], font=self.fontstyle3, bg='#c0d6e4', fg='green')
				lbl_terbit = Label(self.frame3, text=terbit[i], font=self.fontstyle3, bg='#c0d6e4', fg='green')
				lbl_zuhur = Label(self.frame3, text=zuhur[i], font=self.fontstyle3, bg='#c0d6e4', fg='green')
				lbl_ashar = Label(self.frame3, text=ashar[i], font=self.fontstyle3, bg='#c0d6e4', fg='green')
				lbl_maghrib = Label(self.frame3, text=maghrib[i], font=self.fontstyle3, bg='#c0d6e4', fg='green')
				lbl_isya = Label(self.frame3, text=isya[i], font=self.fontstyle3, bg='#c0d6e4', fg='green')

				lbl_subuh.place(x=820, y=140)
				lbl_terbit.place(x=820, y=180)
				lbl_zuhur.place(x=820, y=220)
				lbl_ashar.place(x=820, y=260)
				lbl_maghrib.place(x=820, y=300)
				lbl_isya.place(x=820, y=340)

	def frame_3(self):
		'''Frame - 3'''

		tahun = self.kalender.selection_get().year
		bulan = self.kalender.selection_get().month
		tanggal = self.kalender.selection_get().day

		date, month, subuh, terbit, zuhur, ashar, maghrib, isya = self.hitung_waktu_shalat()
	
		lbl_index = Label(self.frame3, text='', bg='#23dd17', font=self.fontstyle2, width='87')
		lbl_index.place(x=3, y=3)
		indexx = ['TANGGAL', 'SUBUH', 'TERBIT', 'ZUHUR', 'ASHAR', ' MAGHRIB', '   ISYA']
		x_size = 3
		y_size = 3
		
		for i in range(0, len(indexx)):
			lbl_tanggal = Label(self.frame3, text=indexx[i], font=self.fontstyle2, bg='#23dd17')
			lbl_tanggal.place(x=x_size, y=y_size)
			x_size = x_size + 100

		self.scr_jadwal = scrolledtext.ScrolledText(self.frame3, width=85, height=18, bg='#c0d6e4', font=self.fontstyle)
		self.scr_jadwal.place(x=5, y=30)

		lbl_jadwal = Label(self.frame3, text='JADWAL SHALAT', font=self.fontstyle3, bg='#c0d6e4', fg='black')
		lbl_jadwal.place(x=750, y=15)

		x_size2 = 730
		y_size2 = 140
		index = ['SUBUH', 'TERBIT', 'ZUHUR', 'ASHAR', 'MAGHRIB', 'ISYA']
		for i in range(0, len(index)):
			lbl_subuh = Label(self.frame3, text=index[i], font=self.fontstyle, bg='#c0d6e4', fg='black')
			lbl_subuh.place(x=x_size2, y=y_size2)
			y_size2 = y_size2+40

	def save_file(self):
		'''Command untuk menyimpan file dalam format .txt'''

		files = [('Text Document', '*.txt')]
		file = asksaveasfile(mode='w', filetypes=files, defaultextension=files)

		if file is None:  #Jika user menekan cancel
			return

		file_to_save3 = "  TANGGAL           \tSUBUH         \t\tTERBIT           \tZUHUR        \t\t ASHAR           \t  MAGHRIB        \t  ISYA\n"
		file_to_save4 = "------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
		file.write(self.file_to_save1)
		file.write(self.file_to_save2)
		file.write(file_to_save4)
		file.write(file_to_save3)
		file.write(file_to_save4)
		file.write(self.scr_jadwal.get("1.0", 'end'))
		file.close()


root = Tk()
app = Window(root)
root.geometry('950x650')
root.resizable(0,0)
root.wm_attributes("-transparentcolor", 'grey')
icon_photo = PhotoImage(file=os.path.dirname(os.getcwd())+'/data/cal_logo.ico')
root.iconphoto(False, icon_photo)
root.mainloop()
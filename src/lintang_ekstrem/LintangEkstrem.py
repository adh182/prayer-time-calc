import numpy as np 
from WaktuSholat import WaktuSholat
from datetime import date

class LintangEkstrem:  

	def __init__(self, tahun, bulan, tanggal, lintang, bujur, zona_waktu, ketinggian=100):
		self.tahun = tahun
		self.bulan = bulan
		self.tanggal = tanggal
		self.lintang = lintang
		self.bujur = bujur 
		self.zona_waktu = zona_waktu
		self.ketinggian = ketinggian

		self.tahun0 = tahun
		self.bulan0 = bulan
		self.tanggal0 = tanggal

		self.tahun1 = tahun
		self.bulan1 = bulan
		self.tanggal1 = tanggal
		
	def isLeap(self):
		'''Apakah tahun kabisat???'''
		kabisat = False
		if self.tahun % 4 == 0:
			if self.tahun % 100 == 0:
				if self.tahun % 400 == 0:
					kabisat = True
				else:
					kabisat = False
			else:
				kabisat = True
		else:
			kabisat = False

		return kabisat


	def prev_available(self):
		'''Mencari waktu sholat yang ada sebelum tanggal X'''

		no_bulan = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

		if self.isLeap() == True:
			jumlah_hari = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		else:
			jumlah_hari = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

		prev_available_date = []
		prev_available_month = []
		prev_available_year = []

		for i in range(1, len(no_bulan)+1):
			if self.bulan0 == i:
				banyak_hari = jumlah_hari[self.bulan0-1]
		
				if self.tanggal0 < banyak_hari:
					while self.tanggal0 > 0:
						self.tanggal0 = self.tanggal0 - 1
						# print(tanggal)
						if self.tanggal0 < 1:
							self.bulan0 = self.bulan0-1
							self.tanggal0 = jumlah_hari[self.bulan0-1]
						if self.bulan0 < 1:
							self.tahun0 = self.tahun0 - 1
							self.bulan0 = 12
						try:
							jadwal_shalat = WaktuSholat(self.tahun0, self.bulan0,self.tanggal0, self.lintang, self.bujur, self.zona_waktu, self.ketinggian)
							subuh, terbit, zuhur, ashar, maghrib, isya = jadwal_shalat.show_result()

							prev_available_date.append(self.tanggal0)
							prev_available_month.append(self.bulan0)
							prev_available_year.append(self.tahun0)
							break
						except:
							continue

		return (prev_available_year, prev_available_month, prev_available_date)


	def next_available(self):
		'''Mencari waktu sholat yang ada setelah tanggal X'''

		no_bulan = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

		if self.isLeap() == True:
			jumlah_hari = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		else:
			jumlah_hari = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

		next_available_date = []
		next_available_month = []
		next_available_year = []

		for i in range(1, len(no_bulan)+1):
			if self.bulan1 == i:
				banyak_hari = jumlah_hari[self.bulan1-1]
				
				if self.tanggal1 < banyak_hari:
					
					while self.tanggal1 > 0:
						self.tanggal1 = self.tanggal1 + 1
						
						if self.tanggal1 > jumlah_hari[self.bulan1-1]:
							self.bulan1 = self.bulan1 + 1
							self.tanggal1 = jumlah_hari[self.bulan1-1]
						if self.bulan1 > 12:
							self.tahun1 = self.tahun1 + 1
							self.bulan1 = 1
						try:
							jadwal_shalat = WaktuSholat(self.tahun1, self.bulan1, self.tanggal1, self.lintang, self.bujur, self.zona_waktu, self.ketinggian)
							subuh, terbit, zuhur, ashar, maghrib, isya = jadwal_shalat.show_result()
							
							next_available_date.append(self.tanggal1)
							next_available_month.append(self.bulan1)
							next_available_year.append(self.tahun1)
							break
						except:
							continue

		return (next_available_year, next_available_month, next_available_date)

	def take_date(self, prev_tahun, prev_bulan, prev_tanggal, next_tahun, next_bulan, next_tanggal):
		'''Mengambil tanggal sebelum dan sesudah tanggal X'''

		date1 = date(prev_tahun[0], prev_bulan[0], prev_tanggal[0])
		date2 = date(next_tahun[0], next_bulan[0], next_tanggal[0])
		date_now = date(self.tahun, self.bulan, self.tanggal)
		I = date2 - date1
		C = date_now - date1

		return date1, date2, date_now, I, C

	def calculate_date(self, waktuA, waktuB):
		'''Mengecek waktu sholat tanggal A dan B dan return dalam format jam desimal'''

		def split_time(time):
			'''Mengambil jam, menit dan detik'''
			hour = int(time[0:2])
			minute = int(time[3:5])
			second = int(time[6:8])

			return hour, minute, second

		def convert_to_decimal(jam, menit, detik):
			'''Konversi jam, menit, detik ke desimal'''

			detik_des = detik/3600
			menit_des = menit/60
			jam_des = jam+menit_des+detik_des
			return jam_des

		#cari waktu sholat 
		jamB, menitB, detikB = split_time(waktuB)
		jamA, menitA, detikA = split_time(waktuA)

		jam_desB = convert_to_decimal(jamB, menitB, detikB)
		jam_desA = convert_to_decimal(jamA, menitA, detikA)

		return jam_desB, jam_desA


	def calculate_interpolate(self, A, B, I, C):
		'''Interpolasi nilai pada tanggal X'''

		time = A - (A-B)*C/I

		pukul = int(time)
		menit = int((time - pukul)*60)
		detik = int((((time - pukul)*60) - menit )*60)

		if pukul<10:
			pukul = '0'+str(pukul)
		if menit<10:
			menit = '0'+str(menit)
		if detik<10:
			detik = '0'+str(detik)
		hasil = '{}:{}:{}'.format(pukul, menit, detik)
		return hasil

	def count_time(self):
		'''Menghitung waktu sholat subuh sampai isya'''

		prev_tahun, prev_bulan, prev_tanggal = self.prev_available()
		next_tahun, next_bulan, next_tanggal = self.next_available()
		dateA, dateB, dateC, I, C = self.take_date(prev_tahun, prev_bulan, prev_tanggal, next_tahun, next_bulan, next_tanggal)

		jadwal_shalatA = WaktuSholat(dateA.year, dateA.month, dateA.day, self.lintang, self.bujur, self.zona_waktu)
		subuhA, terbitA, zuhurA, asharA, maghribA,isyaA = jadwal_shalatA.show_result()

		jadwal_shalatB = WaktuSholat(dateB.year, dateB.month, dateB.day, self.lintang, self.bujur, self.zona_waktu)
		subuhB, terbitB, zuhurB, asharB, maghribB,isyaB = jadwal_shalatB.show_result()

		timeA = [subuhA, terbitA, zuhurA, asharA, maghribA, isyaA]
		timeB = [subuhB, terbitB, zuhurB, asharB, maghribB, isyaB]
		jadwal = []

		for i in range(0, len(timeA)):
			A, B = self.calculate_date(timeA[i], timeB[i])
			hasil = self.calculate_interpolate(A, B, I, C)
			jadwal.append(hasil)

		return jadwal

	#getter
	def result(self):
		'''Menampilkan hasil interpolasi'''
		jadwal = self.count_time()
		subuh = jadwal[0]
		terbit = jadwal[1]
		zuhur = jadwal[2]
		ashar = jadwal[3]
		maghrib = jadwal[4]
		isya = jadwal[5]

		return subuh, terbit, zuhur, ashar, maghrib, isya
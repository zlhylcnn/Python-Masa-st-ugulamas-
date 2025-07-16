import tkinter as tk
from tkinter import ttk, messagebox
import json
import sys
from tkinter import font as tkfont
import os
from tkinter import PhotoImage

class YemekTarifiUygulamasi:
    def __init__(self, root):
        if sys.platform == "win32":
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)

        self.root = root
        self.root.title("Yemek Tarifi Önerici <3")
        self.root.geometry("1500x800")
        self.root.configure(bg="#f5f5f5")
        
        # Stil ayarları
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Renk paleti
        self.colors = {
            'primary': '#4CAF50',
            'secondary': '#8BC34A',
            'accent': '#FFC107',
            'background': '#f5f5f5',
            'text': '#212121',
            'light_text': '#757575',
            'card': '#FFFFFF',
            'border': '#E0E0E0'
        }
        
        # Stil konfigürasyonları
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], foreground=self.colors['text'])
        self.style.configure('TButton', background=self.colors['primary'], foreground='white', borderwidth=1)
        self.style.map('TButton', 
                      background=[('active', self.colors['secondary']), ('pressed', self.colors['accent'])])
        self.style.configure('TCombobox', fieldbackground='white', background='white')
        self.style.configure('TCheckbutton', background=self.colors['background'], foreground=self.colors['text'])
        
        # Emoji desteği için font ayarı 
        self.emoji_font = ("Segoe UI Emoji", 12) if sys.platform == "win32" else ("Apple Color Emoji", 14)

        # Malzeme-emoji eşleştirmeleri (orijinal kodunuzdaki gibi)
        self.malzeme_emojileri = {
            # Emoji eşleştirmeler kısmı...
            "Biberiye": "🌿", "Tatlı Patates": "🍠", "Pancar": "🍠", "Mantar": "🍄","Kültür Mantarı": "🍄", "Balkabağı": "🎃",
            "Soğan": "🧅", "Havuç": "🥕", "Patates": "🥔", "Domates": "🍅", "Salatalık": "🥒",
            "Patlıcan": "🍆", "Kabak": "🥬", "Biber": "🌶️", "Kapya Biber": "🌶️","Dolmalık Biber":"🌶️", "Bezelye": "🫛",
            "Pazı": "🥬", "Ispanak": "🥬", "Lahana": "🥬", "Brüksel Lahanası": "🥬", "Kereviz": "🥬",
            "Turp": "🍠", "Brokoli": "🥦", "Bakla": "🫛","Taze Bakla": "🫛","Maydanoz": "🌿", "Marul": "🥬",
            "Enginar": "🥬", "Pırasa": "🧅", "Karnabahar": "🥦", "Yer Elması": "🍠",
            "Şevketibostan": "🌿", "Roka": "🌱", "Taze Fasulye": "🫛", "Bamya": "🌱",
            "Kırmızı Lahana": "🥬", "Kuşkonmaz": "🌱", "Yeşil Soğan": "🧅", "Dereotu": "🌿",
            "Taze Nane": "🌿", "Fesleğen": "🌿","Sarımsak":"🧅","Trüf Mantarı": "🍄","Porçini Mantarı": "🍄",

            # Meyveler
            "Siyah Zeytin": "🫒", "Elma": "🍎", "Muz": "🍌", "Armut": "🍐", "Çilek": "🍓",
            "Erik": "🍑", "Kiraz": "🍒", "Vişne": "🍒", "Mandalina": "🍊", "Portakal": "🍊",
            "Turunç": "🍊", "Bergamot": "🍊", "Kumkat": "🍊", "Ayva": "🍐", "Kivi": "🥝",
            "Üzüm": "🍇", "İncir": "🍈", "Alıç": "🍒", "Hurma": "🌴", "Karadut": "🫐",
            "Beyaz Dut": "🍇", "Frambuaz": "🍓", "Kavun": "🍈", "Karpuz": "🍉", "Kayısı": "🍑",
            "Şeftali": "🍑", "Yaban Mersini": "🫐", "Kuşburnu": "🌹", "Malta Eriği": "🍊",
            "Muşmula": "🍐", "Yenidünya": "🍑","  ,Altın çilek": "🍓", "Ananas": "🍍",
            "Mango": "🥭", "Avakado": "🥑", "Hindistan Cevizi": "🥥", "Papaya": "🍈",
            "Pomelo": "🍊", "Yıldız Meyvesi": "⭐", "Pitaya": "🐉", "Liçi": "🍒",
            "Ejder Meyvesi": "🐉",

            # Soslar
            "Domates Sosu": "🍅","Domates Salçası" : "🍅","Tatlı Biber Salçası" : "🍅","Acı Biber Salçası" : "🍅","Ketçap": "🍅", "Mayonez": "🥄", "Hardal": "🌭", "Soya Sosu": "🍶",
            "Limon Sosu": "🍋", "Barbekü": "🍖", "Ranch Sos": "🥛", "Acı Sos": "🌶️",
            "Nar Ekşisi": "🍯", "Hamburger Sosu": "🍔", "Cheddar Sos": "🧀", "Köri Sos": "🌿",
            "Pesto Sos": "🌿", "Sirke": "🍶", "Chipotle Sos": "🌶️",

            # Baklagiller
            "Kuru Börülce": "🫘", "Kırmızı Mercimek": "🫘", "Nohut": "🫘", "Kuru Fasulye": "🫘",
            "Yeşil Mercimek": "🫘", "Bulgur": "🌾", "Pirinç": "🍚", "Buğday": "🌾",
            "Maş Fasulyesi": "🫘", "Un": "🌾", "Yulaf Unu": "🌾", "Tam Buğday Unu": "🌾",
            "Mısır Unu": "🌽", "Galeta Unu": "🍞", "Siyez Unu": "🌾", "Karabuğday": "🌾",
            "Makarna": "🍝", "Erişte": "🍜", "Spagetti": "🍝",
            "Arpa Şehriye": "🌾", "Tel Şehriye": "🍜","Arborio Pirinci": "🍚",

            # Hayvansal Gıdalar
            "Süt": "🥛", "Yoğurt": "🥛", "Süzme Yoğurt": "🥛", "Beyaz Peynir": "🧀","Lor Peyniri":"🧀","Labne":"🧀","Rokfor Peyniri":"🧀","Hellim Peyniri":"🧀","Mascarpone Peyniri":"🧀","Künefe Peyniri":"🧀","Ezine Peyniri":"🧀","Kaymak":"🥛",
            "Tereyağı": "🧈", "Krema": "🥛", "Tavuk": "🍗",
            "Tavuk Göğsü": "🍗", "Tavuk But": "🍗",
            "Kaşar Peyniri": "🧀",
            "Mozeralla": "🧀", "Parmesan": "🧀","Cheddar": "🧀", "Yumurta": "🥔",

            # Baharatlar ve Tatlandırıcılar
            "Tuz": "🧂", "Şeker": "🍬", "Esmer Şeker": "🍬", "Bal": "🍯", "Pekmez": "🍯",
            "Agave Şurubu": "🍯", "Stevia": "🍃", "Dut Kurusu": "🍇", "Karabiber": "⚫",
            "Pulbiber": "🌶️", "Kimyon": "🌿", "Nane": "🌿", "Kekik": "🌿", "Köri": "🌿",
            "Kırmızı Toz Biber": "🌶️", "İsot": "🌶️", "Sumak": "🌿", "Zerdeçal": "🌿",
            "Zencefil": "🌿", "Sarımsak Tozu": "🧄", "Soğan Tozu": "🧅", "Çörek Otu": "⚫",
            "Susam": "⚫", "Hindistan Cevizi Tozu": "🥥","Hindistan Cevizi Sütü": "🥛", "Kahve": "☕", "Defne Yaprağı": "🌿",
            "Biberiye": "🌿", "Karanfil": "🌿", "Mahlep": "🌿", "Tarçın": "🌿", "Salep": "🌿",
            "Kakao": "🍫", "Vanilya": "🌿", "Kabartma Tozu": "🧂", "Pudra Şekeri": "🍬",
            "Karbonat": "🧂", "Kuş Üzümü": "🍇", "Kişniş": "🌿", "Safran": "🌿", "Muskat": "🌿",
            "Reyhan": "🌿", "Meyankökü": "🌿", "Adaçayı": "🌿", "Ihlamur": "🌿", "Kajun": "🌿",

            # Glutensiz Ürünler
            "Pirinç": "🍚", "Soya": "🫘", "Patates": "🥔", "Karabuğday": "🌾",
            "Maş Fasulyesi": "🫘", "Kinoa": "🌾", "Yulaf": "🌾", "Arorat": "🌾",
            "Amarant": "🌾", "Keten Tohumu": "🌱", "Chia Tohumu": "🌱",
            "Bezelye": "🫛", " Kırmızı Mercimek": "🫘", "Barbunya": "🫘", "Fındık": "🌰",
            "Fıstık": "🥜", "Badem": "🌰", "Ceviz": "🌰","Kestane":"🌰", "Leblebi": "🫘","Yulaf " :"🌱","Karnabahar Unu":"🌾","Yulaf Kepeği":"🌾", "Glutensiz Şehriye":"🌾",
            "Glütensiz Ekmek":"🌾",
            # Yağlar
            "Ayçiçek Yağı" : "🛢️", "Zeytinyağı": "🫒", "Hindistan Cevizi Yağı": "🥥",
            "Mısır Yağı": "🌽", "Susam Yağı": "⚫", "Kuyruk Yağı": "🥩", "İç Yağı": "🥩",

            # Diğer
            "Cızlak": "🍢", "Kepekli Ekmek": "🍞", "Pirinç": "🍚","Beyaz Şarap": "🥛",
            #en son eklediklerim
            "Glütensiz Lavaş":"🍞","Bitter Çikolata":"🍫","Sütlü Çikolata":"🍫","Belçika Çikolatası":"🍫","Damla Çikolata":"🍫","Nohut Unu":"🌾","Glütensiz Makarna":"🍝",
            "Hindistan Cevizi Unu":"🌾","Vanilin":"🌿","Haşhaş":"🌱","Mavi Haşhaş" :"🌱","Haşhaş Tohumu":"🌱","Pirinç Noodle":"🍝","Ramen Noodle":"🍝",
            "Tavuk Döner Eti":"🍗","Tavuk Kalçalı But":"🍗","Tavuk Baget":"🍗","Tavuk Kanatları":"🍗","Tavuk Pirzola":"🍗","Tavuk Bonfile":"🍗","Tavuk Ciğeri":"🍗",
            "Glütensiz Şehriye":"🍞","Glütensiz Lavaş":"🍞","Glütensiz Un Karışımı":"🍞","Glütensiz Ekmek":"🍞","Glütensiz Sandviç Ekmeği":"🍞",
            "Haşlanmış Nohut":"🫘","Tahin":"🌿","Tahin Helvası":"🍫",
            "Yulaf Ezmesi":"🌾","Balzamik Sosu":"⚫","Yoğurtlu Sos":"🥛","İnce Bulgur":"🌾","Baget Ekmeği":"🍞","Ekşi Mayalı Ekmek":"🍞","Trüf Yağı":"⚫",
            "Tam Buğday Ekmeği":"🍞","Közlenmiş Patlıcan":"🍆","Tam Tahıllı Ekmek":"🍞","Focaccio Ekmeği":"🍞","Esmer Pirinç":"🌾","Spagetti Makarna":"🍝",
            "Taglietelle Makarna":"🍝","Penne Makarna":"🍝","Fettucine Makarna":"🍝","Kuru Üzüm":"🍇","Kuru Maya":"🥛","Yaş Maya":"🥛","Milför Hamuru":"🍞",
            "Yufka":"🍞","Baklavalık Yufka":"🍞","Tortilla":"🍞","Sandviç Ekmeği":"🍞","Kuzu Kıyma":"🥩","Kuzu Kuşbaşı":"🥩","Kuzu Pirzola":"🥩","Kuzu Antrikot":"🥩",
            "Kuzu Kaburga":"🥩","Kuzu Bonfile":"🥩","Kuzu İncik":"🥩","Kuzu Gerdan":"🥩","Kuzu Ciğeri":"🥩" ,"Kuzu Eti":"🥩",
            "Dana Eti":"🥩","Dana Kuşbaşı":"🥩","Dana Kıyma":"🥩","Dana Pirzola":"🥩","Dana Antrikot":"🥩","Dana Bonfile":"🥩","Dana Kaburga":"🥩","Dana İncik":"🥩","Dana Ciğeri":"🥩","Kıyma":"🥩","Et Döner":"🥩",
            "Hamsi":"🐟","İstavrit":"🐟","Uskumru":"🐟","Levrek":"🐟","Çupra":"🐟","Somon":"🐟","Somon Fileto":"🐟","Sardalya":"🐟","Ton Balığı":"🐟","Mezgit":"🐟","Mezgit Fileto":"🐟","Yengeç":"🐟","Istakoz":"🐟","Karides":"🐟","Jumbo Karides":"🐟","Hindi Eti":"🦃","Hindi Kıyma":"🦃",
            "Sosis":"🥩","Midye":"🐟","Ördek Göğsü":"🥩","Ördek Eti":"🥩","Sucuk":"🥩","Pastırma":"🥩","Jambon":"🥩","Nar Suyu":"🍯","Limon Suyu":"🍯","Portakal Suyu":"🍯","Deniz Tuzu":"🧂",
            "Kaya Tuzu":"🧂","Himalaya Tuzu":"🧂","Limon Tuzu":"🧂","Tavuk Suyu":"🥛","Dövme Buğday":"🌾","Dolmalık Fıstık":"🫘","Mısır Nişastası":"🌱","Buğday Nişastası":"🌱",
            "Antep Fıstığı":"🌰","Tarhun Otu":"🌿","Kuru Bakla":"🫛","Beşamel Sos":"🥛","Pide":"🍞","Deniz Börülcesi":"🫛","Ebegümeci":"🌿","Nar":"🫐","Pezik(Pancar Sapı)":"🌿",
            "Asma Yaprağı":"🌿","Kuru İncir":"🫐","Reçel":"🍯","Ahududu Reçeli":"🍯","Gül Suyu":"🍯","Leblebi Unu":"🌾","Kurutulmuş Domates":"🍅","Şerbet":"🍯","Karamel Sos":"🍯","Çikolata Sosu":"🍫","Ahududu":"🫐",
            "Kedidili Bisküvi":"🛢️","Etimek":"🛢️","Pandispanya Keki":"🍞","Bisküvi":"🛢️","Bebe Bisküvisi":"🛢️","Petibör Bisküvi":"🛢️","Güllaç Yaprağı":"⚫",
            "Tel Kadayıf":"🍞","Ekmek Kadayıfı":"🍞","Krem Şanti":"🥛","Jelatin":"🍯","İrmik":"🌱","Kuskus":"🌱","Çam Fıstığı":"🌰","Badem Tozu":"🥛","Soda":"🥛","Yeni Bahar":"🌿","Haşlanmış Fasulye":"🫘","Kruton":"🍞",
            "Semizotu":"🌿","Kıvırcık Marul":"🥬","Çeri Domates":"🍅","Salkım Domates":"🍅","Pembe Domates":"🍅","Tam Buğday Lavaş":"🍞","Tam Buğday Lazanya":"🍞","Kereviz Sapı":"🌿","Mısır Yarması":"🌽","Haşlanmış Pancar":"🍠",
            "Sivri Yeşil Biber":"🌶️","Yeşil Biber": "🌶️","Kırmızı Biber": "🌶️","Deniz Hıyarı":"🥒","Altın Çilek":"🍓","Ejder Meyvesi":"🥭","Kornişon Turşu":"🥒","Pirinç Unu":"🌿",
         

        }

        # Başlık çerçevesi
        self.header_frame = ttk.Frame(self.root, style='TFrame')
        self.header_frame.pack(fill='x', padx=10, pady=10)
        
        # Başlık etiketi
        self.header_label = ttk.Label(
            self.header_frame, 
            text="Yemek Tarifi Önerici", 
            font=('Helvetica', 18, 'bold'),
            foreground=self.colors['primary']
        )
        self.header_label.pack(side='left')
        
        # Ana çerçeve
        self.main_frame = ttk.Frame(self.root, style='TFrame')
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Sağ taraf (tarif öneri alanı)
        self.right_frame = ttk.Frame(self.main_frame, width=500, style='TFrame')
        self.right_frame.pack(side="right", fill="y", padx=10)
        
        # Tarif paneli başlığı
        self.recipes_header = ttk.Label(
            self.right_frame, 
            text="Bulunan Tarifler", 
            font=('Helvetica', 12, 'bold'),
            foreground=self.colors['primary']
        )
        self.recipes_header.pack(pady=(10,5))
        
        # Listbox ve scrollbar için bir frame oluştur
        listbox_frame = ttk.Frame(self.right_frame, style='TFrame')
        listbox_frame.pack(pady=10, fill="both", expand=True)
        
        # Listbox stili
        self.style.configure('Listbox', 
                           background='white',
                           foreground=self.colors['text'],
                           selectbackground=self.colors['accent'],
                           selectforeground='black',
                           font=('Helvetica', 10),
                           borderwidth=1,
                           relief='solid')
        
        # Scrollbar oluştur
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox'ı scrollbar ile ilişkilendir
        self.tarif_listesi = tk.Listbox(
            listbox_frame, 
            height=30, 
            width=60, 
            yscrollcommand=scrollbar.set,
            bg='white',
            fg=self.colors['text'],
            selectbackground=self.colors['accent'],
            font=('Helvetica', 10),
            relief='solid',
            borderwidth=1
        )
        self.tarif_listesi.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tarif_listesi.yview)
        self.tarif_listesi.bind('<Double-1>', self.tarif_detayini_goster)
        
        # Buton çerçevesi
        button_frame = ttk.Frame(self.right_frame, style='TFrame')
        button_frame.pack(fill='x', pady=10)
        
        # Tarif öner butonu
        self.btn_oner = ttk.Button(
            button_frame, 
            text="Tarif Öner", 
            command=self.tarif_oner,
            style='TButton'
        )
        self.btn_oner.pack(side='left', fill='x', expand=True, padx=5)
        
        # Tarif Ekle butonu
        self.btn_tarif_ekle = ttk.Button(
            button_frame, 
            text="Tarif Ekle", 
            command=self.ac_tarif_ekleme_penceresi,
            style='TButton'
        )
        self.btn_tarif_ekle.pack(side='left', fill='x', expand=True, padx=5)

        # Kategori Seçimi
        ttk.Label(
            self.right_frame, 
            text="Yemek Türü Seçin:",
            font=('Helvetica', 10)
        ).pack(pady=(10, 0))
        
        self.kategoriler = ["Çorba","Salata", "Ana Yemek", "Kahvaltı", "Tatlı", "Kek","Meze","Aperatif Tarifler", "Diyet", "Glutensiz Yemek", "Hepsi"]
        self.kategori_secim = ttk.Combobox(
            self.right_frame, 
            values=self.kategoriler,
            font=('Helvetica', 10)
        )
        self.kategori_secim.set("Hepsi")
        self.kategori_secim.pack(pady=(0, 10), fill='x')

        # Sol taraf (malzeme seçim alanı)
        self.left_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Ana Canvas ve Scrollbar'lar
        self.main_canvas = tk.Canvas(
            self.left_frame,
            bg=self.colors['background'],
            highlightthickness=0
        )
        self.v_scroll = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.main_canvas.yview)
        self.h_scroll = ttk.Scrollbar(self.left_frame, orient="horizontal", command=self.main_canvas.xview)

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        self.main_canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Scrollable Frame
        self.scrollable_frame = ttk.Frame(self.main_canvas, style='TFrame')
        self.scrollable_frame_id = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Malzeme grupları
        self.malzeme_secimleri = {}

        # 4 sütunlu grid oluştur
        for i in range(4):
            self.scrollable_frame.columnconfigure(i, weight=1, uniform="group")

        # Malzeme gruplarını oluştur (orijinal kodunuzdaki gibi)
        self.olustur_malzeme_grubu("Sebzeler", ["Tatlı Patates", "Pancar","Haşlanmış Pancar", "Mantar","Kültür Mantarı","Trüf Mantarı","Porçini Mantarı", "Balkabağı","Soğan","Yeşil Soğan", "Havuç", "Patates", "Domates","Çeri Domates","Salkım Domates","Pembe Domates", "Salatalık", "Patlıcan","Közlenmiş Patlıcan", "Kabak", "Biber",
            "Kapya Biber", "Bezelye", "Pazı", "Ispanak", "Lahana", "Brüksel Lahanası","Dolmalık Biber",
            "Kereviz","Kereviz Sapı", "Turp", "Brokoli", "Bakla","Taze Bakla", "Maydanoz", "Marul","Kıvırcık Marul", "Enginar", "Pırasa",
            "Karnabahar", "Yer Elması", "Şevketibostan", "Roka", "Taze Fasulye", "Bamya",
            "Kırmızı Lahana","Sivri Yeşil Biber","Kırmızı Biber","Yeşil Biber", "Kuşkonmaz","Dereotu","Semizotu", "Taze Nane", "Fesleğen","Sarımsak","Deniz Hıyarı","Deniz Börülcesi","Ebegümeci","Pezik(Pancar Sapı)"
       ], 0, 0)  # ... orijinal malzeme listeleri
        self.olustur_malzeme_grubu("Meyveler", [ "Siyah Zeytin", "Elma", "Muz", "Armut", "Çilek", "Erik", "Kiraz", "Vişne",
            "Mandalina", "Portakal", "Turunç", "Bergamot", "Kumkat", "Ayva", "Kivi", "Üzüm",
            "İncir", "Alıç", "Hurma", "Karadut", "Beyaz Dut", "Frambuaz", "Kavun", "Karpuz",
            "Kayısı", "Şeftali", "Yaban Mersini", "Kuşburnu", "Malta Eriği", "Muşmula",
            "Yenidünya", "Altın Çilek", "Ananas", "Mango", "Avakado", "Hindistan Cevizi",
            "Papaya", "Pomelo", "Yıldız Meyvesi", "Pitaya", "Liçi", "Ejder Meyvesi","Kestane",  "Nar","Ahududu"
            ], 1, 0)
        self.olustur_malzeme_grubu("Soslar", ["Domates Salçası","Domates Sosu","Yoğurtlu Sos","Tatlı Biber Salçası","Acı Biber Salçası","Ketçap", "Mayonez", "Hardal",
            "Soya Sosu", "Limon Sosu","Barbekü","Ranch Sos","Acı Sos",
            "Nar Ekşisi","Hamburger Sosu","Cheddar Sos","Köri Sos","Pesto Sos",
            "Sirke","Chipotle Sos","Balzamik Sosu","Beşamel Sos","Karamel Sos","Çikolata Sosu"], 2, 0)
        self.olustur_malzeme_grubu("Baklagiller", ["Kuru Börülce", "Kuru Bakla","Kuru Fasulye","Haşlanmış Fasulye","Nohut","Haşlanmış Nohut","Barbunya","Kırmızı Mercimek","Yeşil Mercimek", "Bulgur","İnce Bulgur",
            "Pirinç","Esmer Pirinç", "Buğday","Dövme Buğday","Mısır Yarması", "Karabuğday", "Makarna","Spagetti Makarna","Taglietelle Makarna","Penne Makarna","Fettucine Makarna", "Kuskus","Erişte", "Spagetti",
              "Arpa Şehriye", "Tel Şehriye","İrmik"], 3, 0)
        self.olustur_malzeme_grubu("Hayvansal Gıdalar", [ "Süt","Yoğurt","Süzme Yoğurt","Yumurta","Beyaz Peynir","Lor Peyniri","Labne","Kaşar Peyniri","Mozeralla","Cheddar","Parmesan","Rokfor Peyniri","Hellim Peyniri",
            "Mascarpone Peyniri","Künefe Peyniri","Ezine Peyniri","Krema","Tereyağı",
            "Tavuk","Tavuk Döner Eti","Tavuk Göğsü","Tavuk But","Tavuk Kalçalı But","Tavuk Baget","Tavuk Kanatları","Tavuk Pirzola","Tavuk Bonfile","Tavuk Ciğeri",
            "Dana Eti","Dana Kuşbaşı","Dana Kıyma","Dana Pirzola","Dana Antrikot","Dana Bonfile","Dana Kaburga","Dana İncik","Dana Ciğeri","Kıyma","Et Döner",
            "Kuzu Kıyma","Kuzu Kuşbaşı","Kuzu Pirzola","Kuzu Antrikot","Kuzu Kaburga","Kuzu Bonfile","Kuzu İncik","Kuzu Gerdan","Kuzu Ciğeri" ,"Kuzu Eti",
            "Hamsi","İstavrit","Uskumru","Levrek","Çupra","Somon","Somon Fileto","Sardalya","Ton Balığı","Mezgit","Mezgit Fileto","Yengeç","Istakoz","Karides","Jumbo Karides","Hindi Eti","Hindi Kıyma",
            "Sosis","Midye","Ördek Göğsü","Ördek Eti","Sucuk","Pastırma","Jambon"], 0, 1)
        self.olustur_malzeme_grubu("Baharatlar ve Tatlandırıcılar", [ "Tuz","Deniz Tuzu","Kaya Tuzu","Himalaya Tuzu","Limon Tuzu","Şeker","Esmer Şeker","Gül Suyu","Reçel","Ahududu Reçeli","Bal","Soda","Pekmez","Tahin","Tahin Helvası","Kakao","Bitter Çikolata","Sütlü Çikolata","Belçika Çikolatası","Damla Çikolata",
            "Agave Şurubu","Şerbet","Stevia","Dut Kurusu","Kuru İncir", "Karabiber", "Pulbiber", "Kimyon", "Nane", "Kekik", "Köri",
            "Kırmızı Toz Biber", "İsot", "Sumak", "Zerdeçal", "Zencefil", "Sarımsak Tozu",
            "Soğan Tozu", "Çörek Otu", "Susam", "Hindistan Cevizi Tozu","Hindistan Cevizi Sütü", "Kahve",
            "Defne Yaprağı","Asma Yaprağı","Tarhun Otu", "Biberiye", "Karanfil", "Mahlep", "Tarçın","Yeni Bahar", "Salep", "Kakao","Vanilya","Vanilin", "Kabartma Tozu","Kuru Maya","Yaş Maya",
            "Pudra Şekeri","Krem Şanti","Jelatin","Karbonat", "Kuş Üzümü","Kuru Üzüm","Kurutulmuş Domates","Dolmalık Fıstık",
            "Kişniş", "Safran", "Muskat", "Reyhan", "Meyankökü", "Adaçayı", "Ihlamur", "Kajun","Beyaz Şarap","Kornişon Turşu","Nar Suyu","Limon Suyu","Portakal Suyu","Tavuk Suyu","Buğday Nişastası"], 1, 1)
        self.olustur_malzeme_grubu("Glütensiz Ürünler", ["Soya","Maş Fasulyesi","Kinoa","Yulaf","Arborio Pirinci","Arorat","Amarant","Keten Tohumu","Chia Tohumu","Haşhaş","Mavi Haşhaş","Haşhaş Tohumu",
            "Fındık","Fıstık","Badem","Badem Tozu","Ceviz","Leblebi","Antep Fıstığı","Çam Fıstığı",
            "Karnabahar Unu","Yulaf Kepeği","Yulaf Ezmesi","Yulaf Unu","Hindistan Cevizi Unu",
            "Glütensiz Şehriye","Glütensiz Lavaş","Glütensiz Un Karışımı","Glütensiz Ekmek","Glütensiz Makarna","Glütensiz Sandviç Ekmeği"], 2, 1)
        self.olustur_malzeme_grubu("Yağlar ve Unlu Mamüller", ["Ayçiçek Yağı","Zeytinyağı","Hindistan Cevizi Yağı","Mısır Yağı","Susam Yağı","Kuyruk Yağı","İç Yağı","Trüf Yağı",
            "Un","Tam Tahıllı Ekmek","Tam Buğday Unu","Tam Buğday Ekmeği",
            "Mısır Unu", "Galeta Unu", "Siyez Unu","Pirinç Unu","Nohut Unu","Leblebi Unu","Tel Kadayıf","Ekmek Kadayıfı",
            "Kedidili Bisküvi","Etimek","Pandispanya Keki","Bisküvi","Bebe Bisküvisi","Petibör Bisküvi","Güllaç Yaprağı","Pirinç Noodle","Ramen Noodle","Pide","Yufka","Baklavalık Yufka","Tortilla","Kruton","Baget Ekmeği","Ekşi Mayalı Ekmek","Tam Buğday Lavaş","Tam Buğday Lazanya","Focaccio Ekmeği","Sandviç Ekmeği","Milför Hamuru",
            "Mısır Nişastası","Buğday Nişastası"], 3, 1)

        # Tarifleri yükle
        self.tarifler = self.jsondan_tarifleri_yukle()
        self.bulunan_tarifler = []

        # Scrollbar ayarları
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind("<Configure>", self.on_canvas_configure)

        # Tarif ekleme penceresi için değişkenler
        self.tarif_ekleme_penceresi = None
        self.yeni_tarif_adi_entry = None
        self.yeni_tarif_malzemeler_text = None
        self.yeni_tarif_yapilis_text = None
        self.yeni_tarif_kategori_combobox = None
        self.diyet_var = tk.IntVar()
        self.glutensiz_var = tk.IntVar()
    def on_frame_configure(self, event):
        """Scroll bölgesini frame boyutuna göre ayarlar"""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Canvas boyutu değiştiğinde iç frame genişliğini ayarlar"""
        canvas_width = event.width
        self.main_canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)
        
    def olustur_malzeme_grubu(self, grup_adi, malzeme_listesi, column, row):
        group_frame = ttk.Frame(
            self.scrollable_frame,
            padding=10,
            relief='solid',
            style='Card.TFrame'
        )
        self.style.configure('Card.TFrame', 
                           background='white',
                           bordercolor=self.colors['border'],
                           borderwidth=1)
        
        group_frame.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

        # Grup başlığı
        ttk.Label(
            group_frame, 
            text=grup_adi, 
            font=('Helvetica', 11, 'bold'),
            foreground=self.colors['primary'],
            background='white'
        ).pack(pady=(0, 5))

        # Her grup için ayrı bir canvas ve scrollbar
        canvas = tk.Canvas(
            group_frame, 
            height=300, 
            width=220, 
            bd=0, 
            highlightthickness=0,
            bg='white'
        )
        scrollbar = ttk.Scrollbar(group_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = ttk.Frame(canvas, style='Card.TFrame')
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Checkbutton stili
        self.style.configure('TCheckbutton', 
                           background='white',
                           foreground=self.colors['text'],
                           font=('Helvetica', 9))
        
        for malzeme in malzeme_listesi:
            var = tk.IntVar()
            emoji = self.malzeme_emojileri.get(malzeme, "•")
            
            # Checkbutton yerine daha modern bir görünüm için Frame kullanıyoruz
            item_frame = ttk.Frame(inner_frame, style='Card.TFrame')
            item_frame.pack(anchor="w", padx=4, pady=2, fill='x')
            
            chk = tk.Checkbutton(
                item_frame,
                text=f" {emoji} {malzeme}",
                variable=var,
                anchor="w",
                width=22,
                font=self.emoji_font,
                bg='white',
                activebackground='white',
                selectcolor=self.colors['accent'],
                fg=self.colors['text'],
                activeforeground=self.colors['text']
            )
            chk.pack(side='left')
            
            self.malzeme_secimleri[malzeme] = var

        inner_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))

        # Grid ağırlıklarını ayarla
        self.scrollable_frame.rowconfigure(row, weight=1)
        self.scrollable_frame.columnconfigure(column, weight=1)
    def jsondan_tarifleri_yukle(self):
        """JSON dosyasından tarifleri yükler"""
        try:
            with open('recipess.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []  # Dosya yoksa boş liste döndür
        except json.JSONDecodeError:
            messagebox.showerror("Hata", "Tarif dosyası bozuk!")
            return []

    def tarif_oner(self):
        """Seçilen malzemelere göre tarif önerir ve listede gösterir"""
        # Seçilen malzemeleri al
        secilen_malzemeler = [m for m, var in self.malzeme_secimleri.items() if var.get() == 1]
        secilen_kategori = self.kategori_secim.get().lower()  # Küçük harfe çevir

        self.tarif_listesi.delete(0, tk.END)  # Listeyi temizle
        self.bulunan_tarifler = []  # Bulunan tarifleri sıfırla

        if not secilen_malzemeler:
            self.tarif_listesi.insert(tk.END, "⚠️ Lütfen en az 1 malzeme seçin!")
            return

        # Debug için seçilen malzemeleri göster
        print(f"Seçilen malzemeler: {secilen_malzemeler}")
    
        uygun_tarifler = []
        for tarif in self.tarifler:
            # Kategori filtresi
            if secilen_kategori != "hepsi" and tarif.get("kategori", "").lower() != secilen_kategori:
                continue
            
            # Malzeme kontrolü - daha esnek arama yapalım
            tarif_malzemeler_metin = tarif.get("malzemeler", "").lower()
            
            # Debug için tarif malzemelerini göster
            print(f"Tarif: {tarif['isim']}, Malzemeler: {tarif_malzemeler_metin}")
            
            # Tüm seçilen malzemeler tarifte varsa
            malzemeler_var = True
            for secilen_malzeme in secilen_malzemeler:
                # Malzeme ismini küçük harfe çevirip arama yapalım
                if secilen_malzeme.lower() not in tarif_malzemeler_metin:
                    print(f"  - '{secilen_malzeme}' malzemesi bulunamadı")
                    malzemeler_var = False
                    break
                else:
                    print(f"  + '{secilen_malzeme}' malzemesi bulundu")
            
            if malzemeler_var:
                print(f"Uygun tarif: {tarif['isim']}")
                uygun_tarifler.append(tarif)

        if uygun_tarifler:
            self.tarif_listesi.insert(tk.END, f"✅ {len(uygun_tarifler)} uygun tarif bulundu:")
            self.tarif_listesi.insert(tk.END, "")  # Boş satır ekle
            
            for index, tarif in enumerate(uygun_tarifler):
                kategori_text = tarif.get('kategori', 'Genel')
                self.tarif_listesi.insert(tk.END, f"🍴 {tarif['isim']} ({kategori_text})")
                self.bulunan_tarifler.append(tarif)  # Tarifleri geçici listeye kaydet
        else:
            self.tarif_listesi.insert(tk.END, "❌ Uygun tarif bulunamadı.")
            self.tarif_listesi.insert(tk.END, f"Seçilen malzemeler: {', '.join(secilen_malzemeler)}")
            self.tarif_listesi.insert(tk.END, f"Seçilen kategori: {secilen_kategori}")


    def tarif_detayini_goster(self, event):
        """Listeden seçilen tarifi detaylı gösterir"""
        secim_indeksleri = self.tarif_listesi.curselection()
        if not secim_indeksleri:
            return
        
        secim_indeksi = secim_indeksleri[0]
        if secim_indeksi < 2 or secim_indeksi >= len(self.bulunan_tarifler) + 2:
            return
        
        tarif_indeksi = secim_indeksi - 2
        secilen_tarif = self.bulunan_tarifler[tarif_indeksi]
        
        # Yeni pencere oluştur
        tarif_penceresi = tk.Toplevel(self.root)
        tarif_penceresi.title(secilen_tarif['isim'])
        tarif_penceresi.geometry("700x600")
        tarif_penceresi.configure(bg=self.colors['background'])
        
        # Ana frame
        main_frame = ttk.Frame(tarif_penceresi, style='TFrame')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Başlık
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            title_frame,
            text=secilen_tarif['isim'],
            font=('Helvetica', 18, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['background']
        ).pack(side='left')
        
        # Kategori ve etiketler
        info_frame = ttk.Frame(main_frame, style='TFrame')
        info_frame.pack(fill='x', pady=(0, 15))
        
        kategori_text = secilen_tarif.get('kategori', 'Genel')
        tk.Label(
            info_frame,
            text=f"Kategori: {kategori_text}",
            font=('Helvetica', 10),
            fg=self.colors['light_text'],
            bg=self.colors['background']
        ).pack(side='left', padx=(0, 15))
        
        # Özel etiketler
        etiketler = []
        if secilen_tarif.get('diyet', False):
            etiketler.append("🥗 Diyet")
        if secilen_tarif.get('glutensiz', False):
            etiketler.append("🌾 Glutensiz")
        
        if etiketler:
            tk.Label(
                info_frame,
                text=" | ".join(etiketler),
                font=('Helvetica', 10),
                fg=self.colors['primary'],
                bg=self.colors['background']
            ).pack(side='left')
        
        # Malzemeler
        tk.Label(
            main_frame,
            text="Malzemeler:",
            font=('Helvetica', 12, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['background']
        ).pack(anchor='w', pady=(10, 5))
        
        malzeme_alani = tk.Text(
            main_frame,
            height=8,
            wrap="word",
            font=('Helvetica', 10),
            bg='white',
            fg=self.colors['text'],
            padx=10,
            pady=10,
            relief='solid',
            borderwidth=1
        )
        malzeme_alani.insert("1.0", secilen_tarif['malzemeler'])
        malzeme_alani.config(state="disabled")
        malzeme_alani.pack(fill="x", pady=(0, 10))
        
        # Yapılış
        tk.Label(
            main_frame,
            text="Yapılış:",
            font=('Helvetica', 12, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['background']
        ).pack(anchor='w', pady=(10, 5))
        
        yapilis_alani = tk.Text(
            main_frame,
            height=15,
            wrap="word",
            font=('Helvetica', 10),
            bg='white',
            fg=self.colors['text'],
            padx=10,
            pady=10,
            relief='solid',
            borderwidth=1
        )
        yapilis_alani.insert("1.0", secilen_tarif['yapilis'])
        yapilis_alani.config(state="disabled")
        yapilis_alani.pack(fill="both", expand=True, pady=(0, 10))
        
        # Kapat butonu
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(
            btn_frame,
            text="Kapat",
            command=tarif_penceresi.destroy,
            style='TButton'
        ).pack(side='right')

    def ac_tarif_ekleme_penceresi(self):
        """Yeni tarif ekleme penceresini açar"""
        # Tarif ekleme penceresi açma kodu...
         
        if self.tarif_ekleme_penceresi is not None:
            self.tarif_ekleme_penceresi.lift()
            return
            
        self.tarif_ekleme_penceresi = tk.Toplevel(self.root)
        self.tarif_ekleme_penceresi.title("Yeni Tarif Ekle")
        self.tarif_ekleme_penceresi.geometry("600x700")
        self.tarif_ekleme_penceresi.protocol("WM_DELETE_WINDOW", self.tarif_ekleme_penceresini_kapat)
        
        # Ana frame
        main_frame = tk.Frame(self.tarif_ekleme_penceresi, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)
        
        # Tarif adı
        tk.Label(main_frame, text="Tarif Adı:").pack(anchor="w")
        self.yeni_tarif_adi_entry = tk.Entry(main_frame, width=50)
        self.yeni_tarif_adi_entry.pack(fill="x", pady=(0, 10))
        
        # Kategori
        tk.Label(main_frame, text="Kategori:").pack(anchor="w")
        self.yeni_tarif_kategori_combobox = ttk.Combobox(main_frame, values=self.kategoriler)
        self.yeni_tarif_kategori_combobox.pack(fill="x", pady=(0, 10))
        self.yeni_tarif_kategori_combobox.set("ana yemek")
        
        # Malzemeler
        tk.Label(main_frame, text="Malzemeler (virgülle ayırın):").pack(anchor="w")
        self.yeni_tarif_malzemeler_text = tk.Text(main_frame, height=10, wrap="word")
        self.yeni_tarif_malzemeler_text.pack(fill="x", pady=(0, 10))
        
        # Yapılış
        tk.Label(main_frame, text="Yapılış:").pack(anchor="w")
        self.yeni_tarif_yapilis_text = tk.Text(main_frame, height=15, wrap="word")
        self.yeni_tarif_yapilis_text.pack(fill="x", pady=(0, 10))
        
        # Özel özellikler
        ozel_frame = tk.Frame(main_frame)
        ozel_frame.pack(fill="x", pady=(0, 10))
        
        tk.Checkbutton(ozel_frame, text="Diyet Tarifi", variable=self.diyet_var).pack(side="left", padx=5)
        tk.Checkbutton(ozel_frame, text="Glutensiz", variable=self.glutensiz_var).pack(side="left", padx=5)
        
        # Butonlar
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        tk.Button(button_frame, text="İptal", command=self.tarif_ekleme_penceresini_kapat).pack(side="left", padx=(0, 10))
        tk.Button(button_frame, text="Kaydet", command=self.yeni_tarifi_kaydet).pack(side="left")

        pass

    def tarif_ekleme_penceresini_kapat(self):
        """Tarif ekleme penceresini kapatır"""
        # Tarif ekleme penceresini kapatma kodu...
        
        if self.tarif_ekleme_penceresi is not None:
            self.tarif_ekleme_penceresi.destroy()
            self.tarif_ekleme_penceresi = None
        pass

    def yeni_tarifi_kaydet(self):
        """Yeni tarifi kaydeder"""
        # Yeni tarif kaydetme kodu...
        """Yeni tarifi kaydeder"""
        tarif_adi = self.yeni_tarif_adi_entry.get().strip()
        if not tarif_adi:
            messagebox.showerror("Hata", "Tarif adı boş olamaz!")
            return
            
        malzemeler = self.yeni_tarif_malzemeler_text.get("1.0", tk.END).strip()
        if not malzemeler:
            messagebox.showerror("Hata", "En az bir malzeme eklemelisiniz!")
            return
            
        yapilis = self.yeni_tarif_yapilis_text.get("1.0", tk.END).strip()
        if not yapilis:
            messagebox.showerror("Hata", "Yapılış bilgisi boş olamaz!")
            return
            
        kategori = self.yeni_tarif_kategori_combobox.get().strip()
        diyet = bool(self.diyet_var.get())
        glutensiz = bool(self.glutensiz_var.get())
        
        yeni_tarif = {
            "isim": tarif_adi,
            "malzemeler": malzemeler,
            "yapilis": yapilis,
            "kategori": kategori,
            "diyet": diyet,
            "glutensiz": glutensiz
        }
        
        self.tarifler.append(yeni_tarif)
        self.tarifleri_jsona_kaydet()
        messagebox.showinfo("Başarılı", "Tarif başarıyla kaydedildi!")
        self.tarif_ekleme_penceresini_kapat()
        

    def tarifleri_jsona_kaydet(self):
     """Tarif listesini JSON dosyasına kaydeder"""
     try:
        # Aynı dosya adını kullanın
        with open('recipess.json', 'w', encoding='utf-8') as f:
            json.dump(self.tarifler, f, ensure_ascii=False, indent=4)
     except Exception as e:
        messagebox.showerror("Hata", f"Tarifler kaydedilirken hata oluştu:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YemekTarifiUygulamasi(root)
    root.mainloop()
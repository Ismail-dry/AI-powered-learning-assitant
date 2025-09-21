# Gerekli kütüphaneleri import ediyoruz
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QPushButton, QTextEdit, QSplitter,
    QTabWidget, QGroupBox, QProgressBar,QComboBox
)
#from PyQt6.QtMultimedia import QMediaPlayer
#from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView


# Önceki modüllerinizi olduğu gibi import ediyoruz
from web_scraper import WebScraper 
from ai_core import AICore
from youtube_transcript_api import YouTubeTranscriptApi
import re,os
from helper_audio import download_audio_temp_from_youtube, transcribe_audio_whisper
from youtubesearchpython import ChannelsSearch, Channel
from yt_dlp import YoutubeDL


class ModernButton(QPushButton):
    """Modern görünümlü özelleştirilmiş buton"""
    def __init__(self, text, color="primarzy"):
        super().__init__(text)
        self.setMinimumHeight(35)
        self.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        
        if color == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4A90E2, stop:1 #357ABD);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5BA0F2, stop:1 #4A90E2);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #357ABD, stop:1 #2E6BA8);
                }
                QPushButton:disabled {
                    background: #CCCCCC;
                    color: #666666;
                }
            """)
        elif color == "success":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5CB85C, stop:1 #449D44);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #6CC86C, stop:1 #5CB85C);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #449D44, stop:1 #398439);
                }
            """)
        elif color == "warning":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F0AD4E, stop:1 #EC971F);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F2BD5E, stop:1 #F0AD4E);
                }
            """)


class ModernLineEdit(QLineEdit):
    """Modern görünümlü input alanı"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E1E8ED;
                border-radius: 8px;
                padding: 8px 12px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
                background: #F8FBFF;
            }
            QLineEdit:hover {
                border-color: #4A90E2;
            }
        """)


class ModernTextEdit(QTextEdit):
    """Modern görünümlü metin alanı"""
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E1E8ED;
                border-radius: 8px;
                padding: 12px;
                background: white;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border-color: #4A90E2;
            }
        """)


class ModernGroupBox(QGroupBox):
    """Modern görünümlü grup kutusu"""
    def __init__(self, title):
        super().__init__(title)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2C3E50;
                border: 2px solid #E1E8ED;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: #FAFBFC;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background: #FAFBFC;
            }
        """)


class VideoAssistantApp(QMainWindow):
    """
    Modern tasarımlı AI Video Asistanı ana penceresi
    """
    def __init__(self ,username=None):
        super().__init__()
        self.current_username = username or 'Kullanıcı'

        self.fixed_channel_url = "https://www.youtube.com/@ADekoTechnologies"  # <== Kendi kanalınla değiştir

        # --- MODÜLLERİ BAŞLATMA ---
        self.scraper = WebScraper()
        self.channel_video_map = {}

        self.ai_core = AICore()

        # --- 1. Pencere Temel Ayarları ---
        self.setWindowTitle("🎬 AI Video Asistanı - Modern Interface")
        self.setGeometry(50, 50, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Modern tema ayarları
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F5F7FA, stop:1 #E9ECEF);
            }
        """)

        # --- 2. Ana Widget ve Layout ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Ana layout splitter ile bölünecek
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.central_widget.setLayout(QHBoxLayout())
        self.central_widget.layout().addWidget(main_splitter)

        # --- 3. Sol Panel (Video ve Kontroller) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(15, 15, 15, 15)

        # Video oynatıcı grubu
        video_group = ModernGroupBox("🎥 Video Oynatıcı")
        video_layout = QVBoxLayout(video_group)
        
        # Video widget
        #self.video_widget = QVideoWidget()
        self.video_widget = QWebEngineView()
        self.video_widget.setMinimumSize(400, 300)
        self.video_widget.setStyleSheet("""
        QWebEngineView {
            border: 2px solid #E1E8ED;
            border-radius: 8px;
        }
        """)

        #self.media_player = QMediaPlayer()
        #self.media_player.setVideoOutput(self.video_widget)
        
        # Video kontrol butonları
        #controls_layout = QHBoxLayout()
        #self.load_button = ModernButton("📁 Video Yükle", "primary")
        #self.play_button = ModernButton("▶️ Oynat", "success")
        #self.pause_button = ModernButton("⏸️ Duraklat", "warning")
        self.clear_youtube_summary_button = ModernButton("🗑️ AI Özeti Temizle", "warning")

        
        #self.play_button.setEnabled(False)
        #self.pause_button.setEnabled(False)

        summary_header_layout = QHBoxLayout()
        summary_title = QLabel("🤖 AI Özet:")
        summary_title.setFont(QFont("Segoe UI", 10))
        summary_title.setStyleSheet("color: #2C3E50;")

        summary_header_layout.addWidget(summary_title)
        summary_header_layout.addStretch()
        summary_header_layout.addWidget(self.clear_youtube_summary_button)
        
        

        
        #controls_layout.addWidget(self.load_button)
        #controls_layout.addWidget(self.play_button)
        #controls_layout.addWidget(self.pause_button)
        #controls_layout.addStretch()
        
        video_layout.addWidget(self.video_widget)
        #video_layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E1E8ED;
                border-radius: 8px;
                text-align: center;
                background: white;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A90E2, stop:1 #357ABD);
                border-radius: 6px;
            }
        """)
        
        left_layout.addWidget(video_group)
        left_layout.addWidget(self.progress_bar)
        left_layout.addStretch()

        # --- 4. Sağ Panel (Kontroller ve Sonuçlar) ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(15, 15, 15, 15)

        # Tab widget ile farklı işlevleri ayıralım
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #E1E8ED;
                border-radius: 8px;
                background: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #F8F9FA;
                border: 2px solid #E1E8ED;
                padding: 8px 20px;
                margin-right: 2px;
                border-radius: 8px 8px 0px 0px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background: #E9ECEF;
            }
        """)

        # --- Terim Arama Sekmesi ---
        search_tab = QWidget()
        search_layout = QVBoxLayout(search_tab)
        search_layout.setSpacing(15)

        # Arama grubu
        search_group = ModernGroupBox(f"🔍 Merhaba,{self.current_username}")
        search_group_layout = QVBoxLayout(search_group)
        
        search_label = QLabel("Nasıl yardımcı olabilirim ?")
        search_label.setFont(QFont("Segoe UI", 10))
        search_label.setStyleSheet("color: #2C3E50; margin-bottom: 5px;")
        
        self.term_input = ModernLineEdit("Örn: adekocam, etiket şablonu, takım yolu...")
        self.search_button = ModernButton("🚀 Ara ve Özetle", "primary")
        self.clear_search_button = ModernButton("🗑️ Temizle", "warning")
        
        search_input_layout = QHBoxLayout()
        search_input_layout.addWidget(self.term_input, 4)
        search_input_layout.addWidget(self.search_button, 2)
        search_input_layout.addWidget(self.clear_search_button, 1)
        
        search_group_layout.addWidget(search_label)
        search_group_layout.addLayout(search_input_layout)
        
        # Sonuçlar alanı
        result_group = ModernGroupBox("📋 Arama Sonuçları")
        result_layout = QVBoxLayout(result_group)
        
        # Clear button for results
        result_header_layout = QHBoxLayout()
        result_title = QLabel("Sonuçlar:")
        result_title.setFont(QFont("Segoe UI", 10))
        result_title.setStyleSheet("color: #2C3E50;")
        self.clear_results_button = ModernButton("🗑️ Sonuçları Temizle", "warning")
        self.clear_results_button.setMaximumWidth(150)
        
        result_header_layout.addWidget(result_title)
        result_header_layout.addStretch()
        result_header_layout.addWidget(self.clear_results_button)
        
        self.result_display = ModernTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(300)
        
        result_layout.addLayout(result_header_layout)
        result_layout.addWidget(self.result_display)
        
        search_layout.addWidget(search_group)
        search_layout.addWidget(result_group)
        
        self.tab_widget.addTab(search_tab, "🔍 AI Assistant")

        right_layout.addWidget(self.tab_widget)

        # 1. Sekme tanımla
        youtube_tab = QWidget()
        youtube_layout = QVBoxLayout(youtube_tab)

        # 2. Grup kutusu tanımla
        youtube_group = ModernGroupBox("📺 Sabit Kanal Videoları")
        youtube_group_layout = QVBoxLayout(youtube_group)

        # Transkript görüntüleme kutusu
        self.youtube_summary_display = ModernTextEdit()
        self.youtube_summary_display.setReadOnly(True)
        self.youtube_summary_display.setMinimumHeight(200)


        youtube_group_layout.addWidget(QLabel("🤖 AI Özet:"))
        youtube_group_layout.addWidget(self.youtube_summary_display)

        self.channel_video_combo = QComboBox()
        self.play_selected_video_button = ModernButton("🎬 Videoyu Özetle", "success")
        # Video seçim arayüzü
        video_select_layout = QVBoxLayout()

        video_select_layout.addWidget(QLabel("📽 Videolar:"))
        video_select_layout.addWidget(self.channel_video_combo)  
        video_select_layout.addWidget(self.play_selected_video_button)
        
        youtube_group_layout.addLayout(video_select_layout)
        youtube_layout.addWidget(youtube_group)
        youtube_group_layout.addLayout(summary_header_layout)
        youtube_group_layout.addWidget(self.youtube_summary_display)

         #5. Sekmeye ekle
        self.tab_widget.addTab(youtube_tab, "📺 YouTube")

        # Panelleri splitter'a ekle
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([400, 600])  # Sol panel 400px, sağ panel 600px

        # --- 5. Sinyal Bağlantıları ---
        self.search_button.clicked.connect(self.search_term_and_summarize)
        self.clear_search_button.clicked.connect(self.clear_search_input)
        self.clear_results_button.clicked.connect(self.clear_search_results)
        #self.load_button.clicked.connect(self.open_video_file)
        self.clear_youtube_summary_button.clicked.connect(self.clear_youtube_summary)

        #self.play_button.clicked.connect(self.media_player.play)
        #self.pause_button.clicked.connect(self.media_player.pause)
        #self.clear_youtube_button.clicked.connect(self.clear_youtube_input)
        #self.clear_youtube_results_button.clicked.connect(self.clear_youtube_results)
        #self.channel_search_button.clicked.connect(self.search_channel_by_name)
        #self.play_selected_video_button.clicked.connect(self.play_selected_video_from_channel)
        #self.youtube_button.clicked.connect(self.call_get_channel_videos_from_input)

        
        # Medya player sinyalleri
        #self.media_player.playbackStateChanged.connect(self.update_button_states)
        
        # Metin seçimi işlevi
        self.result_display.mouseDoubleClickEvent = self.handle_text_selection
        
        # Enter tuşu ile arama
        self.term_input.returnPressed.connect(self.search_term_and_summarize)
        #self.youtube_input.returnPressed.connect(self.process_youtube_link)

        self.load_fixed_channel_videos()
        self.channel_video_combo.currentIndexChanged.connect(self.play_video_only_from_combo)

        self.play_selected_video_button.clicked.connect(self.play_selected_video_from_channel)


    def play_video_only_from_combo(self):
        """Sadece video oynat, AI özetleme yapma"""
        title = self.channel_video_combo.currentText()
        if not hasattr(self, "channel_video_map") or not title:
            print("⚠️ Önce video seçin.")
            return

        url = self.channel_video_map.get(title)
        if url:
            self.play_youtube_embed_video(url)
        else:
            print("❌ Video bağlantısı bulunamadı.")

    def play_selected_video_from_channel(self):
        """Seçilen videoyu oynatma ve AI dekript başlatma"""
        title = self.channel_video_combo.currentText()
        if not hasattr(self, "channel_video_map") or not title:
            print("⚠️ Önce video seçin.")
            return

        url = self.channel_video_map.get(title)
        if url:
            self.play_youtube_embed_video(url)
            self.process_youtube_link(url)
        else:
            print("❌ Video bağlantısı bulunamadı.")

    def play_youtube_embed_video(self, url):
        match = re.search(r"(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})", url)
        if not match:
            print("❌ Geçerli bir YouTube bağlantısı değil.")
            return

        video_id = match.group(1)
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0"
        self.video_widget.setUrl(QUrl(embed_url))
        #self.play_button.setEnabled(False)
        #self.pause_button.setEnabled(False)
    def process_youtube_link(self, url=None):
        """YouTube videosunu AI ile dekript etme"""
        if url is None:
            print("⚠️ Video URL'si bulunamadı.")
            return

        self.show_progress("YouTube transkript alınıyor...")
        print("⏳ Video decript ediliyor, lütfen bekleyin...")
        QApplication.processEvents()

        # Transkript al
        transcript_text = self.get_transcript_from_youtube(url)

        if transcript_text.startswith("❌") or transcript_text.startswith("⚠️"):
            print(transcript_text)
            self.hide_progress()
            return
        

        print("🎯 Transkript başarıyla alındı. AI özetleme başlatılıyor...\n")
        QApplication.processEvents()
        # AI ile özetle
        summary = self.ai_core.summarize_with_gemini(transcript_text)

        # ✅ Arayüzde göster

        self.youtube_summary_display.setText(summary)

        print("✅ AI Dekript Sonucu:\n\n" + summary)
        self.hide_progress()

    def get_transcript_from_youtube(self, url: str) -> str:
        """YouTube videosundan transkript alma"""
        try:
            # Video ID'sini çıkar
            video_id = None
            match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
            if match:
                video_id = match.group(1)
            else:
                return "⚠️ Geçerli bir YouTube video bağlantısı giriniz."

            try:
                # Önce altyazı dene
                from youtube_transcript_api import YouTubeTranscriptApi
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['tr', 'en'])
                return " ".join([entry['text'] for entry in transcript])

            except:
                # Altyazı yoksa Whisper kullan
                print("📡 Altyazı bulunamadı, Whisper AI modeliyle dekript ediliyor...")
                QApplication.processEvents()

                from helper_audio import download_audio_temp_from_youtube, transcribe_audio_whisper

                audio_path = download_audio_temp_from_youtube(url)
                if "HATA" in audio_path:
                    return audio_path

                whisper_text = transcribe_audio_whisper(audio_path)

                #Temizlik
                os.remove(audio_path)
                return whisper_text

        except Exception as e:
            return f"❌ Transkript alınamadı: {e}"

    def load_fixed_channel_videos(self):
        """Sabit kanal videolarını yükle"""
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.fixed_channel_url, download=False)

                if info and 'entries' in info:
                    self.channel_video_combo.clear()
                    self.channel_video_map = {}

                    for video in info['entries']:
                        title = video.get('title', 'Başlık bulunamadı')
                        video_id = video.get('id')
                        if video_id:
                            video_url = f"https://www.youtube.com/watch?v={video_id}"
                            self.channel_video_combo.addItem(title)
                            self.channel_video_map[title] = video_url

        except Exception as e:
            print(f"❌ Sabit kanal video yükleme hatası: {e}")

    def show_progress(self,message="İşlem yapılıyor..."):
        """Progress bar göster"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
    def hide_progress(self):
        """Progress bar gizle"""
        self.progress_bar.setVisible(False)

    def clear_search_input(self):
        """Terim arama input alanını temizle"""
        self.term_input.clear() 
        self.term_input.setFocus()

    def clear_search_results(self):
        """Arama sonuçlarını temizle"""
        self.result_display.clear()


    """def open_video_file(self):
        Video dosyası seçme
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Video Dosyaları (*.mp4 *.avi *.mkv *.mov *.wmv)")
        
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.media_player.play()
            print(f"Video yüklendi: {file_path}")"""
   

    ''' def update_button_states(self, state):
        """Oynatma durumuna göre butonları güncelle"""
        if self.media_player.source().isEmpty():
            self.play_button.setEnabled(False)
            self.pause_button.setEnabled(False)
            return

        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setEnabled(False)
            self.pause_button.setEnabled(True)
        else:
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)'''

    def search_term_and_summarize(self):
        user_term = self.term_input.text().strip()
        if not user_term:
            self.result_display.setText("⚠️ Lütfen bir terim girin.")
            return

        self.show_progress("Arama yapılıyor...")
        self.result_display.setText(f"🔍 '{user_term}' için dokümanlarda arama yapılıyor...")
        QApplication.processEvents()

        # AICore üzerinden doğru çağrı
        predicted_title = self.ai_core.find_subject_title_with_gemini(user_term)
        print(f"🎯 Tahmin edilen başlık: {predicted_title}")
        
        titles_to_try = [t.strip() for t in predicted_title.split("\n") if t.strip()]
        print(f"[DEBUG] {len(titles_to_try)} başlık bulundu: {titles_to_try}")

        if "OpenAI konu bulma hatası" in predicted_title:
            self.result_display.append("⚠️ Konu başlığı tahmini sırasında hata oluştu.")
            self.hide_progress()
            return

        self.result_display.append(f"📚 Tahmin edilen başlık: {predicted_title}\n")
        QApplication.processEvents()

        # Arama yap ve sonuçların linklerini al
        result_links = []
        for title in titles_to_try:
            self.result_display.append(f"🔍 '{title}' başlığı için arama yapılıyor...\n")
            QApplication.processEvents()
            links = self.scraper.search_and_get_result_links(title)
            if links:
                result_links.extend([(title, link) for link in links])

        if not result_links:
            self.result_display.append("❌ Bu terimle ilgili bir sonuç bulunamadı.")
            self.hide_progress()
            return

        # Her link için işlem yap
        valid_links = [(title, link) for title, link in result_links if link and "Hata:" not in link]

        if not valid_links:
            self.result_display.append("❌ Geçerli bir sonuç linki bulunamadı.")
            self.hide_progress()
            return

        summaries = []

        for i, (title, link) in enumerate(valid_links[:10]):
            self.result_display.append(f"\n📄 {link} ({title}) sayfası okunuyor...")
            QApplication.processEvents()

            page_content = self.scraper.get_page_content(link)
            print(f"[DEBUG] Sayfa: {link}")
            print(f"[DEBUG] Sayfa içeriği karakter sayısı: {len(page_content) if page_content else 0}")

            if page_content and "Hata:" not in page_content:
                self.result_display.append(f"🤖 Sayfa {i+1} içeriği yapay zekaya özetletiliyor...\n")
                QApplication.processEvents()

                summary = self.ai_core.find_and_summarize(title, page_content, min_chunk_size=30)
                print(f"[DEBUG] AI özet çıktısı:\n{summary}")

                if summary and "Hata:" not in summary and "bulunamadı" not in summary:
                    summaries.append(f"📌 **Sayfa {i+1}** ({link}) - {title}:\n{summary.strip()}\n")
                else:
                    summaries.append(f"📌 **Sayfa {i+1}** ({link}) - {title}: Anlamlı özet üretilemedi.\n")
            else:
                summaries.append(f"📌 **Sayfa {i+1}** ({link}) - {title}: İçerik okunamadı.\n")

        if summaries:
            self.result_display.setText("✅ **ARAMA SONUÇLARI**\n\n" + "\n".join(summaries))
        else:
            self.result_display.setText("❌ Bulunan sayfalardan anlamlı özet üretilemedi.")
        
        self.hide_progress()

    def clear_youtube_summary(self):
        """AI özet kutusunu temizle"""
        self.youtube_summary_display.clear()

    def set_term_and_search(self, term):
        """Seçilen terimi input'a set et ve ara"""
        self.term_input.setText(term)
        self.search_term_and_summarize()

    def handle_text_selection(self, event):
        """Metin seçimi işleme"""
        cursor = self.result_display.textCursor()
        selected_text = cursor.selectedText().strip()
        if selected_text:
            self.set_term_and_search(selected_text)

    def closeEvent(self, event):
        """Uygulama kapatılırken temizlik"""
        print("🛑 Uygulama kapatılıyor...")
        self.scraper.close_driver()
        event.accept()


# --- Uygulamayı Başlatan Ana Kısım ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Modern tema ayarları
    app.setStyle('Fusion')

    window = VideoAssistantApp()
    window.show()
    sys.exit(app.exec())
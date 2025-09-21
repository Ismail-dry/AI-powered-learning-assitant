import sys,os
import psycopg2
from cryptography.fernet import Fernet
from PyQt6.QtCore import Qt, QTimer
# Gerekli QAction ve QIcon sınıfları için içe aktarmalar güncellendi
from PyQt6.QtGui import QPixmap, QIcon, QFont, QColor, QDesktopServices, QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox, QFrame,
                           QGraphicsDropShadowEffect)
from PyQt6.QtCore import QUrl
from test import VideoAssistantApp
import os

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
pixmap_path = os.path.join(base_path, "adeko.png")

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
pixmap_path1 = os.path.join(base_path, "closed-eyes.png")

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
pixmap_path2 = os.path.join(base_path, "eye-close-up.png")

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
pixmap_path3 = os.path.join(base_path, "adeko.ico")


class ClickableLabel(QLabel):
    """Tıklanabilir logo etiketi"""
    def __init__(self, pixmap, url):
        super().__init__()
        self.url = url
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Hover efekti için stil
        self.setStyleSheet("""
            QLabel {
                border-radius: 10px;
                padding: 10px;
                background: transparent;
            }
            QLabel:hover {
                background: rgba(255, 107, 53, 0.1);
                border-radius: 10px;
            }
        """)
    
    def mousePressEvent(self, event):
        """Tıklama olayını yakala"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_website()
    
    def open_website(self):
        """Web sitesini aç"""
        try:
            QDesktopServices.openUrl(QUrl(self.url))
        except Exception as e:
            print(f"Web sitesi açılırken hata: {str(e)}")

class ModernButton(QPushButton):
    """ADEKO temalı modern buton"""
    def __init__(self, text, color="primary"):
        super().__init__(text)
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if color == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF6B35, stop:1 #E55A2B);
                    border: none;
                    border-radius: 15px;
                    color: white;
                    padding: 15px 30px;
                    font-weight: bold;
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FF7B45, stop:1 #FF6B35);
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #E55A2B, stop:1 #D44A21);
                    transform: translateY(0px);
                }
                QPushButton:disabled {
                    background: #CCCCCC;
                    color: #666666;
                }
            """)
        elif color == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #6C757D, stop:1 #5A6268);
                    border: 2px solid #FF6B35;
                    border-radius: 15px;
                    color: #FF6B35;
                    padding: 15px 30px;
                    font-weight: bold;
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    background: transparent;
                }
                QPushButton:hover {
                    background: #FF6B35;
                    color: white;
                    border-color: #FF6B35;
                }
                QPushButton:pressed {
                    background: #E55A2B;
                    border-color: #E55A2B;
                }
            """)


class ModernLineEdit(QLineEdit):
    """ADEKO temalı modern input alanı"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(55)
        self.setFont(QFont("Segoe UI", 12))
        
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E1E8ED;
                border-radius: 15px;
                padding: 15px 25px;
                background: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                color: #2C3E50;
                selection-background-color: #FF6B35;
            }
            QLineEdit:focus {
                border-color: #FF6B35;
                background: rgba(255, 255, 255, 1);
                outline: none;
                box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
            }
            QLineEdit:hover {
                border-color: #FF6B35;
                background: rgba(255, 255, 255, 0.95);
            }
        """)


class ModernCard(QFrame):
    """ADEKO temalı modern kart widget'ı"""
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 25px;
                border: 1px solid rgba(255, 107, 53, 0.1);
                backdrop-filter: blur(10px);
            }
        """)
        
        # Gelişmiş gölge efekti
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(255, 107, 53, 60))
        shadow.setOffset(0, 15)
        self.setGraphicsEffect(shadow)


class AnimatedLabel(QLabel):
    """Animasyonlu başlık"""
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Fade-in animasyonu için timer
        self.opacity_timer = QTimer()
        self.opacity_timer.timeout.connect(self.fade_in)
        self.opacity_value = 0.0
        self.opacity_timer.start(50)
    
    def fade_in(self):
        if self.opacity_value < 1.0:
            self.opacity_value += 0.05
            self.setStyleSheet(f"""
                QLabel {{
                    color: #2C3E50;
                    background: transparent;
                }}
            """)
        else:
            self.opacity_timer.stop()

   

class LoginWindow(QWidget):
    def __init__(self, host='localhost', dbname='Helper_ai_based', 
                 user='postgres', password='123456', port=5432):
        super().__init__()

        # Veritabanı bağlantısı
        try:
            self.conn = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=user,
                password=password,
                port=port
            )
            self.cursor = self.conn.cursor()
            print("✅ Veritabanına bağlantı başarılı.")
        except Exception as e:
            print("❌ Veritabanına bağlanırken hata:", str(e))

        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("🔐 ADEKO AI Video Asistanı - Giriş")
        self.setWindowIcon(QIcon('adeko.ico'))
        
        # YENİ: Şifre görünürlüğü için ikonları yükle
        # Bu dosyaların script ile aynı dizinde olduğundan emin olun
        self.visibility_on_icon = QIcon(pixmap_path2)
        self.visibility_off_icon = QIcon(pixmap_path1)
        
        # ADEKO temalı gradient arkaplan ve YENİ: QLineEdit içindeki ikon butonu için stil
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.3 #764ba2, stop:0.7 #f093fb, stop:1 #f5576c);
            }
            QLineEdit QToolButton {
                background: transparent;
                border: none;
                margin-right: 5px; /* İkon ile metin arasına boşluk ekler */
            }
        """)
        
        self.initUI()
        self.show()

    
    def initUI(self):
        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Ortalama için spacer
        main_layout.addStretch(1)
        
        # Ana container
        container = QHBoxLayout()
        container.addStretch(1)
        
        # Login kartı
        login_card = ModernCard()
        login_card.setFixedSize(480, 680)
        
        card_layout = QVBoxLayout(login_card)
        card_layout.setSpacing(25)
        card_layout.setContentsMargins(45, 45, 45, 45)
        
        # Logo ve başlık
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
       
        card_layout.addLayout(header_layout)
        
        # Form alanları
        form_layout = QVBoxLayout()
        form_layout.setSpacing(17)
        
        # Kullanıcı adı bölümü
        username_layout = QVBoxLayout()
        username_label = QLabel("👤 Kullanıcı Adı")
        username_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        username_label.setStyleSheet("""
            color: #2C3E50; 
            margin-top: 1px;
            font-weight: bold;
        """)
        
        self.username_input = ModernLineEdit("Kullanıcı adınızı girin")
        self.username_input.returnPressed.connect(self.login)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)
        
        # Şifre bölümü
        password_layout = QVBoxLayout()
        password_label = QLabel("🔒 Şifre")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        password_label.setStyleSheet("""
            color: #2C3E50; 
            margin-top: 2px;
            font-weight: bold;
        """)
        
        self.password_input = ModernLineEdit("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.login)
        
        # YENİ: Şifre görünürlüğü için aksiyon (tıklanabilir ikon) oluşturma
        self.toggle_password_action = QAction(self.visibility_off_icon, "Şifreyi Göster/Gizle", self)
        self.toggle_password_action.setCheckable(True) # İkonun durumunu (basılı/değil) saklamasını sağlar
        self.toggle_password_action.toggled.connect(self.on_toggle_password_visibility)
        self.password_input.addAction(self.toggle_password_action, QLineEdit.ActionPosition.TrailingPosition)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)
        
        card_layout.addLayout(form_layout)
        
        # Butonlar
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        
        # Giriş butonu
        self.login_button = ModernButton(" Giriş Yap", "primary")
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)
        
        # Kayıt ol butonu
        self.register_button = ModernButton(" Kayıt Ol", "secondary")
        self.register_button.clicked.connect(self.openRegister)
        button_layout.addWidget(self.register_button)
        
        card_layout.addLayout(button_layout)

    
        logo_pixmap = QPixmap(pixmap_path)
        scaled_pixmap = logo_pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        website_url = "https://www.adeko.com/"  
        
        logo_label = ClickableLabel(scaled_pixmap, website_url)
        card_layout.addWidget(logo_label)

        # Alt bilgi 
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_label = QLabel("ADEKO AI Video Asistanı")
        info_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        info_label.setStyleSheet("""
            color: #FF6B35; 
            margin-top: 1px;
            font-weight: bold;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        version_label = QLabel("v2.0 - Gelişmiş AI Teknolojisi")
        version_label.setFont(QFont("Segoe UI", 9))
        version_label.setStyleSheet("""
            color: #95A5A6; 
            margin-top: 5px;
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_layout.addWidget(info_label)
        info_layout.addWidget(version_label)
        card_layout.addLayout(info_layout)
        
        container.addWidget(login_card)
        container.addStretch(1)
        
        main_layout.addLayout(container)
        main_layout.addStretch(1)
        
        self.setLayout(main_layout)
    
    # YENİ: Şifre görünürlüğünü değiştiren metod
    def on_toggle_password_visibility(self, checked):
        """
        Şifre alanının görünürlüğünü ve ilgili ikonu değiştirir.
        'checked' parametresi QAction'ın 'toggled' sinyalinden otomatik olarak gelir.
        """
        if checked:
            # Aksiyon seçili ise (şifre görünür yapılacaksa)
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_action.setIcon(self.visibility_on_icon)
        else:
            # Aksiyon seçili değilse (şifre gizlenecekse)
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_action.setIcon(self.visibility_off_icon)

    def pop_message(self, text, title="Bilgi", msg_type="info"):
        """ADEKO temalı modern mesaj kutusu"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setWindowIcon(QIcon('adeko.ico'))
        
        # Mesaj tipine göre ikon
        if msg_type == "success":
            msg.setIcon(QMessageBox.Icon.Information)
        elif msg_type == "error":
            msg.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "warning":
            msg.setIcon(QMessageBox.Icon.Warning)
        else:
            msg.setIcon(QMessageBox.Icon.Information)
        
        # ADEKO temalı stil
        msg.setStyleSheet("""
            QMessageBox {
                background: white;
                border-radius: 15px;
                font-family: 'Segoe UI';
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FF6B35, stop:1 #E55A2B);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 12px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FF7B45, stop:1 #FF6B35);
            }
            QMessageBox QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E55A2B, stop:1 #D44A21);
            }
        """)
        
        msg.exec()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            self.pop_message("⚠️ Lütfen kullanıcı adı ve şifre girin.", "Eksik Bilgi", "warning")
            return
        try:
            # Buton animasyonu
            self.login_button.setEnabled(False)
            self.login_button.setText("🔄 Giriş Yapılıyor...")
            self.login_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #CCCCCC, stop:1 #AAAAAA);
                    border: none;
                    border-radius: 15px;
                    color: #666666;
                    padding: 15px 30px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            QApplication.processEvents()
            self.cursor.execute("SELECT Username, Password, Key_F FROM Users")
            users = self.cursor.fetchall()
            for user_row in users:
                enc_username_db, enc_password_db, key_db = user_row
                cipher_db = Fernet(key_db.encode())
                dec_username_db = cipher_db.decrypt(enc_username_db.encode()).decode()
                dec_password_db = cipher_db.decrypt(enc_password_db.encode()).decode()

                if username == dec_username_db and password == dec_password_db:
                    self.pop_message(f"🎉 Hoş geldiniz {username}!\nADEKO AI Video Asistanına yönlendiriliyorsunuz.", "Giriş Başarılı", "success")
                    
                    # Ana uygulamayı aç
                    self.main_window = VideoAssistantApp(username=username)
                    self.main_window.show()
                    self.close()
                    return
            # Giriş başarısız - butonu eski haline getir
            self.reset_login_button()
            self.pop_message("❌ Kullanıcı adı veya şifre hatalı.\nLütfen bilgilerinizi kontrol edin.", "Giriş Hatası", "error")

        except Exception as e:
            self.reset_login_button()
            self.pop_message(f"❌ Giriş hatası: {str(e)}", "Sistem Hatası", "error")

    def reset_login_button(self):
        """Giriş butonunu eski haline getir"""
        self.login_button.setEnabled(True)
        self.login_button.setText(" Giriş Yap")
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FF6B35, stop:1 #E55A2B);
                border: none;
                border-radius: 15px;
                color: white;
                padding: 15px 30px;
                font-weight: bold;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FF7B45, stop:1 #FF6B35);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E55A2B, stop:1 #D44A21);
                transform: translateY(0px);
            }
        """)

    def openRegister(self):
        """Kayıt penceresini aç"""
        try:
            from RegisterForUsers import RegisterWindow
            self.register_window = RegisterWindow()
            self.register_window.show()
            self.close()
        except ImportError:
            self.pop_message("❌ Kayıt modülü bulunamadı.", "Modül Hatası", "error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Modern ve şık tema
    app.setStyle('Fusion')
    
    # Uygulama ikonu
    app.setWindowIcon(QIcon('adeko.ico'))
    
    window = LoginWindow()
    sys.exit(app.exec())
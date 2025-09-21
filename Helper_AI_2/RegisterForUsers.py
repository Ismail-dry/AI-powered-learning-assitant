import sys,os
import datetime
import psycopg2
from cryptography.fernet import Fernet
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QGroupBox, QFrame,
    QProgressBar, QSplitter
)

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
pixmap_path = os.path.join(base_path, "adeko.ico")

class ModernButton(QPushButton):
    """Modern görünümlü özelleştirilmiş buton"""
    def __init__(self, text, color="primary"):
        super().__init__(text)
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        
        if color == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4A90E2, stop:1 #357ABD);
                    border: none;
                    border-radius: 10px;
                    color: white;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5BA0F2, stop:1 #4A90E2);
                    transform: translateY(-2px);
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
                    border-radius: 10px;
                    color: white;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #6CC86C, stop:1 #5CB85C);
                    transform: translateY(-2px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #449D44, stop:1 #398439);
                }
            """)
        elif color == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #6C757D, stop:1 #495057);
                    border: none;
                    border-radius: 10px;
                    color: white;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #7C848D, stop:1 #6C757D);
                    transform: translateY(-2px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #495057, stop:1 #343A40);
                }
            """)


class ModernLineEdit(QLineEdit):
    """Modern görünümlü input alanı"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 11))
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E1E8ED;
                border-radius: 10px;
                padding: 12px 16px;
                background: white;
                font-size: 14px;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
                background: #F8FBFF;
                box-shadow: 0 0 10px rgba(74, 144, 226, 0.3);
            }
            QLineEdit:hover {
                border-color: #4A90E2;
                background: #FAFBFC;
            }
        """)


class ModernGroupBox(QGroupBox):
    """Modern görünümlü grup kutusu"""
    def __init__(self, title):
        super().__init__(title)
        self.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #2C3E50;
                border: 3px solid #E1E8ED;
                border-radius: 15px;
                margin-top: 15px;
                padding-top: 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F8F9FA);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
                background: white;
                border-radius: 8px;
            }
        """)


class RegisterWindow(QWidget):
    def __init__(self, host='localhost', dbname='Helper_ai_based', user='postgres', password='123456', port=5432):
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
            print("❌ Veritabanı bağlantı hatası:", str(e))

        # Pencere ayarları
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("🔐 Kullanıcı Kaydı - Modern Interface")
        self.setWindowIcon(QIcon(pixmap_path))
        self.setMinimumSize(500, 600)
        
        # Modern tema ayarları
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.3 #764ba2, stop:0.7 #f093fb, stop:1 #f5576c);
            }
        """)
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

        self.initUI()
        self.show()

    def initUI(self):
        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        
        # Başlık
        title_label = QLabel(" Yeni Hesap Oluştur")
        
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                background: none;
                padding: 20px;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Kullanıcı bilgileri grubu
        user_info_group = ModernGroupBox("👤 Kişisel Bilgiler")
        user_info_layout = QVBoxLayout(user_info_group)
        user_info_layout.setSpacing(15)

        # Ad ve Soyad (yan yana)
        name_layout = QHBoxLayout()
        self.name_input = ModernLineEdit("Adınız")
        self.surname_input = ModernLineEdit("Soyadınız")
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.surname_input)

        # Kullanıcı adı ve Email
        self.username_input = ModernLineEdit("Kullanıcı Adı")
        self.email_input = ModernLineEdit("E-posta Adresi")

        user_info_layout.addLayout(name_layout)
        user_info_layout.addWidget(self.username_input)
        user_info_layout.addWidget(self.email_input)

        # Şifre bilgileri grubu
        password_group = ModernGroupBox("🔒 Güvenlik Bilgileri")
        password_layout = QVBoxLayout(password_group)
        password_layout.setSpacing(15)

        # Şifre alanları
        self.password_input = ModernLineEdit("Şifre")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.confirm_input = ModernLineEdit("Şifreyi Tekrarla")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.confirm_input)

        # Şifre güvenlik ipucu
        security_note = QLabel("💡 Şifreniz en az 6 karakter olmalıdır")
        security_note.setFont(QFont("Segoe UI", 9))
        security_note.setStyleSheet("""
            QLabel {
                color: #6C757D;
                background: none;
                padding: 5px;
                font-style: italic;
            }
        """)
        password_layout.addWidget(security_note)

        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.register_btn = ModernButton("✅ Kayıt Ol", "success")
        self.cancel_btn = ModernButton("❌ İptal", "secondary")
        
        # Buton boyutları
        self.register_btn.setMinimumWidth(150)
        self.cancel_btn.setMinimumWidth(150)
        
        button_layout.addStretch()
        button_layout.addWidget(self.register_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()

        # Ana layout'a widget'ları ekle
        main_layout.addWidget(title_label)
        main_layout.addWidget(user_info_group)
        main_layout.addWidget(password_group)
        main_layout.addStretch()
        main_layout.addWidget(self.progress_bar)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Sinyal bağlantıları
        self.register_btn.clicked.connect(self.register)
        self.cancel_btn.clicked.connect(self.backToLogin)
        
        # Enter tuşu ile kayıt
        self.confirm_input.returnPressed.connect(self.register)

    def show_progress(self, message="İşlem yapılıyor..."):
        """Progress bar göster"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.register_btn.setEnabled(False)
        
    def hide_progress(self):
        """Progress bar gizle"""
        self.progress_bar.setVisible(False)
        self.register_btn.setEnabled(True)

    def pop_message(self, text, msg_type="info"):
        """Modern mesaj kutusu"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowIcon(QIcon('adeko.ico'))
        
        if msg_type == "success":
            msg.setWindowTitle("✅ Başarılı")
            msg.setIcon(QMessageBox.Icon.Information)
        elif msg_type == "error":
            msg.setWindowTitle("❌ Hata")
            msg.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "warning":
            msg.setWindowTitle("⚠️ Uyarı")
            msg.setIcon(QMessageBox.Icon.Warning)
        else:
            msg.setWindowTitle("ℹ️ Bilgi")
            msg.setIcon(QMessageBox.Icon.Information)
        
        # Modern stil
        msg.setStyleSheet("""
            QMessageBox {
                background: white;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QMessageBox QPushButton {
                background: #4A90E2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: #5BA0F2;
            }
        """)
        
        msg.exec()

    def register(self):
        # Input değerlerini al
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        # Validation
        if not all([name, surname, username, email, password, confirm]):
            self.pop_message("Lütfen tüm alanları doldurun.", "warning")
            return

        if len(password) < 6:
            self.pop_message("Şifre en az 6 karakter olmalıdır.", "warning")
            return

        if password != confirm:
            self.pop_message("Şifreler eşleşmiyor.", "error")
            return

        # Email format kontrolü (basit)
        if "@" not in email or "." not in email:
            self.pop_message("Geçerli bir e-posta adresi girin.", "warning")
            return

        # İşlem başlat
        self.show_progress("Kayıt işlemi yapılıyor...")
        QApplication.processEvents()
        try:
            # Şifreleme için key oluştur
            key = Fernet.generate_key()
            cipher = Fernet(key)
            enc_username = cipher.encrypt(username.encode()).decode()
            enc_password = cipher.encrypt(password.encode()).decode()
            # Kullanıcı mevcut mu kontrolü
            self.cursor.execute("SELECT Username, Key_F FROM Users")
            users = self.cursor.fetchall()
            for user_row in users:
                enc_username_db, key_db = user_row
                cipher_db = Fernet(key_db.encode())
                dec_username_db = cipher_db.decrypt(enc_username_db.encode()).decode()
                if username == dec_username_db:
                    self.hide_progress()
                    self.pop_message("Bu kullanıcı adı zaten kullanımda.", "error")
                    return
            # INSERT
            insert_query = """
                INSERT INTO Users(Name, Surname, Username, Password, Email, Key_F, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (
                name,
                surname,
                enc_username,
                enc_password,
                email,
                key.decode(),
                datetime.datetime.now()
            ))
            self.conn.commit()
            self.hide_progress()
            self.pop_message("Kayıt işlemi başarıyla tamamlandı! 🎉", "success")
            self.backToLogin()
            
        except Exception as e:
            self.conn.rollback()
            self.hide_progress()
            self.pop_message(f"Kayıt işlemi başarısız: {str(e)}", "error")

    def backToLogin(self):
        """Giriş ekranına dön"""
        try:
            from UserLogin import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
        except ImportError:
            print("⚠️ UserLogin modülü bulunamadı")
            self.close()

    def closeEvent(self, event):
        """Pencere kapatılırken veritabanı bağlantısını kapat"""
        if hasattr(self, 'conn'):
            self.conn.close()
            print("🔐 Veritabanı bağlantısı kapatıldı.")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Modern tema ayarları
    app.setStyle('Fusion')
    
    window = RegisterWindow()
    sys.exit(app.exec())
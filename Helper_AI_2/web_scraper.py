# web_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time


class WebScraper:
    def __init__(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--log-level=3")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--headless")  # Şimdilik kapalı
                
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            print("WebDriver başarıyla başlatıldı.")
        except Exception as e:
            print(f"Hata: WebDriver başlatılamadı. Hata mesajı: {e}")
            self.driver = None

    def search_and_get_result_links(self, term: str) -> list[str]:
        if not self.driver:
            return ["Hata: WebDriver düzgün başlatılamadı."]

        try:
            self.driver.get("https://doc.clickup.com/d/h/q8maf-301/30dc66d72028a09")

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search pages']"))
            )
            search_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search pages']")
            search_input.clear()
            search_input.send_keys(term)
            search_input.send_keys(Keys.RETURN)
            print(f"'{term}' için arama yapılıyor...")

            # Yeni yapıya göre sayfa bağlantılarını bul
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-test='dashboard-doc-item']"))
            )

            time.sleep(6)  # içerik için küçük bekleme

            items = self.driver.find_elements(By.CSS_SELECTOR, "div[data-test='dashboard-doc-item']")
            links = []
            for item in items:
                doc_id = item.get_attribute("id")  # örn: doc-page-q8maf-1234
                if doc_id and doc_id.startswith("doc-page-"):
                    page_id = doc_id.replace("doc-page-", "")
                    full_link = f"https://doc.clickup.com/d/h/q8maf-301/30dc66d72028a09/{page_id}"
                    links.append(full_link)

            print(f"✔️ {len(links)} adet sonuç linki bulundu.")
            return links

        except Exception as e:
            return [f"Hata: Arama işlemi sırasında sorun oluştu: {e}"]

    def get_page_content(self, url: str) -> str:
        if not self.driver:
            return "Hata: WebDriver başlatılamadı."

        try:
            self.driver.get(url)

        # Sayfa ana içerik elementini bekle (30 saniyeye kadar bekle)
            WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor.ql-editor-readonly"))
            )


        # Scroll ederek içeriği yüklemeye çalış
            for attempt in range(10):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                content_element = self.driver.find_element(By.CSS_SELECTOR, "div.ql-editor.ql-editor-readonly")

                content = content_element.text.strip()

                print(f"[{attempt+1}/10] Scroll sonrası içerik karakter sayısı: {len(content)}")

                if content and len(content) > 30:  # Daha toleranslı olduk
                    print(f"✔️ '{url}' sayfasının içeriği başarıyla alındı ({len(content)} karakter).")
                        
                    return content

            print(f"❌ '{url}' içeriği hala yetersiz veya boş.")
            return "Hata: Sayfa içeriği boş görünüyor."

        except TimeoutException:
            print(f"⏱️ Timeout: '{url}' sayfası zaman aşımına uğradı. Tekrar denenebilir.")
            return "Hata: Sayfa içeriği yüklenemedi."

        except Exception as e:
            return f"Sayfa içeriği alınırken hata oluştu: {e}"


    def close_driver(self):
          if self.driver:
           self.driver.quit()

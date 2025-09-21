from pypdf import PdfReader, PdfWriter
import os

# PDF klasör yolu
pdf_klasoru = r"C:\Users\kralm\OneDrive\Masaüstü\StajDefter"  # BURAYI GÜNCELLE

# Çıktı PDF dosyası
output_path = os.path.join(pdf_klasoru, "Staj-Defteri.pdf")

# PDFWriter nesnesi
writer = PdfWriter()

# defter1.pdf ~ defter29.pdf
for i in range(1, 30):
    dosya_adi = f"defter{i}.pdf"
    tam_yol = os.path.join(pdf_klasoru, dosya_adi)

    if os.path.exists(tam_yol):
        reader = PdfReader(tam_yol)
        for sayfa in reader.pages:
            writer.add_page(sayfa)
    else:
        print(f"❌ Dosya bulunamadı: {tam_yol}")

# Son olarak dosyayı yaz
with open(output_path, "wb") as cikti_dosyasi:
    writer.write(cikti_dosyasi)

print("✅ PDF dosyaları başarıyla birleştirildi!")

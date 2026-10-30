# 🚀 SysPulse Ultimate

SysPulse Ultimate, Windows işletim sistemleri için geliştirilmiş, sistem kaynaklarını canlı izleme, donanım bilgilerini görüntüleme, optimizasyon ve bakım işlemlerini tek bir merkezden yürütme imkanı sunan modern bir masaüstü uygulamasıdır.

✨ Öne Çıkan Özellikler

📊 Canlı Sistem & Ağ Takibi: Anlık CPU, RAM, Disk kullanımı ve canlı ağ indirme/yükleme hızları.

🎮 Otomatik Ekran Kartı (GPU) Algılama: Sistemdeki harici veya dahili grafik birimlerini otomatik tanımlar ve markaya özel logolarla gösterir.

⚡ Yerleşik İnternet Hız Testi: Harici kütüphanelere bağımlı kalmadan Cloudflare altyapısı üzerinden hızlı Ping ve İndirme testi.

🧹 Tek Tıkla Sistem Bakımı:

Geçici dosyaları (Temp) temizleme

DNS önbelleğini sıfırlama (FlushDNS)

Nihai Performans Modunu aktif etme

Sistem dosyası onarımı (sfc /scannow)

🛠️ Hızlı Windows Araçları: Görev Yöneticisi, Aygıt Yöneticisi, Denetim Masası ve DxDiag'a tek tıkla erişim.

🌐 Çoklu Dil Desteği: Türkçe, English, Deutsch ve Español dil seçenekleri.

📌 Masaüstü Widget Modu: Ekranda az yer kaplayan canlı takip pencereli widget desteği.

📄 Raporlama: Sistem özetini .txt formatında dışarı aktarma.

📥 İndirme ve Kullanım (Son Kullanıcılar İçin)

Herhangi bir Python kurulumu veya ek dosya gerektirmeden çalıştırmak için:

Sağ taraftaki Releases bölümüne tıklayın.

SysPulseUltimate.exe dosyasını indirin ve çalıştırın.

💻 Geliştiriciler İçin Kurulum

Projeyi kaynak koddan çalıştırmak veya geliştirmek isterseniz:

Gereksinimler

Python 3.10 veya üzeri

Adımlar

Depoyu klonlayın:

```bash
git clone https://github.com/benreattofficial/SysPulseUltimate.git
cd SysPulseUltimate
```

Gerekli Python paketlerini yükleyin:

```bash
pip install customtkinter psutil pillow
```

Uygulamayı çalıştırın:

```bash
python app.py
```

📦 Tekli .exe Olarak Derleme (PyInstaller)

Uygulamayı tüm medya dosyaları ve dil seçenekleriyle birlikte tek bir .exe haline getirmek için:

```bash
python -m PyInstaller --noconsole --onefile --icon="icon.ico" --name "SysPulseUltimate" --add-data "languages.json;." --add-data "*.png;." app.py
```

📜 Lisans

Bu proje GPL-3.0 lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakabilirsiniz.

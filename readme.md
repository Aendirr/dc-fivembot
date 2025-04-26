# Discord - FiveM Yönetim Botu

Bu proje, Discord üzerinden FiveM sunucularını yönetmek için geliştirilmiş tam teşekküllü bir bot sistemidir.

---

## Özellikler
- Sunucu bilgisi gösterme
- Sunucu restart komutu
- Oyuncu envanteri ve aktiflik kontrolü (SQL üzerinden)
- Discord üzerinden ban, kick, warn yönetimi
- Etkinlik oluşturma ve iptal etme (FiveM broadcast destekli)
- Discord kullanıcılarını banlama, atma ve sohbet temizleme
- Süreli cezalandırma (otomatik rol kaldırma, ceza loglama)
- Slash komutları %100 destekli

---

## Kurulum

1. Bu projeyi klonlayın:
    ```bash
    git clone https://github.com/senin-kullanici-adi/fivem-discord-admin-bot.git
    cd fivem-discord-admin-bot
    ```

2. Gerekli Python kütüphanelerini kurun:
    ```bash
    pip install -r requirements.txt
    ```

3. `bot/config.py` dosyasını düzenleyin:
    ```python
    TOKEN = "Botunuzun Tokeni"
    GUILD_ID = 123456789012345678
    BACKEND_API_URL = "http://127.0.0.1:8000"
    BACKEND_API_TOKEN = "api_token"

    CEZA_LOG_KANAL_ID = 111111111111
    CEZA_ROLLERI = {
        "2gün": 987654321123456,
        "3gün": 987654321123457,
        "1hafta": 987654321123458,
        "1ay": 987654321123459,
        "perma": 987654321123460
    }
    ```

4. `backend/config/config.py` dosyasını düzenleyin:
    ```python
    BACKEND_API_TOKEN = "api_token"
    
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "essentialmode"
    ```

5. Botu başlatın:
    ```bash
    python bot/main.py
    ```

6. Backend API'yi başlatın:
    ```bash
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```

---

## Slash Komutlar

| Komut | Açıklama |
|:---|:---|
| `/ip` | Sunucu bağlantı linki (butonlu) |
| `/sunucu` | Sunucu açıklaması gönderir |
| `/admin` | Aktif adminleri listeler |
| `/sunucures` | Sunucuyu restart eder |
| `/kullanıcı` | Oyuncu aktiflik süresini gösterir |
| `/envanter` | Oyuncu envanterini listeler |
| `/item` | Kullanıcıya item verir |
| `/itemsil` | Kullanıcıdan item siler |
| `/banla`, `/kick`, `/warn` | Oyuncu yönetim komutları |
| `/event`, `/eventiptal` | Event oluşturma ve iptali |
| `/dcbanla`, `/dckick`, `/chatclear` | Discord içi moderasyon |
| `/punish` | Süreli rol/ceza verme (otomatik kaldırma) |

---

## Teknik Bilgiler

- Discord.py ve FastAPI kullanılarak geliştirilmiştir.
- SQL işlemleri pymysql üzerinden yapılır (XAMPP destekli).
- FiveM sunucusuna HTTP tabanlı API ile veri gönderimi yapılır.
- Authorization sistemi `Bearer` token bazlıdır.
- Modüler dosya yapısı sayesinde geliştirilmeye açıktır.

---

## Lisans

MIT Lisansı © Aendirr Studios

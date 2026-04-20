import feedparser
import openai
import os
import re

# Ayarlar
RSS_URL = "https://www.aa.com.tr/tr/rss/default?cat=guncel"
openai.api_key = os.getenv("OPENAI_API_KEY")

def haberi_ozgunlestir(baslik, icerik):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen profesyonel bir haber editörüsün. Haberi ilgi çekici, kısa ve SEO uyumlu bir özet olarak yeniden yaz. Sadece düz metin ver."},
                {"role": "user", "content": f"Başlık: {baslik}\n\nHaber: {icerik}"}
            ]
        )
        return response.choices[0].message.content
    except:
        return icerik[:200] + "..."

def haberleri_islet():
    feed = feedparser.parse(RSS_URL)
    
    html_content = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Haber Gündemi - Son Dakika</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f0f2f5; margin: 0; padding: 0; color: #1c1e21; }
            header { background-color: #e74c3c; color: white; padding: 30px 20px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            .container { max-width: 1200px; margin: 30px auto; padding: 0 15px; }
            .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
            .card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s; display: flex; flex-direction: column; border: 1px solid #ddd; }
            .card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.12); }
            .card-image-container { position: relative; width: 100%; height: 200px; background: #dfe3e8; display: flex; align-items: center; justify-content: center; overflow: hidden; }
            .card-image { width: 100%; height: 100%; object-fit: cover; }
            .no-image-text { color: #888; font-weight: bold; font-size: 14px; text-transform: uppercase; }
            .card-content { padding: 20px; flex-grow: 1; }
            h1 { margin: 0; font-size: 32px; letter-spacing: -1px; }
            h2 { font-size: 19px; color: #1c1e21; margin: 0 0 12px 0; line-height: 1.4; font-weight: 700; }
            p { font-size: 15px; line-height: 1.6; color: #4b4f56; margin: 0; }
            .badge { background: #e74c3c; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 700; position: absolute; top: 15px; left: 15px; z-index: 10; }
            .footer { text-align: center; padding: 40px; color: #606770; font-size: 14px; border-top: 1px solid #ddd; background: white; margin-top: 50px; }
            .nav-links { margin-top: 15px; }
            .nav-links a { color: rgba(255,255,255,0.9); text-decoration: none; margin: 0 12px; font-weight: 400; font-size: 14px; border-bottom: 1px solid transparent; }
            .nav-links a:hover { border-bottom: 1px solid white; }
        </style>
    </head>
    <body>
        <header>
            <h1>HABER GÜNDEMİ</h1>
            <div class="nav-links">
                <a href="/">Anasayfa</a>
                <a href="/hakkimizda.html">Hakkımızda</a>
                <a href="/gizlilik.html">Gizlilik Politikası</a>
            </div>
        </header>
        <div class="container">
            <div class="news-grid">
    """

    for entry in feed.entries[:12]:
        ozgun_icerik = haberi_ozgunlestir(entry.title, entry.summary)
        
        # Resim çekme mantığını güçlendirdik
        image_url = ""
        # 1. Deneme: Media Content
        if 'media_content' in entry and len(entry.media_content) > 0:
            image_url = entry.media_content[0]['url']
        # 2. Deneme: Summary içindeki img tag'ini ara (Regex ile)
        if not image_url:
            img_match = re.search(r'<img [^>]*src="([^"]+)"', entry.summary)
            if img_match:
                image_url = img_match.group(1)
        
        # Kart yapısı
        html_content += f"""
                <div class="card">
                    <div class="card-image-container">
                        <span class="badge">SON DAKİKA</span>
                        """
        if image_url:
            html_content += f'<img src="{image_url}" alt="Haber" class="card-image" onerror="this.parentElement.innerHTML=\'<span class=\\\'no-image-text\\\'>HABER GÜNDEMİ</span>\'">'
        else:
            html_content += '<span class="no-image-text">HABER GÜNDEMİ</span>'
            
        html_content += f"""
                    </div>
                    <div class="card-content">
                        <h2>{entry.title}</h2>
                        <p>{ozgun_icerik}</p>
                    </div>
                </div>
        """

    html_content += """
            </div>
        </div>
        <div class="footer">
            <p>&copy; 2026 Haber Gündemi. Yapay zeka ile otomatik güncellenmektedir.</p>
        </div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    haberleri_islet()

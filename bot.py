import feedparser
import openai
import os

# Ayarlar
RSS_URL = "https://www.aa.com.tr/tr/rss/default?cat=guncel"
openai.api_key = os.getenv("OPENAI_API_KEY")

def haberi_ozgunlestir(baslik, icerik):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen profesyonel bir haber editörüsün. Haberi ilgi çekici, kısa ve SEO uyumlu bir özet olarak yeniden yaz. HTML tagları kullanma, sadece düz metin ver."},
                {"role": "user", "content": f"Başlık: {baslik}\n\nHaber: {icerik}"}
            ]
        )
        return response.choices[0].message.content
    except:
        return icerik[:200] + "..."

def haberleri_islet():
    feed = feedparser.parse(RSS_URL)
    
    # CSS ve Tasarım Kodları
    html_content = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Haber Gündemi - Son Dakika</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; color: #333; }
            header { background-color: #e74c3c; color: white; padding: 20px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .container { max-width: 1000px; margin: 20px auto; padding: 10px; }
            .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.3s; }
            .card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
            h1 { margin: 0; font-size: 24px; }
            h2 { font-size: 18px; color: #2c3e50; margin-top: 0; }
            p { font-size: 14px; line-height: 1.6; color: #7f8c8d; }
            .footer { text-align: center; padding: 20px; font-size: 12px; color: #bdc3c7; }
            .badge { background: #e74c3c; color: white; padding: 3px 8px; border-radius: 4px; font-size: 10px; text-transform: uppercase; margin-bottom: 10px; display: inline-block; }
        </style>
    </head>
    <body>
        <header>
            <h1>HABER GÜNDEMİ</h1>
            <p style="color: white; margin-top: 5px;">Yapay Zeka Tarafından Anlık Güncellenir</p>
        </header>
        <div class="container">
            <div class="news-grid">
    """
    
    for entry in feed.entries[:9]: # Son 9 haberi çekelim (3x3 düzeni için)
        ozgun_icerik = haberi_ozgunlestir(entry.title, entry.summary)
        html_content += f"""
                <div class="card">
                    <span class="badge">SON DAKİKA</span>
                    <h2>{entry.title}</h2>
                    <p>{ozgun_icerik}</p>
                </div>
        """
        
    html_content += """
            </div>
        </div>
        <div class="footer">
            <p>&copy; 2026 Haber Gündemi - Tüm Hakları Saklıdır.</p>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    haberleri_islet()

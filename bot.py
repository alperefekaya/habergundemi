import feedparser
import openai
import os
import requests

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
    
    # CSS ve Tasarım Kodları (Modern Grid)
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
            .container { max-width: 1200px; margin: 20px auto; padding: 10px; }
            .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px; }
            .card { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.3s; display: flex; flex-direction: column; }
            .card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
            .card-image { width: 100%; height: 200px; object-fit: cover; background-color: #ddd; }
            .card-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }
            h1 { margin: 0; font-size: 28px; }
            h2 { font-size: 20px; color: #2c3e50; margin-top: 0; margin-bottom: 10px; line-height: 1.3; }
            p { font-size: 14px; line-height: 1.6; color: #7f8c8d; margin-bottom: 15px; flex-grow: 1; }
            .footer { text-align: center; padding: 30px; font-size: 12px; color: #bdc3c7; background-color: #fff; margin-top: 30px;}
            .badge { background: #e74c3c; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; text-transform: uppercase; display: inline-block; margin-bottom: 10px; }
            .yasal-linkler { margin-top: 10px; }
            .yasal-linkler a { color: white; text-decoration: none; margin: 0 10px; font-size: 14px; }
        </style>
    </head>
    <body>
        <header>
            <h1>HABER GÜNDEMİ</h1>
            <p style="color: white; margin-top: 5px; opacity: 0.8;">Yapay Zeka Destekli Son Dakika Haberleri</p>
            <div class="yasal-linkler">
                <a href="/hakkimizda.html">Hakkımızda</a> | 
                <a href="/gizlilik.html">Gizlilik Politikası</a>
            </div>
        </header>
        <div class="container">
            <div class="news-grid">
    """
    
    for entry in feed.entries[:12]: # 12 haber çekelim, jilet gibi dursun.
        ozgun_icerik = haberi_ozgunlestir(entry.title, entry.summary)
        
        # AA'nın RSS'inden fotoğraf çekmeye çalışalım
        # Bazen 'links' içinde, bazen 'media_content' içinde olur.
        image_url = "https://via.placeholder.com/400x225.png?text=Haber+Gundemi" # Varsayılan resim
        
        try:
            if 'media_content' in entry:
                image_url = entry.media_content[0]['url']
            elif 'links' in entry:
                for link in entry.links:
                    if 'image' in link.type:
                        image_url = link.href
                        break
        except:
            pass # Hata olursa varsayılan resim kalsın.

        html_content += f"""
                <div class="card">
                    <img src="{image_url}" alt="{entry.title}" class="card-image" onerror="this.src='https://via.placeholder.com/400x225.png?text=Haber+Gundemi'">
                    <div class="card-content">
                        <span class="badge">GÜNCEL</span>
                        <h2>{entry.title}</h2>
                        <p>{ozgun_icerik}</p>
                    </div>
                </div>
        """
        
    html_content += """
            </div>
        </div>
        <div class="footer">
            <p>&copy; 2026 Haber Gündemi - Tüm Hakları Saklıdır.</p>
            <p>Bu site yapay zeka teknolojileri kullanılarak otomatik olarak güncellenmektedir.</p>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    haberleri_islet()

import feedparser
import openai
import os
import re

# Ayarlar
RSS_URL = "https://www.aa.com.tr/tr/rss/default?cat=guncel"
openai.api_key = os.getenv("OPENAI_API_KEY")

def haberi_ozgunlestir(baslik, icerik):
    try:
        # OpenAI 0.28 sürümü için uyumlu kod
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen profesyonel bir haber editörüsün. Haberi kısa, SEO uyumlu ve ilgi çekici bir özet olarak yeniden yaz."},
                {"role": "user", "content": f"Başlık: {baslik}\n\nHaber: {icerik}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Hatası: {e}")
        return icerik[:200] + "..."

def haberleri_islet():
    feed = feedparser.parse(RSS_URL)
    
    # Eğer haber çekilemezse boş kalmasın diye kontrol
    if not feed.entries:
        print("RSS kaynağından haber çekilemedi!")
        return

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
            header { background-color: #e74c3c; color: white; padding: 25px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .container { max-width: 1100px; margin: 20px auto; padding: 15px; }
            .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
            .card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: flex; flex-direction: column; }
            .card-img { width: 100%; height: 180px; object-fit: cover; background: #ddd; border-bottom: 1px solid #eee; }
            .card-body { padding: 20px; }
            h1 { margin: 0; font-size: 26px; }
            h2 { font-size: 18px; margin: 0 0 10px 0; color: #2c3e50; line-height: 1.4; }
            p { font-size: 14px; color: #7f8c8d; line-height: 1.6; margin: 0; }
            .nav { margin-top: 10px; }
            .nav a { color: white; text-decoration: none; margin: 0 10px; font-size: 13px; opacity: 0.9; }
        </style>
    </head>
    <body>
        <header>
            <h1>HABER GÜNDEMİ</h1>
            <div class="nav"><a href="/hakkimizda.html">Hakkımızda</a> | <a href="/gizlilik.html">Gizlilik</a></div>
        </header>
        <div class="container">
            <div class="news-grid">
    """

    for entry in feed.entries[:12]:
        ozgun = haberi_ozgunlestir(entry.title, entry.summary)
        
        # Resim yakalama (Daha basit ve sağlam yol)
        img_url = "https://via.placeholder.com/400x225.png?text=Haber+Gündemi"
        if 'media_content' in entry:
            img_url = entry.media_content[0]['url']
        elif 'links' in entry:
            for l in entry.links:
                if 'image' in l.get('type', ''):
                    img_url = l.href

        html_content += f"""
                <div class="card">
                    <img src="{img_url}" class="card-img" alt="Haber">
                    <div class="card-body">
                        <h2>{entry.title}</h2>
                        <p>{ozgun}</p>
                    </div>
                </div>
        """

    html_content += "</div></div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    haberleri_islet()

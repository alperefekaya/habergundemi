import feedparser
import openai
import os

# Ayarlar
RSS_URL = "https://www.aa.com.tr/tr/rss/default?cat=guncel"
openai.api_key = os.getenv("OPENAI_API_KEY")

def haberi_ozgunlestir(baslik, icerik):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # Daha ucuz ve hızlıdır
            messages=[
                {"role": "system", "content": "Sen profesyonel bir haber editörüsün. Sana verilen haberi anlamını bozmadan, tamamen farklı cümlelerle, ilgi çekici ve SEO uyumlu şekilde yeniden yaz."},
                {"role": "user", "content": f"Başlık: {baslik}\n\nHaber: {icerik}"}
            ]
        )
        return response.choices[0].message.content
    except:
        return baslik # Hata olursa orijinal başlığı bırak

def haberleri_islet():
    feed = feedparser.parse(RSS_URL)
    html_content = "<html><head><meta charset='utf-8'><title>Haber Gündemi</title></head><body>"
    html_content += "<h1>Yapay Zeka Destekli Son Dakika Haberleri</h1><ul>"
    
    for entry in feed.entries[:5]: # Şimdilik 5 haber alalım (kredi tasarrufu)
        ozgun_haber = haberi_ozgunlestir(entry.title, entry.summary)
        html_content += f"<li><h3>{entry.title}</h3><p>{ozgun_haber}</p><hr></li>"
        
    html_content += "</ul></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    haberleri_islet()

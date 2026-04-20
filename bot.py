import feedparser

# Haber kaynağımız (Örnek: AA Güncel)
RSS_URL = "https://www.aa.com.tr/tr/rss/default?cat=guncel"

def haberleri_cek():
    feed = feedparser.parse(RSS_URL)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>Haber Gündemi</title></head><body>")
        f.write("<h1>Son Dakika Haberleri</h1><ul>")
        
        for entry in feed.entries[:10]: # Son 10 haberi al
            f.write(f"<li><a href='{entry.link}'>{entry.title}</a></li>")
            
        f.write("</ul></body></html>")

if __name__ == "__main__":
    haberleri_cek()

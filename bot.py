import os
import random
import requests
import feedparser
import urllib.parse

BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss/"
]

def get_latest_news():
    all_entries = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = entry.get('title', '')
                link = entry.get('link', '')
                source = feed.feed.get('title', 'Crypto News')
                if title and len(title) > 20:
                    all_entries.append({
                        'title': title,
                        'link': link,
                        'source': source
                    })
        except:
            pass
    random.shuffle(all_entries)
    return all_entries[0] if all_entries else None

def generate_image_url(title):
    prompt = urllib.parse.quote(
        f"cryptocurrency trading dashboard, dark neon theme, bitcoin, {title[:50]}, "
        f"professional financial chart, glowing effects, 4k, cinematic"
    )
    seed = random.randint(1, 99999)
    return f"https://image.pollinations.ai/prompt/{prompt}?width=1200&height=675&model=flux&nologo=true&seed={seed}"

def send_to_telegram(news):
    title = news['title'].replace('| CoinDesk', '').replace('| Cointelegraph', '').strip()
    if len(title) > 150:
        title = title[:147] + "..."
    
    image_url = generate_image_url(title)
    
    caption = (
        f" <b>{title}</b>\n\n"
        f"📊 Source: {news['source']}\n"
        f"🔗 <a href='{news['link']}'>Читать далее</a>\n\n"
        f"#Crypto #Bitcoin #TheCryptoPulse"
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {
        "chat_id": CHANNEL_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=data, timeout=30)
    
    if response.status_code == 200:
        print("✅ Успешно опубликовано!")
        return True
    else:
        print(f"❌ Ошибка: {response.text}")
        return False

def main():
    print("🚀 CryptoPulse Bot запущен!")
    news = get_latest_news()
    
    if not news:
        print("⚠️ Новости не найдены")
        return
    
    print(f"📰 Новость: {news['title'][:60]}...")
    send_to_telegram(news)

if __name__ == "__main__":
    main()

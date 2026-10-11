import os
import random
import requests
import feedparser
import urllib.parse

BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

RSS_FEEDS = [
    "https://crypto.news/feed/",
    "https://bitcoinmagazine.com/feed",
    "https://theblock.co/rss.xml",
    "https://cointelegraph.com/rss",
    "https://u.today/rss",
]

def get_latest_news():
    all_entries = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for url in RSS_FEEDS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                for entry in feed.entries[:3]:
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    source = feed.feed.get('title', 'Crypto News')
                    if title and len(title) > 15:
                        all_entries.append({
                            'title': title,
                            'link': link,
                            'source': source
                        })
        except:
            pass
    
    if not all_entries:
        return None
    
    return random.choice(all_entries)

def generate_image_url(title):
    prompt = urllib.parse.quote(
        f"cryptocurrency trading dashboard, dark neon theme, bitcoin, {title[:50]}, "
        f"professional financial chart, glowing effects, 4k, cinematic"
    )
    seed = random.randint(1, 99999)
    return f"https://image.pollinations.ai/prompt/{prompt}?width=1200&height=675&model=flux&nologo=true&seed={seed}"

def send_to_telegram(news):
    title = news['title'].strip()
    if len(title) > 150:
        title = title[:147] + "..."
    
    image_url = generate_image_url(title)
    
    caption = (
        f"🚨 <b>{title}</b>\n\n"
        f"📊 Source: {news['source']}\n"
        f"🔗 <a href='{news['link']}'>Read more</a>\n\n"
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
        print("✅ Successfully posted!")
        return True
    else:
        print(f" Error: {response.text}")
        return False

def main():
    print("🚀 Bot started!")
    news = get_latest_news()
    
    if not news:
        print("⚠️ No news found")
        return
    
    print(f"📰 News: {news['title'][:60]}...")
    send_to_telegram(news)

if __name__ == "__main__":
    main()

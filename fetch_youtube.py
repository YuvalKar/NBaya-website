import requests
import xml.etree.ElementTree as ET
import json
import os

# הסוד שנוסיף בגיטהאב
CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID')
OUTPUT_FILE = 'youtube_update.json'

def fetch_latest_video():
    if not CHANNEL_ID:
        print("Error: YOUTUBE_CHANNEL_ID not found in env.")
        return

    # שימוש בפיד ה-RSS הציבורי של יוטיוב (לא דורש מפתח API!)
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # ניתוח ה-XML
        root = ET.fromstring(response.content)
        
        # הגדרת Namespaces לחיפוש ב-XML
        ns = {
            'yt': 'http://www.youtube.com/xml/schemas/2015', 
            'atom': 'http://www.w3.org/2005/Atom'
        }
        
        # מציאת הרשומה הראשונה (הסרטון האחרון)
        entry = root.find('atom:entry', ns)
        
        if entry:
            video_id = entry.find('yt:videoId', ns).text
            title = entry.find('atom:title', ns).text
            published = entry.find('atom:published', ns).text
            
            data = {
                "videoId": video_id,
                "title": title,
                "published": published
            }
            
            # שמירה לקובץ JSON
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print(f"Successfully fetched video: {title}")
        else:
            print("No videos found in feed.")

    except Exception as e:
        print(f"Error fetching YouTube feed: {e}")

if __name__ == "__main__":
    fetch_latest_video()
# env : conblock , lib : icrawler (pip)


from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler
import os
import time

# 각 재질별 크롤링 키워드(예시 포함, 확장 가능)
recycle_keywords = {
    'PETE': [
        'pet bottle', 'beverage bottle', 'cola bottle', 'soda bottle', 'juice bottle',
        'water bottle', 'soy sauce bottle', 'cooking oil bottle',
        '생수병', '콜라병', '사이다병', '음료수병', '간장병', '식용유병', '주스병'
    ],
    'HDPE': [
        'hdpe container', 'hdpe water bottle', 'hdpe shampoo bottle', 'hdpe detergent bottle',
        'white makgeolli bottle', '물통', '샴푸 용기', '세제 용기', '백색 막걸리통'
    ],
    'LDPE': [
        'ldpe milk bottle', 'ldpe makgeolli bottle',
        '우유병', '막걸리병'
    ],
    'PP': [
        'pp box', 'plastic basket', 'pp trash bin', 'pp scoop',
        '상자류', '플라스틱 바구니', '쓰레기통', '바가지', '맥주 상자', '소주 상자', '콜라 상자'
    ],
    'PS': [
        'ps bottle', 'ps yogurt bottle', 'ps fermented milk bottle',
        '요구르트병', '발효유병'
    ],
    'PVC': [
        'pvc container', 'pvc bottle', 'pvc industrial container'
    ]
}

def crawl_images(keywords, save_dir, max_num=400, use_bing=True, use_baidu=True, delay=10, repeat=3):
    os.makedirs(save_dir, exist_ok=True)
    for query in keywords:
        for r in range(repeat):
            print(f"[{r+1}/{repeat}] Google 크롤링: [{save_dir}] ← '{query}'")
            google_crawler = GoogleImageCrawler(storage={'root_dir': save_dir})
            google_crawler.crawl(keyword=query, max_num=max_num)
            time.sleep(delay)
            if use_bing:
                print(f"[{r+1}/{repeat}] Bing 크롤링: [{save_dir}] ← '{query}'")
                bing_crawler = BingImageCrawler(storage={'root_dir': save_dir})
                bing_crawler.crawl(keyword=query, max_num=max_num)
                time.sleep(delay)
            if use_baidu:
                print(f"[{r+1}/{repeat}] Baidu 크롤링: [{save_dir}] ← '{query}'")
                baidu_crawler = BaiduImageCrawler(storage={'root_dir': save_dir})
                baidu_crawler.crawl(keyword=query, max_num=max_num)
                time.sleep(delay)

# 재질별로 한 번에 모두 크롤링
for material, keywords in recycle_keywords.items():
    save_dir = f'data/{material}'
    crawl_images(keywords, save_dir, max_num=400, use_bing=True, use_baidu=True, delay=10, repeat=3)

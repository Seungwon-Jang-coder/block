# env : conblock , lib : icrawler (pip)

from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler
import os
import time

# 각 재질별 크롤링 키워드(예시 포함, 확장 가능)
recycle_keywords = {
    'PETE': [
        'PETE plastic waste', 'recycled PET bottle', 'PET flakes', 'PET bottle recycling plant',
        'used PET plastic bottle', 'PETE waste fabric', '폐 PET병', '페트병 폐기물', 'PET 플레이크',
        'PET 음료수병 폐기물', 'recycled PET packaging', 'PET 병 재활용'
    ],
    'HDPE': [
        'HDPE plastic waste', 'HDPE agricultural film waste', 'HDPE bottle recycling',
        'HDPE pesticide container waste', 'recycled HDPE pipe', '농업용 폐비닐 HDPE',
        '폐 농업용 필름 HDPE', '폐 HDPE 파이프', 'hdpe 용기', 'hdpe water bottle', 
        'hdpe shampoo bottle', 'hdpe detergent bottle', 'white makgeolli bottle', 
        '물통', '샴푸 용기', '세제 용기', '백색 막걸리통'
    ],
    'LDPE': [
        'LDPE plastic film waste', 'LDPE agricultural mulch film waste', 'recycled LDPE film',
        'LDPE mulch film recycling', '폐 LDPE 비닐', '농업용 폐비닐 LDPE', 'LDPE 필름 폐기물',
        'ldpe milk bottle', 'ldpe makgeolli bottle', '우유병', '막걸리병'
    ],
    'PP': [
        'PP plastic waste', 'polypropylene net waste', 'recycled PP rope',
        'PP fishing net waste', 'PP rope waste', 'polypropylene string waste',
        'polypropylene bag waste', '폐 PP 로프', '폐 폴리프로필렌 어망', 'recycled PP pellet',
        '폐 PP 어망', '폴리프로필렌 마대', 'pp box', 'pp trash bin', 'pp scoop',
        '상자류', '맥주 상자', '소주 상자', '콜라 상자'
    ],
    'PS': [
        'PS foam waste', 'polystyrene waste', 'recycled polystyrene fishing float',
        'PS fishing float waste', '폐 스티로폼', 'PS 부표 폐기물',
        'ps bottle', 'ps yogurt bottle', 'ps fermented milk bottle',
        '요구르트병', '발효유병'
    ],
    'PVC': [
        'PVC pipe waste', 'PVC hose waste', 'recycled PVC pipe', 'PVC sheet waste',
        '폐 PVC 파이프', '폐 PVC 호스', 'pvc container', 'pvc bottle', 'pvc industrial container'
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

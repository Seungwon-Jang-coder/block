import os
import glob
from PIL import Image
import hashlib

# ---- 재질별 크롤링 데이터 폴더 구조와 호환 ----
root_dir = 'data/PVC'  # data/PETE, data/HDPE, ... 등 하위 폴더 자동 포함

# 1. 깨진 이미지/확장자 문제/손상 파일 자동 삭제
def remove_invalid_and_non_jpg_png(root_dir):
    # webp/gif/svg 등 불필요 확장자 삭제
    for ext in ['*.webp', '*.gif', '*.svg']:
        for file in glob.glob(f'{root_dir}/**/{ext}', recursive=True):
            print(f"삭제: {file} (불필요 확장자)")
            os.remove(file)
    for folder, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(folder, file)
            # jpg/png/jpeg만 남기기
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                print(f"삭제: {file_path} (지원하지 않는 확장자)")
                os.remove(file_path)
            else:
                # 손상/열리지 않는 이미지도 삭제
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                except Exception as e:
                    print(f"오류로 삭제: {file_path} ({e})")
                    os.remove(file_path)

# 2. 너무 작은 이미지 자동 삭제 (예: 128x128 미만)
def remove_small_images(root_dir, min_width=128, min_height=128):
    for folder, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(folder, file)
            try:
                with Image.open(file_path) as img:
                    w, h = img.size
                    if w < min_width or h < min_height:
                        print(f"삭제: {file_path} (크기: {w}x{h})")
                        os.remove(file_path)
            except Exception as e:
                print(f"오류로 삭제: {file_path} ({e})")
                os.remove(file_path)

# 3. 완전히 중복된 이미지 자동 삭제 (해시값 비교)
def remove_duplicate_images(root_dir):
    hashes = {}
    for folder, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(folder, file)
            try:
                with open(file_path, 'rb') as f:
                    img_hash = hashlib.md5(f.read()).hexdigest()
                if img_hash in hashes:
                    print(f"중복 삭제: {file_path} (이미 {hashes[img_hash]}와 동일)")
                    os.remove(file_path)
                else:
                    hashes[img_hash] = file_path
            except Exception as e:
                print(f"해시 오류로 삭제: {file_path} ({e})")
                os.remove(file_path)

# ---- 실행 순서 ----
if __name__ == '__main__':
    print("=== 불량/확장자/손상 이미지 삭제 ===")
    remove_invalid_and_non_jpg_png(root_dir)

    print("\n=== 너무 작은 이미지 삭제 ===")
    remove_small_images(root_dir, min_width=128, min_height=128)

    print("\n=== 완전히 중복 이미지 삭제 ===")
    remove_duplicate_images(root_dir)

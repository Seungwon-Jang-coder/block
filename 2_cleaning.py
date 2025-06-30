import os
import glob
from PIL import Image
import hashlib

# ---- 지원 포맷: jpg, jpeg, png, bmp, gif 만 남기기 ----
valid_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

def remove_invalid_and_non_supported(root_dir):
    # webp/svg 등 미지원 확장자 우선 삭제
    for ext in ['*.webp', '*.svg']:
        for file in glob.glob(f'{root_dir}/**/{ext}', recursive=True):
            print(f"삭제: {file} (미지원 확장자)")
            os.remove(file)
    # 지원 확장자 외 나머지 파일 삭제 + 손상 파일 삭제
    for folder, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(folder, file)
            # 지원 포맷만 남기기
            if not file.lower().endswith(valid_ext):
                print(f"삭제: {file_path} (지원하지 않는 확장자)")
                os.remove(file_path)
            else:
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                except Exception as e:
                    print(f"오류로 삭제: {file_path} ({e})")
                    os.remove(file_path)

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

# 여러 폴더를 한 번에 정제 가능하도록
def clean_all(root_dirs):
    for d in root_dirs:
        print(f"\n=== {d} ===")
        print("불량/확장자/손상 이미지 삭제")
        remove_invalid_and_non_supported(d)
        print("너무 작은 이미지 삭제")
        remove_small_images(d, min_width=128, min_height=128)
        print("완전히 중복 이미지 삭제")
        remove_duplicate_images(d)

if __name__ == '__main__':
    # 주요 데이터셋 폴더 전체 정제
    root_dirs = [
        'data_split/train',
        'data_split/val',
        'data_split/test'
    ]
    clean_all(root_dirs)

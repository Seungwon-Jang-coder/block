import os
from PIL import Image

def ultra_clean(root_dir):
    valid_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    count_total, count_deleted = 0, 0
    for folder, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(folder, file)
            count_total += 1
            delete = False
            # 확장자 체크
            if not file.lower().endswith(valid_ext):
                print("삭제: 미지원 확장자", file_path)
                os.remove(file_path)
                count_deleted += 1
                continue
            # 실제 이미지 검증
            try:
                with Image.open(file_path) as img:
                    img.verify()
            except Exception as e:
                print("삭제: 손상/오류 이미지", file_path, f"({e})")
                os.remove(file_path)
                count_deleted += 1
    print(f"{root_dir}: 전체 {count_total}개, 삭제 {count_deleted}개, 남은 파일 {count_total - count_deleted}개")

ultra_clean("data_split/train")
ultra_clean("data_split/val")
ultra_clean("data_split/test")

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# 1. 데이터 불러오기/전처리
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2    # 20%는 검증용
)

train_gen = datagen.flow_from_directory(
    'data/',
    target_size=(128, 128),   # 이미지 크기 줄여도 실습에 문제없음
    batch_size=8,
    class_mode='categorical',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    'data/',
    target_size=(128, 128),
    batch_size=8,
    class_mode='categorical',
    subset='validation'
)

# 2. 모델 정의
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(2, activation='softmax')  # 클래스 2개(페트병, 캔)
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 3. 학습
history = model.fit(
    train_gen,
    epochs=10,
    validation_data=val_gen
)

# 4. 학습 결과 시각화 (옵션)
plt.plot(history.history['accuracy'], label='train_acc')
plt.plot(history.history['val_accuracy'], label='val_acc')
plt.legend()
plt.show()

# 5. 최종 검증 정확도(수치) 터미널 출력
val_loss, val_acc = model.evaluate(val_gen)
print(f'Validation Accuracy: {val_acc:.4f}')

# 실제 적용 예시

import numpy as np
from tensorflow.keras.preprocessing import image
import os

# 예측할 이미지 경로를 입력하세요 (예시: 테스트할 이미지 파일을 프로젝트 폴더에 넣고 파일명 지정)
test_img_path = '/Users/sng209d/Desktop/download.jpeg'  # 예시. 파일명/경로 원하는 걸로 바꾸세요

# 파일이 실제 존재하는지 확인 (없으면 오류나니, 파일명/경로 확인 필수!)
if os.path.exists(test_img_path):
    # 이미지 불러와서 전처리
    img = image.load_img(test_img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0  # 정규화
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가

    # 예측
    pred = model.predict(img_array)
    class_names = list(train_gen.class_indices.keys())  # 예: ['can', 'plastic_bottle']
    pred_class = class_names[np.argmax(pred)]

    print(f'이미지 예측 결과: {pred_class}')
else:
    print(f"파일이 존재하지 않습니다: {test_img_path}")


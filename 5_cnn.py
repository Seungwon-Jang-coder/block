# find data_split/ -type f | while read f; do file "$f" | grep -q 'Web/P image' && echo "삭제: $f" && rm "$f"; done

import tensorflow as tf
from keras.utils import image_dataset_from_directory
from keras import layers, models, Sequential, Input
import matplotlib.pyplot as plt

# 1. 데이터셋 준비
data_dir = "data_split"
batch_size = 16
img_size = (128, 128)

train_ds = image_dataset_from_directory(
    f"{data_dir}/train",
    image_size=img_size,
    batch_size=batch_size,
    label_mode="categorical"
)
val_ds = image_dataset_from_directory(
    f"{data_dir}/val",
    image_size=img_size,
    batch_size=batch_size,
    label_mode="categorical"
)
test_ds = image_dataset_from_directory(
    f"{data_dir}/test",
    image_size=img_size,
    batch_size=batch_size,
    label_mode="categorical"
)

# 1-1. 클래스 정보는 prefetch 전에 변수에 저장!
class_names = train_ds.class_names
num_classes = len(class_names)

# 2. 증강 레이어 정의 (Keras 공식)
data_augmentation = Sequential([
    layers.Rescaling(1./255),        # 0~255 → 0~1 정규화
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.08),
    layers.RandomZoom(0.1),
    layers.RandomBrightness(factor=0.2),  # 밝기 변환 (Keras 3.x)
])

# 3. 데이터셋 prefetch (성능 향상)
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

# 4. 모델 정의 (EfficientNetB0 예시)
base_model = tf.keras.applications.EfficientNetB0(
    include_top=False, input_shape=(128, 128, 3), pooling='avg', weights='imagenet'
)
base_model.trainable = False  # 처음엔 동결

inputs = Input(shape=(128,128,3))
x = data_augmentation(inputs)
x = base_model(x)
x = layers.Dense(128, activation='relu')(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)
model = models.Model(inputs, outputs)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 5. 학습
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=15
)

# 6. 결과 시각화
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.legend()
plt.show()

# 7. 테스트셋 최종 평가
test_loss, test_acc = model.evaluate(test_ds)
print(f"Test Accuracy: {test_acc:.4f}")

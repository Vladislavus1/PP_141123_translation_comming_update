import tensorflow as tf

def create_model(input_shape):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))  # 1 выход, так как у нас бинарная классификация

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Пример использования
# Предполагается, что у вас есть данные для обучения, например, принимаемые и непринимаемые изображения
# train_images = ...
# train_labels = ...

# Здесь вам нужно подготовить ваши данные для обучения
# ...

# Предобработка данных (пример, используя tf.keras.preprocessing.image.ImageDataGenerator)
# ...

# Создание модели
# input_shape = (height, width, channels)  # Замените на размер ваших изображений
# model = create_model(input_shape)gggdaswfa
# Обучение модели
# model.fit(train_images, train_labels, epochs=10)

# Сохранение модели на диск
# model.save('image_classifier_model.h5')
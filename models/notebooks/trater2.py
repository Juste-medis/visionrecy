# Importation des dépendances nécessaires
import warnings  # Pour gérer les avertissements
import tensorflow as tf  # Pour le deep learning
# Pour le prétraitement des images
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
# Modèle pré-entraîné MobileNetV2
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image  # Pour manipuler les images
# Pour charger un modèle sauvegardé
from tensorflow.keras.models import load_model
# Couches du modèle
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model  # Pour créer un modèle
from tensorflow.keras.optimizers import Adam  # Optimiseur Adam
# Callbacks pour l'entraînement
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Importation des modules de scikit-learn pour l'évaluation
from sklearn.metrics import classification_report, confusion_matrix

# Autres imports
import os  # Pour interagir avec le système de fichiers
import numpy as np  # Pour les calculs numériques
import matplotlib.pyplot as plt  # Pour la visualisation
import seaborn as sns  # Pour des graphiques statistiques
from IPython.display import Image  # Pour afficher des images dans un notebook
import glob  # Pour rechercher des fichiers

# Affichage des images pour comprendre le contexte
Image(r'D:Content\share-of-global-mismanaged-plastic-waste.png', width=900, height=700)
Image(r'D:Content\stats e waste.png', width=900, height=700)
Image(r'D:Content\waste crisis.png', width=900, height=700)
Image(r'D:Content\sorting challenges.png', width=900, height=700)
Image(r'D:Content\wastesorting.png', width=900, height=700)

# Définition des répertoires de base pour le dataset
BASE_DIR = r"C:\Users\Hp\pictures\back up\wastes"  # Chemin vers le dataset
train_dir = os.path.join(BASE_DIR, 'train')  # Répertoire d'entraînement
test_dir = os.path.join(BASE_DIR, 'test')    # Répertoire de test

# Visualisation des données d'entraînement
# Chemin vers le dossier d'entraînement
train_dir = r"C:\Users\Hp\pictures\back up\wastes\train"
class_names = os.listdir(train_dir)  # Liste des classes (dossiers)

# Affichage du nombre d'images par classe et visualisation de quelques images
for class_name in class_names:
    class_dir = os.path.join(train_dir, class_name)
    class_images = glob.glob(os.path.join(
        class_dir, '*.jpg'))  # Liste des images .jpg
    print(
        f"Nombre d'images d'entraînement dans la classe '{class_name}': {len(class_images)}")

    # Affichage de 5 images aléatoires de la classe
    if len(class_images) > 0:
        plt.figure(figsize=(10, 5))
        for i in range(5):
            plt.subplot(1, 5, i+1)
            # Choix aléatoire d'une image
            img_path = np.random.choice(class_images)
            # Chargement et redimensionnement
            img = load_img(img_path, target_size=(224, 224))
            # Conversion en tableau et normalisation
            img_array = img_to_array(img) / 255.0
            plt.imshow(img_array)
            plt.axis('off')
            plt.title(class_name)
        plt.show()

# Visualisation des données de test
# Chemin vers le dossier de test
test_dir = r"C:\Users\Hp\Videos\back up\wastes\test"
IMG_SIZE = (224, 224)  # Taille des images
class_names = os.listdir(test_dir)  # Liste des classes (dossiers)

# Affichage du nombre d'images par classe et visualisation de quelques images
for class_name in class_names:
    class_dir = os.path.join(test_dir, class_name)
    class_images = glob.glob(os.path.join(
        class_dir, '*.jpg'))  # Liste des images .jpg
    print(
        f"Nombre d'images de test dans la classe '{class_name}': {len(class_images)}")

    # Affichage de 5 images aléatoires de la classe
    if len(class_images) > 0:
        plt.figure(figsize=(10, 5))
        for i in range(5):
            plt.subplot(1, 5, i+1)
            # Choix aléatoire d'une image
            img_path = np.random.choice(class_images)
            # Chargement et redimensionnement
            img = load_img(img_path, target_size=IMG_SIZE)
            # Conversion en tableau et normalisation
            img_array = img_to_array(img) / 255.0
            plt.imshow(img_array)
            plt.axis('off')
            plt.title(class_name)
        plt.show()

# Augmentation des données
train_datagen = ImageDataGenerator(
    rescale=1.0/255,  # Normalisation des pixels
    rotation_range=30,  # Rotation aléatoire jusqu'à 30 degrés
    width_shift_range=0.2,  # Décalage horizontal jusqu'à 20%
    height_shift_range=0.2,  # Décalage vertical jusqu'à 20%
    shear_range=0.2,  # Cisaillement jusqu'à 20%
    zoom_range=0.2,  # Zoom jusqu'à 20%
    horizontal_flip=True,  # Retournement horizontal
    fill_mode='nearest'  # Remplissage des pixels manquants
)

# Générateur de données de test (sans augmentation)
test_datagen = ImageDataGenerator(rescale=1.0/255)  # Normalisation des pixels

# Chargement des données d'entraînement
train_generator = train_datagen.flow_from_directory(
    # Chemin des données d'entraînement
    directory=os.path.join(BASE_DIR, 'train'),
    target_size=IMG_SIZE,  # Redimensionnement des images
    batch_size=32,  # Taille du batch
    class_mode='categorical'  # Classification catégorielle
)

# Chargement des données de test
test_generator = test_datagen.flow_from_directory(
    directory=os.path.join(BASE_DIR, 'test'),  # Chemin des données de test
    target_size=IMG_SIZE,  # Redimensionnement des images
    batch_size=32,  # Taille du batch
    class_mode='categorical',  # Classification catégorielle
    shuffle=False  # Pas de mélange pour l'évaluation
)

# Affichage des étiquettes de classe
# Dictionnaire des classes et leurs indices
class_labels = train_generator.class_indices
print("Étiquettes de classe et valeurs encodées :")
print(class_labels)

# Définition des callbacks
filepath = './final_model_weights.keras'  # Chemin pour sauvegarder les poids
earlystopping = EarlyStopping(
    monitor='val_auc', mode='max', patience=5, verbose=1)
checkpoint = ModelCheckpoint(
    filepath, monitor='val_auc', mode='max', save_best_only=True, verbose=1)
callback_list = [earlystopping, checkpoint]

# Construction du modèle
base_model = MobileNetV2(input_shape=(224, 224, 3),
                         include_top=False, weights="imagenet")
for layer in base_model.layers:
    layer.trainable = False  # Gel des couches du modèle de base

# Ajout de couches personnalisées
model = Sequential()
model.add(base_model)
model.add(Dropout(0.2))
model.add(Flatten())
model.add(BatchNormalization())
model.add(Dense(512, activation="relu", kernel_initializer='he_uniform'))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Dense(256, activation="relu", kernel_initializer='he_uniform'))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Dense(128, activation="relu", kernel_initializer='he_uniform'))
model.add(Dropout(0.2))
model.add(Dense(9, activation="softmax"))  # Couche de sortie pour 9 classes

# Compilation du modèle
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
history = model.fit(
    train_generator,  # Données d'entraînement
    epochs=15,  # Nombre d'époques
    validation_data=test_generator,  # Données de validation
    callbacks=callback_list  # Callbacks
)

# Sauvegarde du modèle
model.save("mobilenetv2_waste_classification_final.h5")
print("Modèle final sauvegardé sous mobilenetv2_waste_classification_final.h5")

# Évaluation du modèle sur les données de test
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Précision sur les données de test : {test_accuracy * 100:.2f}%")

# Affichage des performances d'entraînement
plt.figure(figsize=(10, 5))
plt.plot(history.history['accuracy'], label='Précision (entraînement)')
plt.plot(history.history['loss'], label='Perte (entraînement)')
plt.legend()
plt.title('Performances d\'entraînement')
plt.show()

# Rapport de classification
test_generator.reset()
y_pred = model.predict(test_generator)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

print("\nRapport de classification :\n", classification_report(
    y_true, y_pred_classes, target_names=class_labels))

# Matrice de confusion
cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_labels, yticklabels=class_labels, cbar=False)
plt.title('Matrice de confusion')
plt.xlabel('Prédictions')
plt.ylabel('Vraies étiquettes')
plt.show()

# Prédiction sur une nouvelle image
model = load_model('mobilenetv2_waste_classification.h5')
IMG_SIZE = (224, 224)
# Chemin de l'image à prédire
img_path = r"C:\Users\Hp\Videos\back up\wastes\test\E-waste\E-waste (216).jpg"

# Prétraitement de l'image
img = image.load_img(img_path, target_size=IMG_SIZE)
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.0

# Prédiction
predictions = model.predict(img_array)
predicted_class_index = np.argmax(predictions, axis=1)[0]
class_labels = sorted(os.listdir(train_dir))  # Étiquettes des classes
predicted_class = class_labels[predicted_class_index]

# Affichage de la prédiction
print(f"Classe prédite : {predicted_class}")
plt.imshow(img)
plt.title(f"Prédiction : {predicted_class}")
plt.axis('off')
plt.show()

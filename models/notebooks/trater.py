# Importation des dépendances
import pandas as pd  # Pour la manipulation de données
import numpy as np   # Pour les calculs numériques
import logging       # Pour la gestion des logs
import tensorflow as tf  # Pour le deep learning
import warnings      # Pour gérer les avertissements
import glob          # Pour rechercher des fichiers
import tqdm          # Pour les barres de progression
import os            # Pour interagir avec le système de fichiers

from tqdm import tqdm  # Pour les barres de progression
from IPython import display  # Pour afficher des images dans un notebook
import matplotlib.pyplot as plt  # Pour la visualisation
import seaborn as sns  # Pour des graphiques statistiques
from seaborn import heatmap  # Pour les heatmaps

from sklearn.model_selection import train_test_split  # Pour diviser les données
# Pour l'évaluation du modèle
from sklearn.metrics import confusion_matrix, classification_report

from skimage.io import imread, imshow  # Pour lire et afficher des images
from skimage.transform import resize  # Pour redimensionner les images

from tensorflow import keras  # Pour le deep learning
# Pour créer et charger des modèles
from keras.models import Sequential, load_model
# Couches du modèle
from keras.layers import Conv2D, Lambda, MaxPooling2D, Dense, Dropout, Flatten

from tensorflow.keras.layers import BatchNormalization  # Normalisation des couches
# Augmentation des données
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.applications.vgg16 import VGG16  # Modèle pré-entraîné VGG16
# Pour charger des images depuis un dossier
from tensorflow.keras.preprocessing import image_dataset_from_directory
# Pour charger et convertir des images
from tensorflow.keras.preprocessing.image import load_img, img_to_array
# Callbacks pour l'entraînement
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, History

# Affichage de la structure du dataset
display.Image('Resources/Images/waste_data_structure.jpeg',
              width=550, height=250)

# Chemins des répertoires pour importer les données
base_dir = "../../Resources/Dataset"
train_dir = os.path.join(base_dir, "Train")
test_dir = os.path.join(base_dir, "Test")

# Récupération des chemins des images d'entraînement
train_o = glob.glob(os.path.join(train_dir, 'O', '*.jpg')
                    )  # Images de déchets organiques
train_r = glob.glob(os.path.join(train_dir, 'R', '*.jpg')
                    )  # Images de déchets recyclables

a = len(train_o)  # Nombre d'images organiques
b = len(train_r)  # Nombre d'images recyclables

print(f"Nombre d'images à entraîner : {a + b}")

# Récupération des chemins des images de test
test_o = glob.glob(os.path.join(test_dir, 'O', '*.jpg')
                   )  # Images de déchets organiques
test_r = glob.glob(os.path.join(test_dir, 'R', '*.jpg')
                   )  # Images de déchets recyclables

a = len(test_o)  # Nombre d'images organiques
b = len(test_r)  # Nombre d'images recyclables

print(f"Nombre d'images de test : {a + b}")

# Augmentation des données
# Paramètres :
# - Redimensionnement à 255
# - Taille des images : (180, 180)
# - Retournements horizontaux et verticaux activés
# - Rotation de 10 degrés
# - Zoom de 0.4

# Générateurs de données
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,  # Normalisation des pixels
    zoom_range=0.4,  # Zoom aléatoire
    rotation_range=10,  # Rotation aléatoire
    horizontal_flip=True,  # Retournement horizontal
    vertical_flip=True,  # Retournement vertical
    validation_split=0.2  # Split de validation (80% train, 20% validation)
)

valid_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,  # Normalisation des pixels
    validation_split=0.2  # Split de validation
)

test_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0  # Normalisation des pixels
)

# Chargement des données d'entraînement
train_ds = train_datagen.flow_from_directory(
    directory=train_dir,  # Répertoire des données d'entraînement
    target_size=(180, 180),  # Taille des images
    class_mode='categorical',  # Mode de classification (catégoriel)
    batch_size=32,  # Taille du batch
    subset='training'  # Sous-ensemble d'entraînement
)

# Chargement des données de validation
valid_ds = valid_datagen.flow_from_directory(
    directory=train_dir,  # Répertoire des données d'entraînement
    target_size=(180, 180),  # Taille des images
    class_mode='categorical',  # Mode de classification (catégoriel)
    batch_size=32,  # Taille du batch
    subset='validation'  # Sous-ensemble de validation
)

# Chargement des données de test
test_ds = test_datagen.flow_from_directory(
    directory=test_dir,  # Répertoire des données de test
    target_size=(180, 180),  # Taille des images
    class_mode='categorical',  # Mode de classification (catégoriel)
    batch_size=32,  # Taille du batch
    shuffle=False  # Pas de mélange pour les données de test
)

# Affichage des indices de classe
print(
    f"Indices de classe pour les données d'entraînement : {train_ds.class_indices}")
print(f"Indices de classe pour les données de test : {test_ds.class_indices}")

# Affichage d'exemples d'images
fig, ax = plt.subplots(nrows=2, ncols=5, figsize=(12, 6)
                       )  # Création d'une grille d'images
for i in range(2):
    for j in range(5):
        # Sélection aléatoire d'un batch
        rand1 = np.random.randint(len(train_ds))
        # Sélection aléatoire d'une image dans le batch
        rand2 = np.random.randint(32)
        ax[i, j].imshow(train_ds[rand1][0][rand2])  # Affichage de l'image
        ax[i, j].axis('off')  # Désactivation des axes
        label = train_ds[rand1][1][rand2]  # Récupération du label
        if label[0] == 0:
            # Titre pour les déchets organiques
            ax[i, j].set_title('Déchet Organique')
        else:
            # Titre pour les déchets recyclables
            ax[i, j].set_title('Déchet Recyclable')
plt.tight_layout()
plt.show()

# Construction du modèle
# Modèle de base VGG16
base_model = VGG16(
    input_shape=(180, 180, 3),  # Taille des images en entrée
    include_top=False,  # Exclure les couches fully connected
    weights="imagenet"  # Poids pré-entraînés sur ImageNet
)

# Gel des couches du modèle de base
for layer in base_model.layers:
    layer.trainable = False  # Les couches ne seront pas entraînées

# Ajout de couches personnalisées
model = Sequential()
model.add(base_model)  # Ajout du modèle de base
model.add(Dropout(0.2))  # Dropout pour éviter le surapprentissage
model.add(Flatten())  # Aplatissement des données
model.add(BatchNormalization())  # Normalisation des couches
model.add(Dense(5000, activation="relu",
          kernel_initializer='he_uniform'))  # Couche dense
model.add(BatchNormalization())  # Normalisation des couches
model.add(Dropout(0.2))  # Dropout
model.add(Dense(1000, activation="relu",
          kernel_initializer='he_uniform'))  # Couche dense
model.add(BatchNormalization())  # Normalisation des couches
model.add(Dropout(0.2))  # Dropout
# Couche dense
model.add(Dense(500, activation="relu", kernel_initializer='he_uniform'))
model.add(Dropout(0.2))  # Dropout
model.add(Dense(2, activation="softmax"))  # Couche de sortie (2 classes)

# Compilation du modèle
model.compile(
    loss="categorical_crossentropy",  # Fonction de perte
    optimizer="adam",  # Optimiseur
    metrics=[tf.keras.metrics.AUC(name='auc')]  # Métrique (AUC)
)

# Callbacks pour l'entraînement
filepath = './final_model_weights.hdf5'  # Chemin pour sauvegarder les poids
earlystopping = EarlyStopping(
    monitor='val_auc',  # Surveillance de la métrique AUC
    mode='max',  # Mode de surveillance
    patience=5,  # Patience avant arrêt
    verbose=1
)
checkpoint = ModelCheckpoint(
    filepath,  # Chemin de sauvegarde
    monitor='val_auc',  # Surveillance de la métrique AUC
    mode='max',  # Mode de surveillance
    save_best_only=True,  # Sauvegarde uniquement du meilleur modèle
    verbose=1
)
callback_list = [earlystopping, checkpoint]  # Liste des callbacks

# Entraînement du modèle
model_history = model.fit(
    train_ds,  # Données d'entraînement
    epochs=20,  # Nombre d'époques
    validation_data=valid_ds,  # Données de validation
    callbacks=callback_list,  # Callbacks
    verbose=1  # Affichage des logs
)

# Sauvegarde des résultats d'entraînement
history_df = pd.DataFrame(model_history.history)  # Conversion en DataFrame
history_df.to_csv('Resources/Model/model_history.csv',
                  index=False)  # Sauvegarde en CSV

# Évaluation du modèle sur les données de test
loss, auc = model.evaluate(test_ds)
print(f"Perte finale : {loss}, AUC finale : {auc}")

# Affichage des courbes de perte et d'AUC
plt.figure(figsize=(12, 7))
plt.plot(model_history.history['loss'],
         color='deeppink', linewidth=4, label='Train')
plt.plot(model_history.history['val_loss'],
         color='dodgerblue', linewidth=4, label='Validation')
plt.title('Perte du modèle', fontsize=14, fontweight='bold')
plt.ylabel('Perte', fontsize=14, fontweight='bold')
plt.xlabel('Époque', fontsize=14, fontweight='bold')
plt.legend()
plt.show()

plt.figure(figsize=(12, 7))
plt.plot(model_history.history['auc'],
         color='deeppink', linewidth=4, label='Train')
plt.plot(model_history.history['val_auc'],
         color='dodgerblue', linewidth=4, label='Validation')
plt.title('AUC du modèle', fontsize=14, fontweight='bold')
plt.ylabel('AUC', fontsize=14, fontweight='bold')
plt.xlabel('Époque', fontsize=14, fontweight='bold')
plt.legend()
plt.show()

# Matrice de confusion et rapport de classification
Y_pred = model.predict(test_ds)  # Prédictions
y_pred = np.argmax(Y_pred, axis=1)  # Conversion des prédictions en classes
print('Matrice de confusion :')
print(confusion_matrix(test_ds.classes, y_pred))
print('Rapport de classification :')
print(classification_report(test_ds.classes, y_pred,
      target_names=['Organique', 'Recyclable']))

# Prédiction sur des images de test


def getprediction(img):
    img = img_to_array(img)  # Conversion en tableau numpy
    img = img / 255  # Normalisation
    imshow(img)  # Affichage de l'image
    plt.axis('off')  # Désactivation des axes
    img = np.expand_dims(img, axis=0)  # Ajout d'une dimension pour le batch
    category = np.argmax(model.predict(img), axis=1)  # Prédiction de la classe
    probability = model.predict(img)  # Probabilités
    if category[0] == 1:
        print(
            f"L'image appartient à la catégorie Recyclable, probabilité : {probability[0][1]}")
    else:
        print(
            f"L'image appartient à la catégorie Organique, probabilité : {probability[0][0]}")


# Exemples de prédictions
test_case1 = load_img(test_dir + '/O' + '/O_12568.jpg', target_size=(180, 180))
getprediction(test_case1)

test_case2 = load_img(test_dir + '/O' + '/O_13185.jpg', target_size=(180, 180))
getprediction(test_case2)

test_case3 = load_img(test_dir + '/O' + '/O_13905.jpg', target_size=(180, 180))
getprediction(test_case3)

test_case4 = load_img(test_dir + '/R' + '/R_10000.jpg', target_size=(180, 180))
getprediction(test_case4)

test_case5 = load_img(test_dir + '/R' + '/R_10398.jpg', target_size=(180, 180))
getprediction(test_case5)

test_case6 = load_img(test_dir + '/R' + '/R_10714.jpg', target_size=(180, 180))
getprediction(test_case6)

test_case7 = load_img(test_dir + '/R' + '/R_11107.jpg', target_size=(180, 180))
getprediction(test_case7)

test_case8 = load_img(test_dir + '/R' + '/R_10005.jpg', target_size=(180, 180))
getprediction(test_case8)

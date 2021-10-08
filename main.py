import numpy as np
import itk, os

# ----------------------
# Lecture de l'image
# ----------------------
image_dir = 'images'
input_filename = os.path.join(image_dir, 'brain.png')
image = itk.imread(input_filename)
ImageType = type(image)
# On récupère le type de l'image

# ----------------------
# Création et paramétrage du filtre
# ----------------------

# On créé une instance du filtre qui prend en entrée et ressort des images du même type que l'image d'entrée
smoothFilter = itk.SmoothingRecursiveGaussianImageFilter[ImageType, ImageType].New() 
smoothFilter.SetInput(image) # On spécifie l'image d'entrée du filtre

sigma = 0.7
smoothFilter.SetSigma(sigma) # On sélectionne la variance du filtre

# ----------------------
# Écriture de la sortie du filtre
# ----------------------
itk.imwrite(smoothFilter.GetOutput(), os.path.join(image_dir,'myImage_smoothed.png')) # On écrit sur le disque la sortie du filtre Gaussien
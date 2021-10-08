import itk, os, argparse

# ----------------------
# Parser
# ----------------------
parser = argparse.ArgumentParser(description='TP Recalage')

args = parser.parse_args()

# ----------------------
# Lecture des images
# ----------------------
image_dir = 'images'

image_output_dir = os.path.join(image_dir, 'output')
if not(os.path.exists(image_output_dir)):
    os.makedirs(image_output_dir)

input_filename_fixed = os.path.join(image_dir, 'BrainProtonDensitySliceBorder20.png')
fixed_image = itk.imread(input_filename_fixed)
fixed_image_type = type(fixed_image) # On récupère le type de l'image fixe

input_filename_moving = os.path.join(image_dir, 'BrainProtonDensitySliceR10X13Y17.png')
moving_image = itk.imread(input_filename_moving)
moving_image_type = type(moving_image) # On récupère le type de l'image translatée


# ----------------------
# Optimiseur
# ----------------------
optimizer = itk.RegularStepGradientDescentOptimizer.New() # Instance de la classe d'optimiseur choisie
optimizer.SetMaximumStepLength(4.)
optimizer.SetMinimumStepLength(.01)
optimizer.SetNumberOfIterations(200)

# ----------------------
# initial Parameter
# ----------------------

initialTransform = itk.CenteredRigid2DTransform[itk.D, 2].New() # Instance de la classe de transformation choisie
initialParameters = initialTransform.GetParameters() # Récupération des paramètres de la transformation

initialParameters[0] = 0
initialParameters[1] = moving_image.shape[0]/2
initialParameters[2] = moving_image.shape[1]/2
initialParameters[3] = 0
initialParameters[4] = 0

# ----------------------
# Interpolateur
# ----------------------

interpolator = itk.LinearInterpolateImageFunction[moving_image_type, itk.D].New()

# ----------------------
# Metrics
# ----------------------
metric = itk.MeanSquaresImageToImageMetric[fixed_image_type, moving_image_type].New()

# ----------------------
# Exécution du recalage
# ----------------------

registration_filter = itk.ImageRegistrationMethod[fixed_image_type, moving_image_type].New() # Instance de la classe de recalage
registration_filter.SetFixedImage(fixed_image) # Image de référence
registration_filter.SetMovingImage(moving_image) # Image à recaler
registration_filter.SetOptimizer(optimizer) # Optimiseur
registration_filter.SetTransform(itk.CenteredRigid2DTransform[itk.D, 2].New()) # Transformation
registration_filter.SetInitialTransformParameters(initialParameters) #Application de la transformation initiale
registration_filter.SetInterpolator(interpolator) # Interpolateur
registration_filter.SetMetric(metric) # Métrique
registration_filter.Update() # Exécution du recalage

# ----------------------
# Apply last transform
# ----------------------

final_transform = registration_filter.GetTransform()
resample_filter = itk.ResampleImageFilter[fixed_image_type,moving_image_type].New() #Instance de la classe de ré-échantillonnage
resample_filter.SetInput(moving_image) # Image d'entrée
resample_filter.SetTransform(final_transform)
resample_filter.SetSize(fixed_image.GetLargestPossibleRegion().GetSize())

output_image = resample_filter.GetOutput()
itk.imwrite(output_image, os.path.join(image_output_dir, 'image_recalee2.png'))

itk.imwrite(itk.AbsoluteValueDifferenceImageFilter(output_image, moving_image), os.path.join(image_output_dir,'moving_diff2.png'))
itk.imwrite(itk.AbsoluteValueDifferenceImageFilter(output_image, fixed_image), os.path.join(image_output_dir,'fixed_diff2.png'))
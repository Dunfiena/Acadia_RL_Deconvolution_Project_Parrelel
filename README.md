# Acadia_RL_Deconvolution_Project
Richardson Lucy Decovolution for 1 and 2D images
This project was made with Acadia University and is open for use.  It works on the Richarson-Lucy Deconvolution principles
for deconvolving 1D spectra, 2D grey and 2D color deconvultion on images.


Installation can be done with pyinstaller using the command 'pyinstaller GUI_RL_Deconvolution.py --onefile' in pycharm
or through the terminal


1D Deconvolution) To run 1D deconvolution, use a text file with two columns.  Column two should be the wave of the emission

2D Deconvolution) Takes colored image and turns it grey then deconvolves the array

2D Deconvolution - color) Takes colored images, seperates them into RGB channels and deconvolves each seperately, then puts
  them back together to create RBG image

To deconvolve at the best settings, play with the pixel value, the sigma and the iterations.  Included are sample images
and text files from test we ran in producing this program.


HOW IT WORKS

1D PSF Generation)
  This program is used to generate a few different pieces of information.  From it we get a point spread function (PSF),
  and output images and graphs.  The first step in deconvolving is to generate the point spread function.  For a 1D PSF
  We use this equation below:
  
  results = ((1 / (math.sqrt(2 * math.pi * sigma))) *
                   (math.pow(math.e, -(math.pow((X - Xo), 2) / (2 * math.pow(sigma, 2))))))
                   
  This represents 1 point in the point spread function, this calculation with be run an equal amount of times as pixels
  you have selected for the run.  Sigma is the same as selected for the run, X is the iteration number (from 1 to total
  number of runs), and Xo is equal to pixels/2.
![1D PSF sigma 10](https://github.com/Dunfiena/Acadia_RL_Deconvolution_Project/assets/117761149/bb18de7f-4547-40b5-a02b-f643ce027af5)


2D PSF Generation
  This is run very similarly to the 1D PSF generation, expecting that in including a 2D dimention, we double the number
  of values:

  results = ((1 / (2 * math.pi * math.pow(sigma, 2))) *
                       (math.pow(math.e, -(math.pow((X - Xo), 2) / (2 * math.pow(sigma, 2))))) *
                       (math.pow(math.e, -(math.pow((Y - Yo), 2) / (2 * math.pow(sigma, 2))))))
<img width="221" alt="2D psf sigma 10" src="https://github.com/Dunfiena/Acadia_RL_Deconvolution_Project/assets/117761149/b155c12d-33b8-42f5-bbbf-ec19172a3362">


  Adding another loop to run Y an equal number of times to the iterations, for each time X runs once.  In addition we add
  Y and Yo to the equation with the same parameteres as X and Xo.  For more information on the setup of this generation, 
  see the Generate_PSF.py file.

Deconvolution
  All three Deconvolution types use the same package, which is the skimage.restoration Richardon-Lucy Deconvolution.
  It uses an array that is input, the psf and the number of iterations to Deconvolve the image.  1D takes like to no time,
  but be careful with the 2D deconvlution, running high numbers of iterations can take quite a while; especially with the
  color deconvolution white runs 3 times per iteration (for each color)


  

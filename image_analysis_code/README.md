# Image Analysis Code

This repo provides a sample of some code written during my PhD to provide biologists with a more streamlined way to handle microscope images for quantification of specific information about the cells in those images.

In this particular example, code was used for analysis of data generated as part of the published work: Qian, DeGennaro et al. Developmental Cell 2022 "Loss of non-motor kinesin KIF26A causes congenital brain malformations via dysregulated neuronal migration and axonal growth as well as apoptosis" https://www.sciencedirect.com/science/article/pii/S1534580722006815

To answer a biological question about the effect our gene of interest was having on cells in the developing mouse brain, developmental biologists use the position of cells in the vertical direction within the layers of the brain as one metric of brain health. Cells that are not migrating properly will not be found in the developmentally-appropriate layer of the brain.

This can be easily assessed qualitatively, by looking at a microscope image taken of a thin cross-section of a brain, however quantitative measurements can be challenging and time-consuming to obtain for large numbers of images over many biological and technical replicates.

To address this problem, specifically with 31 images from different animals across 4 different experimental conditions, I developed a pipeline that would transform the raw microscopy imaging data into the same consistent format enabling easy manual quantification of cells and their positions using ImageJ or FIJI software and a custom python script to process the software output, drastically reducing the analysis time for the researcher, and standardizing the image inputs for subsequent publication.

## Usage

Once you have obtained your microscopy image files (we use Zeiss microscopes, so these will be in .czi format) and backed them up, a copy of good images for analysis should be located in a single directory. I name this directory "01_originals". Before running, you'll want to check that all your input files have no spaces in them! ImageJ/FIJI macros do not tolerate this.

### Image pre-processing
With: https://github.com/ellen-dege/public-demo-code/blob/main/image_analysis_code/KIF_FIJImacro_image_preprocessing.ijm
ImageJ/FIJI documentation: https://imagej.net/ij/index.html

Using the above linked ImageJ/FIJI macro saved locally, you can Run or Edit (I find running it in Edit mode to work better, and you can see the full comments as well) the macro from the Plugins > Macros drop-down menu. Running this will open a dialog box where you can specify your input directory ("01_originals" in my case) and the destination output directory for all processed images (I name mine "02_preprocessed"). You can also input the names and desired display colors for each microscope channel. These normally correspond to the various stains we use to label cells and cellular structures (e.g. DAPI is a common dye shown in blue that labels cell nuclei), and it is important for a multichannel aka multi-color images (4 channels here) to be displayed such that each different stain is in a different color, so each color is informative about cell phenotype (for instance, the genes and/or proteins expressed by this cell) in some way. This differs for each specific experiment and is part of the standard immunohistochemistry/immunofluorescence experimental design that results in the microscope images we are starting with for this computational pipeline, so a more detailed discussion is out of the scope of this sample repo.

<img width="835" alt="FIJI_01_Edit_Macro" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/5c2be463-45f9-4a01-850d-c238a8d33203">

After you have selected your directories and image channel names and colors of choice, and click OK, a log will display of all the files in your directory sequentially that will be processed, and the macro will open each file one-by-one.

<img width="816" alt="FIJI_03_Macro_dialog" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/08704cfa-8802-4ea5-8fdd-2a344bd600ee">

As is standard when opening a file in ImageJ/FIJI, a "Bio-Formats Import Options" dialogue box will open. As indicated in the macro script usage notes, you should (1) open all files as Hyperstacks with Color mode: Default, and only Autoscale checked, (2) DO NOT split channels or focal planes (3) double-check that input filenames DO NOT have spaces. Then click OK and wait.

<img width="903" alt="FIJI_04_Open_BioFormats" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/f64b5ca8-8ab6-4363-aa18-8735177a778b">

You will then see the macro open each of the channels of the first image in your directory, and perform an automatic color adjustment across each of the channels. Importantly, this keeps the contrast of all of your channels and all of your images consistent for the entire analysis batch.

Once that is completed, a dialogue box will appear letting you know how to go about rotating the image if necessary depending on the orientation of the tissue on the microscope slide. After you acknowledge, the FIJI Rotate dialogue box will appear and will select one of the channels for you to interactively adjust the rotation. After you click OK, this action will automatically repeat on all of the channels of the image. As prompted, you should not adjust the rotation (as that will create an inconsistency among all of the channels and they will not overlay properly), but click ok on the subsequent dialog boxes, making sure that [X] Enlarge image remains checked.

<img width="744" alt="FIJI_06_BETTER_FIJI_Rotate_withImage" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/25c3c890-0b90-49bf-a02a-0104388e75e4">

Next you will see your composite image appear with all the channels appearing together in the colors you specified earlier. A "Visual inspection approval" dialogue box will appear askign you to check that this image looks good for quantification as-is.
- If it looks good (and isn't a huge image! there is often no need to quantify an entire image when a representative column will suffice), keep "Looks good. Proceed" and click OK. This set of images will be saved to your output directory and you will then be taken through the same process with the rest of your images in your input directory.
- If you would like to make the region for analysis smaller, or crop out part of the image that has been damage or should otherwise be excluded (in this case, some of the tissue on the right side is a little out-of-focus, shown by the black spaces that are out of the imaging plane of the microscope), select "I'd like to crop to an ROI."
-   This will pull up the FIJI ROI Manager. You can then select the region you want to crop to on the composite image (yellow bounding box), and then press "t" or "Add" on the ROI Manager dialogue box. Once you press OK, the cropped region will be applied to all the channels of the image and those will be saved to your output folder. You will see all the images open and close while the macro is saving them, but you do not need to do anything.
- If there are problems with this image that make it not a good canditate for quantification, you can select "Not good. Next image." and the macro will not save any of these images but will take you to the next file to process.

<img width="724" alt="FIJI_07_Visual_inspection_approval_withImage_toCrop" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/551b42b3-76ae-4886-a6c1-bc7f1a2eb09a">

<img width="986" alt="FIJI_08_Crop" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/47398593-f2ae-4522-9c2b-f6114b5e4d14">

If there are more images in the input directory to process, the macro will repeat this process until it reaches the end of the file list.

### Outputs
The outputs generated in your output directory ("02_preprocessed") will then be a total of 12 files (assuming a 4-channel input file, which is what is being demonstrated here. I have alternate versions of this pipeline for 2- or 3-channel images):
- 4 single-channel grayscale images of each channel (e.g. DAPI, green, red, far-red)
- 4 two-channel colorized images of the green channel vs. other stains for quantification (more on this later...)
- 2 three-channel images
- 2 four-channel images

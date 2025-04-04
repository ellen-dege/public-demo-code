# Image Analysis Code

## Introduction
This repo provides a sample of some code written during my PhD to provide biologists with a more streamlined way to handle microscope images for quantification of specific information about the cells in those images.

In this particular example, code was used for analysis of data generated as part of the published work: [Qian, DeGennaro et al. Developmental Cell 2022 "Loss of non-motor kinesin KIF26A causes congenital brain malformations via dysregulated neuronal migration and axonal growth as well as apoptosis"](https://www.sciencedirect.com/science/article/pii/S1534580722006815)

To answer a biological question about the effect our gene of interest was having on cells in the developing mouse brain, developmental biologists use the position of cells in the vertical direction within the layers of the brain as one metric of brain health. Cells that are not migrating properly will not be found in the developmentally-appropriate layer of the brain. We also use methods that stain specific proteins with developmentally significant functions within cells, such that certain types of cells will be labeled with a color indicating that they express a certain protein of interest.

This data can be easily assessed qualitatively, by looking at a microscope image taken of a thin cross-section of a brain, however quantitative measurements can be challenging and time-consuming to obtain for large numbers of images over many biological and technical replicates. Furthermore, many labs rely on repitive manual manipulations to process these images, with little or no assistance from software developed specifically for the purpose of quantifying microscopy image data, and with significant individual variation across researchers performing the same quantification.

To address this problem, I developed a pipeline that would transform the raw microscopy imaging data into the same consistent format enabling easy manual quantification of cells and their positions. This workflow makes use of macros I wrote within the popular [ImageJ or FIJI software](https://imagej.net/ij/index.html), as well as a custom python script to process the software output. Using this pipeline drastically reduces the analysis time for the researcher, and standardizes the image inputs for subsequent documentation, storage, and publication.

## Full workflow

The full image analysis protocol:
1. [Obtain microscope images](https://github.com/ellen-dege/public-demo-code/tree/main/image_analysis_code#1-obtain-microscope-images)
2. [Pre-process images](https://github.com/ellen-dege/public-demo-code/tree/main/image_analysis_code#2-pre-process-images)
3. [Assemble multi-channel images for counting](https://github.com/ellen-dege/public-demo-code/tree/main/image_analysis_code#3-assemble-multi-channel-images-for-counting)
4. [Blind filenames](https://github.com/ellen-dege/public-demo-code/tree/main/image_analysis_code#4-blind-filenames)
5. [Manually count cells in FIJI and save results](https://github.com/ellen-dege/public-demo-code/tree/main/image_analysis_code#5-unblind-images-and-analyze-results)
6. [Unblind images and analyze results](https://github.com/ellen-dege/public-demo-code/tree/main/image_analysis_code#6-unblind-images-and-analyze-results)

Accordingly, my working directories within the parent folder for this workflow are named:
- 01_originals
- 02_preprocessed
- 03_channels_for_multis
- 04_multis_to_analyze
- 05_blinded
- 06_results
- exclude_from_analysis

In the below sections, I will expand in detail on the protocol steps for which I developed code and/or a detailed workflow in FIJI.

### 1. Obtain microscope images

Once you have obtained your microscopy image files (e.g. in .czi format as from Zeiss microscopes) and backed them up, a copy of good images for analysis should be located in a single directory. I name this directory "01_originals". Before running, you'll want to check that all your input files have no spaces in them! My ImageJ/FIJI macros do not tolerate this. I also find that using a standard, informative naming convention for microscopy files is very helpful within the same experiment or experiment type.

### 2. Pre-process images
Using the [above linked ImageJ/FIJI macro](https://github.com/ellen-dege/public-demo-code/blob/main/image_analysis_code/KIF_FIJImacro_image_preprocessing.ijm), you can **Run** or Edit (I find running it in Edit mode to work better, and you can see the full comments as well) the macro from the **Plugins > Macros** drop-down menu.

<img width="835" alt="FIJI_01_Edit_Macro" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/5c2be463-45f9-4a01-850d-c238a8d33203">

Running this will open a dialog box where you can specify your **input directory** ("01_originals" in my case) and the destination **output directory** for all processed images (I name mine "02_preprocessed")
- Importantly the output folder cannot be nested within the input folder.
- You can also input the names and desired display colors for each microscope channel. These normally correspond to the various stains we use to label cells and cellular structures (e.g. DAPI is a common dye shown in blue that labels cell nuclei), and it is important for a multichannel aka multi-color images (4 channels here) to be displayed such that each different stain is in a different color, so each color is informative about cell phenotype (for instance, the genes and/or proteins expressed by this cell) in some way. This differs for each specific experiment and is part of the standard immunohistochemistry/immunofluorescence experimental design that results in the microscope images we are starting with for this computational pipeline, so a more detailed discussion is out of the scope of this sample repo.

<img width="816" alt="FIJI_03_Macro_dialog" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/08704cfa-8802-4ea5-8fdd-2a344bd600ee">

After you have selected your directories and image channel names and colors of choice, and click OK, a log will display of all the files in your directory sequentially that will be processed, and the macro will open each file one-by-one.

As is standard when opening a file in ImageJ/FIJI, a **"Bio-Formats Import Options" dialogue box will open**. As indicated in the macro script usage notes, you should:
1. Open all files as Hyperstacks with Color mode: Default, and only Autoscale checked.
2. DO NOT split channels or focal planes.
3. Double-check that input filenames DO NOT have spaces.
Then click OK and wait.

<img width="903" alt="FIJI_04_Open_BioFormats" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/f64b5ca8-8ab6-4363-aa18-8735177a778b">

You will then see the macro open each of the channels of the first image in your directory, and perform an automatic **color adjustment** across each of the channels. Importantly, this keeps the contrast of all of your channels and all of your images consistent for the entire analysis batch.

Once that is completed, a dialogue box will appear letting you know how to go about **rotating the image if necessary** depending on the orientation of the tissue on the microscope slide.
- After you acknowledge, the FIJI Rotate dialogue box will appear and will select one of the channels for you to interactively adjust the rotation.
- After you click OK, this action will automatically repeat on all of the channels of the image.
- As prompted, you should not adjust the rotation (as that will create an inconsistency among all of the channels and they will not overlay properly), but click ok on the subsequent dialog boxes, **making sure that "Enlarge image" remains checked.**

<img width="744" alt="FIJI_06_BETTER_FIJI_Rotate_withImage" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/25c3c890-0b90-49bf-a02a-0104388e75e4">

Next you will see your composite image appear with all the channels appearing together in the colors you specified earlier. A "Visual inspection approval" dialogue box will appear askign you to check that this image looks good for quantification as-is.
- **If it looks good** (and isn't a huge image! there is often no need to quantify an entire image when a representative column will suffice), keep "Looks good. Proceed" and click OK.
  - This set of images will be saved to your output directory and you will then be taken through the same process with the rest of your images in your input directory.
  - Keep in mind that even if the entire field of view looks good, for some experiments you will only need to quantify a small, representative field of view, so you may want to crop anyway.
- **If you would like to make the region for analysis smaller**, or crop out part of the image that has been damaged or should otherwise be excluded (in this case, some of the tissue on the right side is a little out-of-focus, shown by the black spaces that are out of the imaging plane of the microscope), select "I'd like to crop to an ROI."
  - This will pull up the FIJI ROI Manager.
    - You can then select the region you want to crop to on the composite image (yellow bounding box), and then press "t" or "Add" on the ROI Manager dialogue box.
    - Once you press OK, the cropped region will be applied to all the channels of the image and those will be saved to your output folder.
    - You will see all the images open and close while the macro is saving them, but you do not need to do anything.
- **If there are problems with this image** that make it not a good canditate for quantification, you can select "Not good. Next image." and the macro will not save any more of these images but will take you to the next file to process. It will still save single-channel images which you should manually relocate to a separate directory (e.g. "exclude_from_analysis"). I prefer to do this rather than deleting these files to serve as an extra record of which samples were excluded.

<img width="724" alt="FIJI_07_Visual_inspection_approval_withImage_toCrop" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/551b42b3-76ae-4886-a6c1-bc7f1a2eb09a">

<img width="986" alt="FIJI_08_Crop" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/47398593-f2ae-4522-9c2b-f6114b5e4d14">

If there are more images in the input directory to process, the macro will repeat this process until it reaches the end of the file list.

#### Outputs
The outputs generated in your output directory ("02_preprocessed") will then be a total of 12 files (assuming a 4-channel input file, which is what is being demonstrated here).
- 4 single-channel grayscale images of each channel (e.g. DAPI, green, red, far-red)
- 4 two-channel grayscale and colorized RGB images of the green channel vs. each of the two other color stains for quantification (see below)
- 2 three-channel images (grayscale multichannel and single merged RGB image)
- 2 four-channel images (grayscale multichannel and single merged RGB image)

I have alternate versions of this pipeline for 2- or 3-channel images, but the full 4-channel macro code should be easily modifiable to your own needs. This pipeline also defaults to the 4th channel (in blue) being a nuclear stain not used for quantification (hence only two pairs of two-channel images output).

The purpose of saving all the single-channel grayscale images is to ensure that any combinations of all channels that you would like to combine or recolor will be easily found for downstream processing and publication.

### 3. Assemble multi-channel images for counting

*If you only want to quantify the vertical positioning of cells in a single channel, then you can skip this step and use only multichannel images going forward.*

In addition to the vertical position of cells within the brain tissue, we gain information about a cell based on what color channel stain that cell is labeled with in our microscope image, which was part of the experimental workflow prior to image analysis. For analysis, the goal is then to look at the number of cells in our experimental condition (here, in the green channel) which are co-labeled for other colors. There are several methods of analyzing this in fully or semi-automated fashion within ImageJ/FIJI and other platforms (one I highly recommend is [CellProfiler](https://cellprofiler.org/)), but for some datasets, manual counting can be more reliable and more efficient.

To simplify the manual counting process, my pipeline automatically generates image stacks which can easily be scrolled through in ImageJ/FIJI. These image stacks contain 3 layers: two single-channel images as the first and third images in the stack, with the merged, colorized image of those two channels together in the middle of the stack. This allows the scientist doing the counting to quickly scroll between single and multi-channel versions of the same image making it easy to confirm that the same cell is labeled with both color channels, as opposed to cells that are only labeled by one color channel.

**This uses the above [Assemble Multi Stack](https://github.com/ellen-dege/public-demo-code/blob/main/image_analysis_code/03_assemble_multi_stack.ijm) macro.**

**First, copy the relevant single channel and two-channel RGB images from "01_preprocessed" into "03_channels_for_multis"**, only including the channels you want to count in colors that are easy for you to see. In this example, I will have three single-channel images, in green, red, and far-red, and then two corresponding two-channel RGB images for the pairs of these three channels that I want to compare (green+red and green+far-red) since the green channel contains our gene of interest in this experiment, so a total of 5 versions of this one microscope image.

When you run the macro in ImageJ/FIJI, you will again be prompted to select the local of an input and output directory.

<img width="457" alt="FIJI_09_multi_stack_in_out_dir" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/3c683512-d781-4605-822b-e32435c1b2c1">

After you select the directories and click OK, you will see your images quickly load and then form a stack in a single window. You will then be prompted to **use the FIJI sorter tool** (using the \< or \> arrows) to sort the colorized image to be at the center of the stack (I find this to be the most helpful position for quick counting).

If the FIJI sorter tool window (on the left in the below screenshot) does not appear at first, check for it behind other windows or on other monitors if you have multiple - it will be open but may be hidden.

<img width="677" alt="FIJI_10_sort_nice_selection_with_image_and_dialogues" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/b798269c-7f66-497c-a9bb-6c92bce3e66b">

When you have done this, the trackbar at the bottom of the image will be in the middle when you're viewing the multichannel RGB image (see screenshot). Then **press OK and the macro will save this stack**, and prompt you to do the same for all other stacks and image sets in the directory. A log window will also open to show you the list of saved files after they have completed.

The goal for counting is to be able to scroll or use the arrowkeys in FIJI to quickly toggle between the single and multi-channel images to help identify cells that are clearly labeled in both conditions, as you can see in the gif below.

![FIJI_switch_between_channels_trimmed02](https://github.com/ellen-dege/public-demo-code/assets/46907273/990528ba-bc4f-40e1-af4a-b45eb1d73cd4)


### 4. Blind filenames

To prevent unconscious bias during cell counting, I use the helpful **[Blind Analysis](https://github.com/quantixed/imagej-macros#blind-analysis) macro from [quantixed](https://github.com/quantixed)** and save the resulting .tifs and key to my "05_blinded" folder.

Note that if you analyze your images in multiple batches (a good approach for a large dataset) you should have separate blinded directories for each batch as the blind naming will restart at 0001 each time you run it.

This step can also be performed earlier in this workflow if the microscopist has not included experimental conditions in the filenames and the person counting cells is not the same as the person doing the microcopy.

### 5. Manually count cells in FIJI and save results

To count the cells in FIJI, I use the **Multi-point Tool** on the toolbar. Dobule-click the Multi-point tool icon to show the multi-tool options. A good rule of thumb is to use the same counter number as the slice that you're counting, otherwise it defaults to all points being assigned to Counter=0. Using different counters for each layer is critical if you want to count cells in each of the conditions, but not if you only want the cell positions of a single channel.

<img width="618" alt="FIJI_11_multitool" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/03b221e5-aac9-4409-9cb4-68fee0eca46e">

**Simply click on a cell to add a point to the counter.** Each point will appear on the associated image stack layer that you are viewing when you click, so keep in mind that it may become crowded with points as you go, especially if all points appear on all layers. You can click to drag points out of the way if needed, but the macro records the positioning of each point so it is important to keep them somewhat centered within the cell body. 

<img width="290" alt="FIJI_11_multitool_options" src="https://github.com/ellen-dege/public-demo-code/assets/46907273/2d2d5031-df36-4339-af8f-61ce4b51615f">

To **save your results**, you will want to save a copy of the image itself (will save with the counters) as a .tiff, which I normally do in a "results" directory within "05_blinded". Then if you haven't already, press 'm' or command+'m' (or from the dropdown menu, select Analyze > Measure) to display the counters for each point. You can then save this table as a text file in the same results folder. I use the format results_00NN.txt to match the image filename.

### 6. Unblind images and analyze results

With the log.txt and results_00NN.txt files as inputs, you can now use the above **[Cell Position Analysis python script](https://github.com/ellen-dege/public-demo-code/blob/main/image_analysis_code/KIF_laminar_dist_analysis03.ipynb)** to quantify the vertical location of the cells in your tissue. This sample only looks at the vertical position of cells in one single microscope image channel across 4 different conditions, but this can also be done across the different stained color channels or within sub-populations of cells that were labeled by multiple overlapping channels.

# References and related links
- [ImageJ/FIJI documentation](https://imagej.net/ij/index.html)
- [CellProfiler](https://cellprofiler.org/)
- [Blind Analysis macro](https://github.com/quantixed/imagej-macros#blind-analysis)
- [Helpful and informative image analysis forum](https://forum.image.sc/)
- [Qian, X., DeGennaro, E.M., et al., 2022. Loss of non-motor kinesin KIF26A causes congenital brain malformations via dysregulated neuronal migration and axonal growth as well as apoptosis. Developmental Cell, 57(20), pp.2381-2396.](https://www.sciencedirect.com/science/article/pii/S1534580722006815)

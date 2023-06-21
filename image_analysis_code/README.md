# Image Analysis Code

This repo provides a sample of some code written during my PhD to provide biologists with a more streamlined way to handle microscope images for quantification of specific information about the cells in those images.

In this particular example, code was used for analysis of data generated as part of the published work: Qian, DeGennaro et al. Developmental Cell 2022 "Loss of non-motor kinesin KIF26A causes congenital brain malformations via dysregulated neuronal migration and axonal growth as well as apoptosis" https://www.sciencedirect.com/science/article/pii/S1534580722006815

To answer a biological question about the effect our gene of interest was having on cells in the developing mouse brain, developmental biologists use the position of cells in the vertical direction within the layers of the brain as one metric of brain health. Cells that are not migrating properly will not be found in the developmentally-appropriate layer of the brain.

This can be easily assessed qualitatively, by looking at a microscope image taken of a thin cross-section of a brain, however quantitative measurements can be challenging and time-consuming to obtain for large numbers of images over many biological and technical replicates.

To address this problem, specifically with 31 images from different animals across 4 different experimental conditions, I developed a pipeline that would transform the raw microscopy imaging data into the same consistent format enabling easy manual quantification of cells and their positions using ImageJ or FIJI software and a custom python script to process the software output, drastically reducing the analysis time for the researcher, and standardizing the image inputs for subsequent publication.


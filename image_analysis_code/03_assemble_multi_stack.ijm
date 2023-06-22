//MakeStackforCounting v2

// This macro will take in single-channel grayscale tifs and their RGB colorized merge (as previously processed by
// AdjColorBal4chMultipleMerge06) and arrange them into an image stack for easier quantification.
//There should be 3 single-channel images, Ch2only, Ch3only, and Ch4only, and two colorized RGB merged images,
//for a total of 5 input images per imaged section.

////Author: Ellen DeGennaro
//January 11, 2021
//Updated 4/29/21

//TODO:
//	-Make more invariant: tolerate different filenames
//	-Look at all files and group according to animal ID, etc., then sort
//	-Enable user choice/make different version to handle 3ch input images > 2ch stack

#@ File (label = "Input directory", style = "directory") indir
#@ File (label = "Output directory", style = "directory") outdir

//let's roll
modifyImages();

function modifyImages() {
      //print("getting list");
      list = getFileList(indir);
      n = list.length;
   	  if ((n%5)!=0)
         exit("The number of files must be a multiple of 5");
      //print(indir);

      //print("entering for loop");
      for (i=0; i<n; i+=5) {
          showProgress(i+1, n/5);
          im1=list[i];
          im2=list[i+1];
          im3=list[i+2];
          im4=list[i+3];
          im5=list[i+4];

          //check filenames
          	//want to make sure that filenames are correct so that channels get sorted appropriately
          
		  ////////////
          //make red channel stack with images 1, 3, and 4
		  ////////////
          open(indir+"/"+im1);
          open(indir+"/"+im3);
          open(indir+"/"+im4);

          formatloc = indexOf(im1, "_2ch");
		  newname = substring(im1, 0, formatloc);

		  //use filenames as stack names
		  //do not keep original images
          run("Images to Stack", "name=RedStack title=[] use");

          //then ask user to sort the colorized image into the middle of the stack
          run("Stack Sorter");
		  waitForUser("Please use the sorter tool at the left to sort the colorized image to be in the center of the stack \nPress 'OK' when finished.");
		 
		  selectWindow("RedStack");
		  saveAs("tiff", outdir+"/"+newname+"_Redmultichannel");
		  print("Saved "+outdir+"/"+newname+"_Redmultichannel");

		  ////////////
		  //now the same but for 647 stack with images 2, 3, and 5
		  ////////////
		  open(indir+"/"+im2);
          open(indir+"/"+im3);
          open(indir+"/"+im5);

          formatloc = indexOf(im1, "_2ch");
		  newname = substring(im1, 0, formatloc);

		  //use filenames as stack names
		  //do not keep original images
          run("Images to Stack", "name=FarRedStack title=[] use");

          //then ask user to sort the colorized image into the middle of the stack
          run("Stack Sorter");
	  	  waitForUser("Please use the sorter tool at the left to sort the colorized image to be in the center of the stack \nPress 'OK' when finished.");
		 
		  selectWindow("FarRedStack");
		  saveAs("tiff", outdir+"/"+newname+"_FarRedmultichannel");
		  print("Saved "+outdir+"/"+newname+"_FarRedmultichannel");

		  close("*");//closes all image windows
      }
  }

//print("Processing Complete!");
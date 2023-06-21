//AdjustColorBalance_4channel_MultipleMerge v6

//Usage:
//  This FIJI macro will take inputs of directories of 4 channel 8 or 16-bit images, auto-adjust color, and
//  merge into multiple sets: individual 8-bit grayscale images, 2-, 3-, and 4-channel colorized images.

//Purpose:
//  For standardized and easier downstream manipulation (e.g. cell counting, image publication)
//  Saves to a different, specified output folder (cannot be nested in the input folder).

//Author: Ellen DeGennaro
//January 4, 2021

//Usage notes:
//	-Open all files as Hyperstacks with Color mode: Default, and only Autoscale checked
//	-DO NOT split channels or focal planes
//	-Make sure input filenames DO NOT have spaces

//Updates:
//4/28/21:
//	-changed the order of channel splitting so that ROI doesn't need to be applied to each individual channel
//	-updated variable names to be more invariant, and ask for user to input
//	-for false-color images, saves both RGB and channel versions
//	-cleaned up code significantly with functions
//	-incorporated image rotation (to allow for easier laminar quantifications)
//	-added dropdown for how to do the false coloring

//TODO:
//1) Handle 3ch inputs with user specification
//2) Enable handling of image stacks (z)
//3) Include a flag for saving image subsets to a separate folder
//4) Save image rotation degree as metadata
//5) Ask user which channel they want to use to determine rotation

//////////////

//////
// SET UP FIRST DIALOG BOX
//////

#@ File (label = "Input directory", style = "directory") indir
#@ File (label = "Output directory", style = "directory") outdir
#@ string (label = "Saturation value (default = 0.35)") satset

#@ string (label = "Number of channels in all images") numch; //doesn't do anything yet

#@ string (visibility=MESSAGE, value = "Please specify how each channel will be saved. \nProvide names for filenames and false coloring for multichannel images.");
#@ string (label = "Channel 1 name:") ch1name
#@ string (label = "Channel 1 color:", choices={"red","green","blue","gray","cyan","magenta","yellow"}) chosen1
#@ string (label = "Channel 2 name:") ch2name
#@ string (label = "Channel 2 color:", choices={"red","green","blue","gray","cyan","magenta","yellow"}) chosen2
#@ string (label = "Channel 3 name:") ch3name
#@ string (label = "Channel 3 color", choices={"red","green","blue","gray","cyan","magenta","yellow"}) chosen3
#@ string (label = "Channel 4 name:") ch4name
#@ string (label = "Channel 4 color", choices={"red","green","blue","gray","cyan","magenta","yellow"}) chosen4
//#@ string  (label = "Set minimum displayed value (recommend = 4000") minval
//#@ string  (label = "Set maximum displayed value (recommend = 15,000)") maxval
//maxval is 65535 for 16-bit images and 255 for 8-bit images
//#@ indicates a parameter will be asked for with a GUI
	//first term indicates data type
	//in parenthesis, label string is set to what the GUI will display
	//last term is the variable that the user input will be stored in
	//notably you shouldn't include semicolons after these
	// refer to: https://imagej.net/Script_Parameters




//////
// FUNCTION DEFINITIONS
//////

//based on user input, encode false coloring according to FIJI
	//C1 = red
	//C2 = green
	//C3 = blue
	//C4 = gray
	//C5 = cyan
	//C6 = magenta
	//C7 = yellow
function convertFalseColors(desiredColor){
	if (desiredColor=="red"){
		return "c1";
	}
	if (desiredColor=="green"){
		return "c2";
	}
	if (desiredColor=="blue"){
		return "c3";
	}
	if (desiredColor=="gray"){
		return "c4";
	}
	if (desiredColor=="cyan"){
		return "c5";
	}
	if (desiredColor=="magenta"){
		return "c6";
	}
	if (desiredColor=="yellow"){
		return "c7";
	}
}

function colorBalance(chad) {
	selectWindow(chad);
	run("8-bit");
	run("Color Balance...");
	resetMinAndMax();
	run("Enhance Contrast", "saturated="+satset);
	//setMinAndMax(minval, maxval);
	run("Apply LUT");
}

//nn is newname from for loop
function multipleMergeSave(orig, one, two, three, four, nn, wasCropped, wasRotated){

	basename = outdir+"/"+nn;

	append = "";
	if(wasRotated==1){
		append += "_rotated";
	}
	if(wasCropped==1){
		append += "_cropped";
	}

	//3 channels (no DAPI)
	//C5 (cyan) = ch2
	//C6 (magenta) = ch4
	//C7 (yellow) = ch3
	run("Merge Channels...", false2+"="+two+" "+false4+"="+four+" "+false3+"="+three+" keep create");
	saveAs("tiff", basename+"_ColorAdj_3ch_"+ch2name+"-cyan_"+ch3name+"-yellow_"+ch4name+"-magenta"+append);
	run("RGB Color");
	saveAs("tiff", basename+"_ColorAdj_3ch_RGB_"+ch2name+"-cyan_"+ch3name+"-yellow_"+ch4name+"-magenta"+append);

	//first pair - comparing each to ch2
	//C5 (cyan) = ch2
	//C7 (yellow) = ch3
	run("Merge Channels...", false2+"="+two+" "+false3+"="+three+" keep create");
	saveAs("tiff", basename+"_ColorAdj_2ch_"+ch2name+"-cyan_"+ch3name+"-yellow"+append);
	run("RGB Color");
	saveAs("tiff", basename+"_ColorAdj_2ch_RGB_"+ch2name+"-cyan_"+ch3name+"-yellow"+append);

	//second pair
	//C5 (cyan) = ch2
	//C6 (magenta) = ch4
	run("Merge Channels...", false2+"="+two+" "+false4+"="+four+" keep create");
	saveAs("tiff", basename+"_ColorAdj_2ch_"+ch2name+"-cyan_"+ch4name+"-magenta"+append);
	run("RGB Color");
	saveAs("tiff", basename+"_ColorAdj_2ch_RGB_"+ch2name+"-cyan_"+ch4name+"-magenta"+append);

	//aaaaaand all 4 again
	//C3 (blue) = ch1
	//C5 (cyan) = ch2
	//C6 (magenta) = ch4
	//C7 (yellow) = ch3
	run("Merge Channels...", false1+"="+one+" "+false2+"="+two+" "+false4+"="+four+" "+false3+"="+three+" keep create");
	saveAs("tiff", basename+"_ColorAdj_4ch_"+ch1name+"-blue_"+ch2name+"-cyan_"+ch3name+"-yellow_"+ch4name+"-magenta"+append);
	run("RGB Color");
	saveAs("tiff", basename+"_ColorAdj_4ch_RGB_"+ch1name+"-blue_"+ch2name+"-cyan_"+ch3name+"-yellow_"+ch4name+"-magenta"+append);
}

//Make a Dialog box for user to be able to approve color balanced image, then choose to rotate, crop an ROI, etc.
//from https://imagej.net/Generic_dialog
Dialog.create("Visual inspection approval");
Dialog.addMessage("Please verify that the 4-channel looks OK (channel intensities, ROI, etc.) before proceeding.");
Dialog.addMessage("Click cancel to stop processing all images in set.");
	
//Dialog.addCheckbox("Looks good. Proceed.", true);
Dialog.addChoice("Action:", newArray("Looks good. Proceed.","I'd like to crop to an ROI.","Not good. Next image."));

//////
//Set up and check false coloring scheme
//////

false1 = convertFalseColors(chosen1);
false2 = convertFalseColors(chosen2);
false3 = convertFalseColors(chosen3);
false4 = convertFalseColors(chosen4);
//defaults should be (DAPI, cyan, yellow, magenta)
//false1 = "c3";
//false2 = "c5";
//false3 = "c7";
//false4 = "c6";


//throw an error if any of the channel colors are set to be the same
if (chosen1==chosen2||chosen1==chosen3||chosen1==chosen4||chosen2==chosen3||chosen2==chosen4||chosen3==chosen4){
	exit("ERROR: Two or more false colors are the same. Please choose unique colors.");
}





//////
// OPEN FILES AND ENTER FOR LOOP to operate on each image
//////

//print("getting file list");
list = getFileList(indir);
n = list.length;
//print(indir);

//print("entering for loop");
for (i=0; i<n; i++) {
	showProgress(i+1, n);
	currim=list[i];
	print(currim);
	open(indir+"/"+currim);

	//finds the location of the file format in the original file
	formatloc = indexOf(currim, ".");
	//then saves just the filename
	newname = substring(currim, 0, formatloc);

	//initialize
	cropped = 0;
	rotated = 0;

	//first need to split channels so you can adjust each
	//may not need to split them
	//but later it's easier to crop an ROI and rotate on the fully merged image, then split and save
	run("Split Channels");

	ch1 = "C1-"+currim;
	ch2 = "C2-"+currim;
	ch3 = "C3-"+currim;
	ch4 = "C4-"+currim;

	//run color balance on each of the images
	colorBalance(ch1);
	colorBalance(ch2);
	colorBalance(ch3);
	colorBalance(ch4);
	
	//close color adjust panel
	run("Close");

	//first rotate images - need to do on individual channels
	showMessageWithCancel("Please rotate the image. Use bilinear interpolation and NO background fill. \nIt is very important to CHECK ENLARGE IMAGE.\n\nYou may use the preview and add as many gridlines as are helpful.\nThe same rotation will be applied to all channels.");
	selectWindow(ch1);
	run("Rotate... ");
	run("Remove Overlay");
	//would be great to save but this is too hard for now
	saveRotation = getValue("rotation.angle");
	print("Rotated "+saveRotation+" degrees");

	showMessageWithCancel("Repeating rotation on all channels...\nNo need to change any settings. Make sure 'Enlarge image' remains checked.");

	//repeat on other 3 channels
	selectWindow(ch2);
	run("Rotate... ");
	run("Remove Overlay");

	selectWindow(ch3);
	run("Rotate... ");
	run("Remove Overlay");

	selectWindow(ch4);
	run("Rotate... ");
	run("Remove Overlay");
	//if enlarge image is not checked for all, then merges can't happen
	
	rotated = 1;

	//now merge channels back together

	//first all 4
	run("Merge Channels...", false1+"="+ch1+" "+false2+"="+ch2+" "+false4+"="+ch4+" "+false3+"="+ch3+" create");

	//Show Dialog box for user to be able to approve 4ch image before proceeding
	Dialog.show();
		 
	// Once the Dialog is OKed the rest of the code is executed
	// If the user clicks cancel, then no more images will be processed
	//proceed = Dialog.getCheckbox();
	inChoice = Dialog.getChoice();
		
	if (inChoice=="Not good. Next image.") {
		showMessage("Skipped additional channel splitting for this image.");
	}

	if (inChoice=="I'd like to crop to an ROI.") {
		setTool("rectangle");
		run("ROI Manager...");
		waitForUser("Select region for cropping. \nPress 't' then click 'OK' when done.");

		selectWindow(currim);
		run("Crop");
		//saveAs("tiff", outdir+"/"+newname+"_ColorAdj_4ch_405-blue_488-cyan_568-yellow_647-magenta_cropped");
		//print("Saved "+newname+"_ColorAdj_4ch_405-blue_488-cyan_568-yellow_647-magenta_cropped");

		cropped = 1;
	}

	if (inChoice=="Looks good. Proceed.") {
		//if user-verified, select and save all open windows, then continue with other channels

		//full 4-channel image (already merged)
		selectWindow(currim);
		//saveAs("tiff", outdir+"/"+newname+"_ColorAdj_4ch_405-blue_488-cyan_568-yellow_647-magenta");
		//print("Saved "+newname+"_ColorAdj_4ch_405-blue_488-cyan_568-yellow_647-magenta");
	}

	//setBatchMode(true);
	//Batch Mode stops each image from appearing on the screen in a window for faster manipulation

	selectWindow(currim);
	run("Split Channels");

	//have to re-convert each to have no false coloring before merging
	selectWindow(ch1);
	run("8-bit");
	selectWindow(ch2);
	run("8-bit");
	selectWindow(ch3);
	run("8-bit");
	selectWindow(ch4);
	run("8-bit");

	//run multipleMerge
	multipleMergeSave(currim, ch1, ch2, ch3, ch4, newname, cropped, rotated);

	//save single channel images
	app = "";
	if(rotated==1){
		app += "_rotated";
	}
	if(cropped==1){
		app += "_cropped";
	}

	selectWindow(ch1);
	saveAs("tiff", outdir+"/"+newname+"_ColorAdj_1ch_"+ch1name+"Only"+app);
	selectWindow(ch2);
	saveAs("tiff", outdir+"/"+newname+"_ColorAdj_1ch_"+ch2name+"Only"+app);
	selectWindow(ch3);
	saveAs("tiff", outdir+"/"+newname+"_ColorAdj_1ch_"+ch3name+"Only"+app);
	selectWindow(ch4);
	saveAs("tiff", outdir+"/"+newname+"_ColorAdj_1ch_"+ch4name+"Only"+app);
	
	close("*");//closes all image windows
	//setBatchMode(false);
}

//print("Processing Complete!");

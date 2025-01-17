# this example ImageJ/Fiji jython script shows how to apply a
# custom OpenCL kernel to an image which replaces black by 
# white in an image
#
# Author: Robert Haase (@haesleinhuepf)
#         February 2020


from net.haesleinhuepf.clij import CLIJ;
from ij import IJ;
from java.lang import System;
import os;
import inspect

# retrieve the folder where this script is located (thanks to @mountain_man from the ImageJ forum)
filesPath = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))) + "/"

# open an example image
imp = IJ.openImage("https://clij.github.io/clij-benchmarking/plotting_jmh/images/imagesize/clij_ij_comparison_BinaryAnd2D.png");
IJ.run(imp, "RGB Stack", "");
imp.show();
IJ.run(imp, "Make Composite", "display=Composite");

# initialize ClearCL context and convenience layer
time = System.currentTimeMillis();
clij = CLIJ.getInstance();

# convert ImagePlus image to CL images (ready for the GPU)
input = clij.push(imp);
output = clij.create(input);

# apply a filter to the image using ClearCL / OpenCL
parameters = {
	"src":input,
	"dst":output
};
clij.execute(filesPath + "rgbReplaceBlackAndWhite.cl", "rgbReplaceBlackAndWhite", parameters);

# convert the result back to ImagePlus and show it
result = clij.pull(output)
result.show();
IJ.log("The custom kernel execution took " + str(System.currentTimeMillis() - time) + " ms");

IJ.run(result, "Make Composite", "display=Composite");

# clean up
input.close();
output.close();

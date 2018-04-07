# BoostedGcodeCuraPlugin
## What is this?
BoostedGcode.py is a python script to be used as a PostProcessingPlugin script in Cura version 3.2.1  
This plugin handles the communication between Cura and our post processing algorithm deployed in Google Cloud as a cloud function.

## What does it do?
 1. First connects to a Google Cloud function to download script configuration parameters.  
    (These parameters can be changed when you add the post processing script.)
 1. Then it uploads gcode to another Google Cloud function after slicing.
 1. The cloud function does some post processing and returns a post processed version of the gcode.
 1. Cura then writes the post processed gcode into a file.

## Why do you it this way?
 1. Not quite ready to release the algorithm in its source form.
 1. Flexibility to be able to update the post processing algorithm seamlessly.
 1. Support multiple slicers reusing as much as possible of the actual post processing implementation.

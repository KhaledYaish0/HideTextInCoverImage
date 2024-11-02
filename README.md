 The project involves creating a GUI-based steganography tool for hiding secret text within an image using the Least Significant Bit (LSB) technique. The aim is to help users conceal text inside a cover image and later retrieve it.

Key Objectives:

GUI Application: Develop an easy-to-use graphical interface that allows users to interact with images and text for the steganography process.
Hiding Mechanism: Hide secret text within a BMP image using 1, 2, or 3 Least Significant Bits of each pixel.
Restoring Mechanism: Allow the hidden text to be extracted back from the image.
Functional Requirements:
Input Handling:

Allow users to select a BMP image (cover image) and load secret text.
Image format must be .bmp with a size of 800x500 pixels.
User Interface Elements:

Load Image: Button to select and load the cover image.
Split Display:
Cover image area.
Input for secret text.
Resulting image area (image after hiding the text).
Bit Selection: Drop-down or buttons to select the number of LSBs used for hiding (1, 2, or 3).
Control Buttons:
Hide Button: Embed the secret text in the cover image.
Restore Button: Extract the secret text from the modified image.
Save Button: Save the resulting image after hiding text.
Clear Button: Reset the fields.
Hiding Technique:

Implement LSB manipulation for hiding text:
Clear the LSBs of the cover image (based on selection).
Insert secret text bit by bit into the cleared LSBs.
Restoring Process:

Extract the hidden text from the modified image by reading the LSBs.

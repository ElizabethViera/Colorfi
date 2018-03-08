# Colorfi by Elizabeth Viera

This is a developing project for creating photo filters. The eventual goal will be filters with face detection and context-responsive
color analysis. 

This project uses Python Imaging Library (PIL) to request two photos from the user. The first, a traditional photo, is analyzed for color
content and produces a color palette that coordinates (doesn't match exactly!) with the original photo. Then, the program requests an
additional black and white photo and colors it according to the generated color palette. It then merges the two photos. The process creates
a unique piece of art with every generation, since the color palette generation is non-deterministic. The user interface is made using TKinter.

# Metal Phases Analyzer

This application clusters metal phases and outputs the mechanical properties of
each phase. It was developed for researchers from Wroclaw University of Science
and Technology to streamline the analysis of novel amorphous metals they
produce. It is a Data Science postgraduate project by Katarzyna Foszcz at the
Wroclaw University of Economics and Business under the supervision of PhD
Ryszard Zygała.

Special thanks to PhD student Michał Biały, who provided data and field
knowledge for this project ❤️

## How it works

After a sample of amorphous metal is produced, it undergoes nanoindentation
study. A polished metal sample is very precisely indented in a matrix of 15×15
or 10×10 points in distances ranging from 5 to 20 um on a machine *CSM
Instruments NHT²*.

<!-- image_split -->
![Clustering process](amorphous_metals/streamlit/Home/process.svg)
<!-- image_split -->

1. A metal sample under microscope after nanoindentation. Some metal
   phases are visible (not necessarily all, as some may be found under the
   surface).
2. Visualization of metal feature (here HIT, hardness). The analyzer takes
   output file from nanoindentation machine, parses the data and visualizes each
   feature.
3. After clustering (here hierarchical clustering). The analyzer specifies
   values of mechanical properties for each cluster found in the metal sample.

Streamlit application is available [here](https://amorphous-metals.foszcz.co).

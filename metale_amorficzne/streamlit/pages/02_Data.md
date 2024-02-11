## Materials and research methods used in this study

- Zirconium Copper (ZrCu) and Zirconium Titanium (ZrTi) alloys,
- nanoindentation of specifically prepared, polished metal samples in the form
  of thin coins. Indentation was performed on each sample in a matrix of 15×15
  or 10×10 points in distances ranging from 5 to 20 um, force applied ranging
  from 25mN to 200mN.
- data output from nanoindentation machine *CSM Instruments NHT2* comes as .TXT
  file and contains calculations of 21 parameters for each indentation point,

## Analysis Methods and Results

I prepared a parser for output files from the *CSM Instruments NHT2*
nanoindentation machine. Initially I tried classification, but after a while of
trials with decision trees, I realised that in this case clustering should be
performed, as the data in unlabelled.

### Tried methods

- Hierarchical clustering (successful)
- KMeans clustering (semi-successful)
- ChatGPT clustering (not successful)
- OPTICS clustering (not successful)

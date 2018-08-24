>This repository is associated to the paper "A soft matter discovery robot driven by child-like curiosity" by Jonathan Grizou, Laurie J. Points, Abhishek Sharma and Leroy Cronin. A draft version of the paper is [available on Chemarxiv](https://chemrxiv.org/articles/A_Closed_Loop_Discovery_Robot_Driven_by_a_Curiosity_Algorithm_Discovers_Proto-Cells_That_Show_Complex_and_Emergent_Behaviours/6958334) and a brief overview of the scientific approach can be found at https://croningp.github.io/tutorial_icdl_epirob_2017/.

# Dropfactory Analysis

Code to analyse the results of experiments performed on the Dropfactory platform

[![Dropfactory_Station](https://github.com/croningp/dropfactory/raw/master/media/gif/dropfactory_stations_speedup.gif)](https://youtu.be/bY5OoRBJkf0)

## Repository Organization

Folders usage:
- [analysis](analysis) contains script that analyse various aspects of the experiment, it is where we test and develop our analysis before generating the final analysis script and plots in the [figure](figure) folder.
- [csv](csv) is for generating csv files from the datasets extracted in the [datasets](datasets) folder. It is useful if you want to perfom analysis in spreadsheet or send to colleague in a sharteable form.
- [datasets](datasets) is where the data collected from our experiments are gathered, sanitized and stored in a user friendly way. To allow you to reproduce the figures without access to the >500Go data (available upon request), the already processed dataset are available in the [datasets release](https://github.com/croningp/dropfactory_analysis/releases/tag/datasets).
- [figures](figures) contains the exact code used to analayse the data and generate the figures shown in the paper and SI. A bit more information is provided in the next seciton of this README file.
- [properties](properties) is a set of scripts used to infer droplet properties (density, viscocities, and surface tension) from a droplet recipy (the ratio of each oil). See http://www.pnas.org/content/115/5/885 (https://doi.org/10.1073/pnas.1711089115) for more details.
- [utils](utils) contains a set of tools useful across our analysis.

Releases usage for large files:
- The [datasets release](https://github.com/croningp/dropfactory_analysis/releases/tag/datasets) contains the already extracted datasets enabling you to reproduce all the figures.
- The [SI release](https://github.com/croningp/dropfactory_analysis/releases/tag/SI) contains the paper and all supporting information files explaining the working of the system.
- The [video release](https://github.com/croningp/dropfactory_analysis/releases/tag/video) contains supplementary videos in mp4 format and gif format for embedding on github. The video are also [available on youtube](https://www.youtube.com/playlist?list=PLBppiRCztuKo8gxq_kfcYM-5S_A-TlMU1).

## Main results



## Associated repositories

- The robotic platform hardware and code is described at https://github.com/croningp/dropfactory

- The code used to run closed-loop droplet experiments using the curiosity algorithm (and others) is available at https://github.com/croningp/dropfactory_exploration

- The droplet tracking code is available at https://github.com/croningp/chemobot_tools

- Libraries developed to build and control the robotic platform are: [commanduino](https://github.com/croningp/commanduino), [pycont](https://github.com/croningp/pycont), [ModularSyringeDriver](https://github.com/croningp/ModularSyringeDriver), [Arduino-CommandTools](https://github.com/croningp/Arduino-CommandTools), and [Arduino-CommandHandler](https://github.com/croningp/Arduino-CommandHandler)

## Dependencies

This code has been tested under Python 2.7.6 on Ubuntu 14.04 LTS. Despite all our efforts, we cannot guarantee everything will be executable on other OS or Python version.

Aside from the standard libraries, we are using the following libraries. You do not have to install them all, it depends on the task you are performing.

- [numpy](http://www.numpy.org/): Scientific computing in Python.
Version: numpy.__version__ is '1.10.4'

- [scipy](http://www.scipy.org/scipylib/index.html): More scientific computing in Python.
Version: scipy.__version__ is '0.16.1'

- [sklearn](http://scikit-learn.org/): Machine Learning in Python.
Version: sklearn.__version__ is '0.16.1'

- [filetools](https://github.com/jgrizou/filetools) is a simple file management library

- [matplotlib](https://matplotlib.org/) v2.1.1 and [seaborn](http://seaborn.pydata.org/) v0.8.1 for plotting

## Author

[Jonathan Grizou](http://jgrizou.com/) while working in the [CroninGroup](http://www.chem.gla.ac.uk/cronin/).

## License

[![GPL V3](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl.html)

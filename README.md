> This repository is associated to the paper "A curious formulation robot enables the discovery of a novel protocell behavior" by Grizou, J., Points, L. J., Sharma, A. & Cronin, L. (2020) [[PDF in Open Access @ Science Advances]](https://advances.sciencemag.org/content/6/5/eaay4237). An overview of the scientific approach can be found at https://jgrizou.com/projects/chemobot.


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

In the following all section and figure number are related to the [paper](https://github.com/croningp/dropfactory_analysis/releases/download/SI/Dropfactory_v50.pdf) and [SI](https://github.com/croningp/dropfactory_analysis/releases/download/SI/SI_v9.pdf) documents in the [SI release](https://github.com/croningp/dropfactory_analysis/releases/tag/SI).

Within the [figures](figures) folder, you can find:
- [SI](figures/SI) generates all the analysis we could think of for each experimental run, some of those figures are used in section 1.2 and 1.3 (p4-24) of the SI.
- [diff_22_26](figures/diff_22_26) generates the bar plot on the rigth side of Figure 2 of the paper. 
- [dye_release](figures/dye_release) generates the dissolution plot of Figure 6 of the paper, as well as plot for section 1.7 (p29-32) of the SI. See https://youtu.be/zOURJEnbmV4 for the effect of temperature on dye release.
- [exploration](figures/exploration) generates 2D scatter plots showing the range of observation geenrate for each algortihmic run. They are shown on the left side of Figure 2 of the paper. See https://youtu.be/E76t9LMbuts and https://youtu.be/6wPkWJDxN64 for the dynamics of exploration between algortihms.
- [exploration_hull](figures/exploration_hull) generates the exploration analysis using different method, it is used for section 2.2.3 (p102-103) of the SI.
- [speed_distribution](figures/speed_distribution) generates the distribution plots on the top rigth corner of Figure 2 of the paper.
- [stats](figures/stats)
- [temperature_prediction](figures/temperature_prediction) generates the prediction plot of section 1.6 (p27-29) of the SI. See https://youtu.be/zhTeDofB6mk and https://youtu.be/80yAmBkzdmM for the effect of temperature on droplet motion.

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

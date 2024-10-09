# Google Maps Merchant Scraper

## Installation

Clone the repository via:

```
git clone https://gitlab.com/netfm/google_maps_scraper
cd google_maps_scraper
```

To run the program, python, firefox and selenium will need to be installed.

### Python

Install from https://www.python.org/downloads/release/python-3127/. Make sure `pip` is installed alongside python.

### Firefox

This scraper uses the Gecko driver for selenium, which interacts with the firefox driver. Install firefox here https://www.mozilla.org/en-GB/firefox/new/.

### Selenium and Gecko

To install Selenium, run

```
pip install -r requirements.txt
```

from a terminal running within the repositories directory.

Further to this, the selenium gecko driver needs to be installed. The gecko driver can be found at https://github.com/mozilla/geckodriver/releases. Then place it at any location under `$PATH`. To see a list of valid locations, run:

```
echo $PATH
```

### Jupyter Notebooks

A method to view an operate jupyter notebooks will also be required. The easiest way is through VSCode, which can be found here: https://code.visualstudio.com/.

## Usage

Launch VSCode and open the folder containing the repository:

![](readme_images/VSCode_Lauch.png)

Then select `Notebook.ipynb` from the left panel (press `CTRL+B` if it doesn't show).

![](readme_images/VSCode_left_panel.png)

Then follow the instructions in the notebook to use the scraper. 
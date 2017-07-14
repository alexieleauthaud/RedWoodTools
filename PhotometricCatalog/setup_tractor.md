# Tractor Driver Manual

---- 2017-07-11 ----

## Basic Information:

* `Tractor` is a "Probabilistic astronomical source detection & measurement" code written by [Dustin Lang](http://dstn.astrometry.net)
    - In one sentence: it is a magic-box pipeline that transforms pixels from an image into properties of objects in a catalog.
    - `Tractor` is written in C and Python; Python is the interface language.
    - `Tractor` can be found on GitHub [here](https://github.com/dstndstn/tractor)
    - The document of `Tractor` is not perfect yet...but you can find it [here](http://thetractor.org/doc/)

* In case you want to understand the idea behind `Tractor`, you can learn it from the author himself:
    - Dustin's 2012 Princton talk: [PDF slides here](http://cosmology.lbl.gov/talks/Lang_12.pdf)
    - Dustin's 2015 DECaLS talk: [PDF slides here](http://dstn.astrometry.net/talks/2015-03-31-tractor-uw.pdf)
    - Dustin's 2015 LSST talk: [YouTube link here](https://www.youtube.com/watch?v=t06d-hQEo3g)

----

## Road to `Tractor`

* Before we get to run `Tractor` on HSC images, let's setup your working environment.

* The steps are:
    1. Install necessary Unix tools: e.g. C & C++ compiler; necessary libraries.
        - On MacOSX, we recommend you to use `homebrew` to handle all the Unix tools.
    2. Setup Python environment, install necessary libraries: e.g. numpy, scipy, matplotlib, astropy, etc.
        - We recommend you to use `conda` environment to handle python and its libaries.
    3. Download and install the `astrometry.net` library which is required by `Tractor`
    4. Download and install the `Tractor` code
    5. Run the demos provided by `Tractor`.

----

### Tips before we start:

* These are just some random comments, you probably know some of these.

* Try to be comfortable using Terminal and command line tools
    - `iTerm2` is a very nice MacOSX Terminal enulator that can make your life easier.

* Learn to understand what is "shell" and "environment variable"
    - Simply put, the shell is a program that takes your commands from the keyboard and gives them to the operating system to perform.
    - If you have no preference, you can use the default shell, which I believe is [bash](https://gist.github.com/LeCoupa/122b12050f5fb267e75f); I used [zsh](https://github.com/robbyrussell/oh-my-zsh/) for work, feel free to check it out.
    - Either way, we will need to learn how to setup [environmental variables](https://en.wikipedia.org/wiki/Environment_variable) using start-up shell script: e.g. [.bashrc file](https://unix.stackexchange.com/questions/129143/what-is-the-purpose-of-bashrc-and-how-does-it-work) or [.zshrc file](https://github.com/robbyrussell/oh-my-zsh/blob/master/templates/zshrc.zsh-template)
    - The environment variables we need to use include `PATH`, `PYTHONPATH`, `HOME`.

* Pick text/code editor
    - Modern code editors have all kinds of tools/add-ons that can make your life much, much easier...
    - I recommend [Atom editor](https://atom.io), you should find it easy to use, and it has many tools for Python, C, Java, GitHub.
    - In case you just start with Python, you can also try [`Kite`](https://kite.com). Basically it is an interactive cheat sheet for Python.

* You **WILL** encounter all kinds of annoying errors, learn how to read the error and warning message.
    - More importantly, learn how to **Google** error message!
    - [Stack Overflow](https://stackoverflow.com) is another great place you should always visit.

* There are some nice manuals about how to setup up MacOSX for development, they include more details than what I can provide, should be useful at some point.
    - [Mac OS X Setup Guide](http://sourabhbajaj.com/mac-setup/)
    - [Setting Up an Apple Mac for Software Development](http://www.stuartellis.name/articles/mac-setup/)
    - [Mac OS X Dev Setup](https://github.com/nicolashery/mac-dev-setup)
    - [Setting up a Brand New Mac for Development](https://www.taniarascia.com/setting-up-a-brand-new-mac-for-development/)

----

### Backup

* This sounds stupid to say, but **Please make sure your works are properly backuped**
* My strategy is:
    - Use `TimeMachine` to regularly backup everything.
    - Use `Dropbox` to backup codes, figures, documents, drafts, and other crucial files.
    - Use `git` for version control, and backup codes and documents to `GitHub`

----

### Other Softwares

* [SAOImage DS9](http://ds9.si.edu/site/Home.html) is a very useful FITS image viewing tool.
* [Topcat](http://www.star.bris.ac.uk/~mbt/topcat/) is a very useful to deal with catalogs interactively.

----

### Homebrew:

* You should first install:
    1. [XCode](https://developer.apple.com/download/): You need an Apple account, and better install it through App store. Make sure it works for your version of Mac OS X.
    2. [XCode command line tool](https://developer.apple.com/download/more/): Also, you can just type `xcode-select --install` in your terminal.
    3. [XQuartz](https://www.xquartz.org)

* [Homebrew](https://brew.sh): a package manager for Mac OS X
    - Installation is very easy.  You can find a nice [cheat sheet here](http://ricostacruz.com/cheatsheets/homebrew.html)
    - `Homebrew` keeps everything under `/usr/local/bin/` folder. It is better to make sure that this directory is the top one in your `PATH` variable.
        * `PATH` is the most important environmental variable, you should read more [here](https://www.cs.purdue.edu/homes/bb/cs348/www-S08/unix_path.html) or [here](http://www.linfo.org/path_env_var.html)
        * Type: `echo $PATH` will show your current `PATH` variable, you should check to make sure `/usr/local/bin` is before, e.g. `/usr/bin`. Otherwise it may cause confusions later.
    - `brew update` will update the package information
    - `brew search PACKAGE_NAME` will list the relevant pacakges.
    - `brew install PACKAGE_NAME` will install the package.
        * Pay attention to the information it outputs to screen, sometimes it provides very useful suggestions.
    - `brew upgrade` will upgrade the installed packages to the most recent version.

#### Necessary Packages to Install:

* Install basic tools:
    - `brew install wget curl`: To download stuff
    - `brew install git`: Git version control; may need to run `brew link git` to use the `homebrew` version.
* Install C and C++ compiler:
    - `brew install gcc`: This may take a while...
* To install `astrometry.net`:
    - `brew install netpbm cairo libpng libjpeg libzip bzip2 md5sha1sum`
    - `brew install cfitsio`: C library to deal with FITS format file
----

### Conda and Python:

* [Conda](https://conda.io/docs/index.html) is a nice package and enviroment manager for Python and other languages
    - I think you will find it pretty easy to install. Make sure you select the Python version (2 v.s. 3) you need.
    - After installation, you should have a line in your start-up shell script (e.g. `.bashrc` or `.zshrc` file) that put `anaconda` on top of the `PATH` variable:
        ``` bash
        export PATH="/anaconda/bin:"$PATH
        ```
    - You can also test the installation by typing: `which python`.  It should return the python from `anaconda`.
    - Learn the basic from this [test-drive document](https://conda.io/docs/test-drive.html)

#### Necessary libraries to install:

* `conda install pip`: `pip` is also a package manager for Python, sometimes the library we need is not included by `conda`, but we can install it using `pip`.
* `conda install numpy scipy`: [numpy](http://www.numpy.org) and [scipy](https://www.scipy.org) are the fundamental Python libraries for science.
* `conda install matplotlib`: [matplotlib](https://matplotlib.org) is the basic plotting tools.
* `conda install astropy`: [astropy](http://www.astropy.org) is the core package for astronomy
* `pip install --upgrade pyfits`: old python library to handle FITS file, used by `astrometry.net` and `Tractor`.
* `pip install --upgrade emcee`: MCMC sampling code; used by `Tractor`, optional.

----

### Git and GitHub:

* [git](https://www.git-scm.com) is a version controll software.
    - You should be able to use `homebrew` to install, update, and maintain `git`.
    - `brew install git` and `brew link --overwrite git` should do the trick.

* You can find many, many documents that teach you how to use `git`. For example:
    - The official [tutorial videos](https://www.git-scm.com/documentation)
    - The ["Try Git" free interactive course](https://www.codeschool.com/courses/try-git) from CodeSchool

* [github](https://github.com) is one of the largest on-line version control repository.
    - You can learn about the basic function of github from the [official document](https://guides.github.com/activities/hello-world/)
    - Or from the [GitHub Training & Guides YouTube channel](https://www.youtube.com/githubguides)

* There is no better way to learn `git` other than actually using it for your own work.

----

### Astrometry.net:

* [`Astrometry.net`](http://astrometry.net) is another magic box written by Dustin Lang. It is a software for astrometric calibration of astronomical images.
    - Basically,
    - You can find the code on [github](https://github.com/dstndstn/astrometry.net)
    - And the document (which is better than `Tractor`) [here](http://astrometry.net/doc/)

* In case you are interested in the algorithm of `astrometry.net`:
    - You can read this paper [here](https://arxiv.org/abs/0910.2233)
    - Or follow Dustin's 2017 SOFIA talk [here](http://dstn.astrometry.net/talks/2017-05-10-astrometry-nasa.pdf)

#### Installation:

* `Astrometry.net` now can be installed through `homebrew`!!
    - A useful manual can be found [here](https://coreastro.wordpress.com/2016/05/02/installing-astrometry-net/)
    - Before installing `astrometry.net`, you should make sure that you have `pyfits` Python library installed: e.g. `pip install pyfits`
    - Then, in principle, the following commands should help install `astrometry.net`:
        ```bash
        brew tap homebrew/science
        brew install astrometry-net
        ```
    - If everything goes well, you can type `solve-field -h` and see the manual of this function.

* The pre-packaged `astrometry-net` under `homebrew` may have certain issue with the default location for `gsl`, the GNU Scientific Library.
    - Even `homebrew` manages to install `astrometry-net`, `solve-field` may fail.
    - In case `brew install gsl` does not solve this problem. Please try the following method.
    - `brew uninstall --force astrometry-net`
    - `brew install --HEAD astrometry-net`, and ignore any error message.
    - Then do this:
        ``` bash
        cd Library/Caches/Homebrew/astrometry-net--git
        make
        make py
        make extra
        make test
        make install INSTALL_DIR=/usr/local/
        ```

* Link the associated Python library to your `PYTHONPATH` environment variable.
    - Put `export PYTHONPATH=$PYTHONPATH":/usr/local/Cellar/astrometry-net/0.70/lib/python/astrometry` in your `.bash_profile` or `.zshrc` file under your home directory.
    - If you need to do the `brew install --HEAD astrometry-net` step, change the PYTHONPATH to: ```export PYTHONPATH=$PYTHONPATH":~/Library/Caches/Homebrew/astrometry-net--git/```
    - After this, you can test the installation under Python:
        ```Python
        import astrometry
        astrometry.__file__
        ```
    - This should return: `/usr/local/Cellar/astrometry-net/0.70/lib/python/astrometry/__init__.pyc`

----

### Finally, Tractor

* In principle, if everything is prepared, installation of `tractor` should be very simple:
    ```bash
    git clone git@github.com:dstndstn/tractor.git
    cd tractor
    make
    python setup.py install
    ```
    - This should do the trick.
    - You should be able to test the installation by running ```from tractor import *``` under Python

### Run Demos

* If everything goes well, you should be able to run a demo under `tractor` folder called `mog.py`.  Just type, `python mog.py`, you should see the demo is running, and it will output some files.
    - If you are using `Python > 3.0`, you will have error from the above test.

# Comparison of Photometry for Massive Galaxies between HSC and Other Surveys

---- 2017-07-06 ----

## Wide-GAMA09 Region

* We first focus on one of the region covered by the internal S16A data release: Wide-GAMA09

    - RA:  125 to 150 degree
    - Dec: -2.5 to 6.0 degree

* The sky coverage can be found in the following figure:

![alt text](https://github.com/alexieleauthaud/RedWoodTools/blob/master/PhotometricCatalog/figure/s16a_wide_gama09_i.png)

-----

## HSC Catalog:

* The HSC photometric catalogs for massive galaxies can be found [here](https://github.com/alexieleauthaud/RedWoodTools/tree/master/PhotometricCatalog/hsc)
    - We will focus on the one for `Wide-GAMA09` field (`g09`): [This one](https://github.com/alexieleauthaud/RedWoodTools/blob/master/PhotometricCatalog/hsc/hsc_s16a_fastlane_g09_short.fits)
    - The catalog contains **2462** galaxies.

* The HSC survey observs in **five** different filters:
    - From shorter to longer wavelength, they are `g, r, i, z, Y`.

* Useful columns of this table:

| Column                      | Information               | Unit   |
| :--------------------------:|:-------------------------:|:------:|
| `object_id`                 | Unique ID from HSC        |        |
| `ra, dec`                   | Coordinate of object      | degree |
| `a_[g/r/i/z/y]`             | Galactic extinction value | mag    |
| `[g/r/i/z/y]cmodel_mag`     | Magnitude of galaxy       | mag    |
| `[g/r/i/z/y]cmodel_mag_err` | Error of the magnitude    | mag    |
| `z_best`                    | Redshift of galaxy        |        |

* All the observed magnitude need to be corrected for the dust extinction within our own Milky Way.
    - This can be achieved by, e.g. `gcmodel_mag_true` = `gcmodel_mag` - `a_g`

* We also have our own measurements of luminosities within different apertures in the catalog
    - For instance, `lum_100` means the luminosity of the galaxy measured using an elliptical aperture whose major axis length is 100 kpc.
    - These measurements are in unit of "Solar luminosity" ($3.826\times10^{33}$erg/s)
    - With the help of redshift and the absolute magnitude of the sun in the desired filter, we can convert back to observed magnitude.  (Will show how to do that later)

* Please find the Jupyter notebook that demonstrates how to read this catalog: [here](https://github.com/alexieleauthaud/RedWoodTools/blob/master/PhotometricCatalog/notebook/demo_read_fits_catalog.ipynb)

-----

## LegacySurvey Catalog:

* We are now using the "sweep" catalog from LegacySurvey Data Release 3
    - The catalogs can be found [here](http://portal.nersc.gov/project/cosmo/data/legacysurvey/dr3/sweep/3.1/)
    - Please read the description of DECALS catalogs [here](http://legacysurvey.org/dr3/description/)

* Right now, DECALS only has data in three filters
    - They are `g, r, z` bands.
    - Although sharing the same name, the response curves of these filters are slightly different with the HSC ones (We need to deal with them later)

* We are using the following catalogs:
    - `sweep-120m005-130p000.fits`
    - `sweep-120p000-130p005.fits`
    - `sweep-130m005-140p000.fits`
    - `sweep-130p000-140p005.fits`
    - `sweep-140m005-150p000.fits`
    - `sweep-140p000-150p005.fits`

* Need to combine these catalogs and extract useful information
    - The original catalogs are quite large and will not be uploaded here.
    - Please download the catalog from DeCaLs [here](https://www.dropbox.com/s/wturiwmcdj16t3h/decals_dr3_g09_short.fits?dl=0)
    - There are **940172** objects in this catalog
    - **Note that not every object here has useful detection in all three bands.**  For the ones without detection in certain band, the magnitude will become `inf` in Python.

* The useful columns are:

| Column                      | Information               | Unit   |
| :--------------------------:|:-------------------------:|:------:|
| `OBJID`                     | Unique ID from DECALS     |        |
| `TYPE `                     | Object type               |        |
| `RA, DEC`                   | Coordinate of object      | degree |
| `a_[g/r/z]_decal`           | Galactic extinction value | mag    |
| `[g/r/zmag_decal`           | Magnitude of galaxy       | mag    |
| `[g/r/zflux_ivar_decal`     | Inverse variance of flux  |    |

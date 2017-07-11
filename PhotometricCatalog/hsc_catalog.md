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


-----

## Cross-Match using Astropy:

* Please read the instruction [here](http://docs.astropy.org/en/stable/coordinates/matchsep.html)

* We need three components from astropy:
    - `from astropy import units as u`: This is the astropy.unit object; It is pretty easy to use, and you can find more information [here](http://docs.astropy.org/en/stable/units/)
    - `from astropy.coordinates import SkyCoord`: This is the Astropy object for coordinates.  You can read more about it [here](http://docs.astropy.org/en/stable/coordinates/index.html)
    - You still need to load the two catalogs using `astropy.table` and you need to identify the column names for (RA, Dec) in both catalog.
    - And, in case you want to merge the two catalog into one and save it to disk, you need the `hstack` function which merges two catalogs horizontally.
    - Details about the function (or "method" to be precise) that does the cross-match can be found [here](http://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html#astropy.coordinates.match_coordinates_sky)


```python
from astropy import units as u
from astropy.table import Table, hstack
from astropy.coordinates import SkyCoord

# Let's say we match the DECALS catalog to the HSC ones
cat_hsc = Table.read(location_of_hsc_catalog, format='fits')
cat_decals = Table.read(location_of_decals_catalog, format='fits')

# Let's say that the coordinates are stored in these columns:
#  HSC: ra_hsc, dec_hsc
#  DECALS: ra_decals, dec_decals
#  Both of these coordinatess are in unit of degree
coord_hsc = SkyCoord(ra=cat_hsc['ra_hsc'] * u.degree,
                     dec=cat_hsc['dec_hsc'] * u.degree)
coord_decals = SkyCoord(ra=cat_decals['ra_decals'] * u.degree,
                        dec=cat_decals['dec_decals'] * u.degree)

# Let's do the match
index_decals, d2d, _ = coord_hsc.match_to_catalog_sky(coord_decals)

# This will find the nearest neighbor of coord_hsc object in coord_decals
cat_decals_match = cat_decals[index_decals]

# We will only use the ones with distance smaller than, say, 1.0 arcsec
flag_match = (d2d <= 1.0 * u.arcsec)
print("# Find %d matches!" % np.sum(flag_match))

# The matched objects from HSC side
match_hsc = cat_hsc[flag_match]
match_decals = cat_decals_match[flag_match]

# Now you can generate plots to compare the magnitudes
# e.g. plt.scatter(match_hsc['rcmodel_mag'] - match_hsc['a_r'],
#                  match_decals['rmag_decal'] - match_decals['a_r'])

# In case you want to merge the two catalogs and save it
#  You will see some warnings about the "metadata", don't worry about it
#  In case there are columns with the same name from both catalogs, their column name
#  will have suffix "_1" "_2" now
match_merged = hstack([match_hsc, match_decals])
match_merged.write('hsc_decals_matched_1.0arcsec.fits', format='fits',
                    overwrite=True)
```

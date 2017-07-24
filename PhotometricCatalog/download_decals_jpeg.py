#!/usr/bin/env python
# encoding: utf-8

"""Get DECALS JPEG Cutout Images."""

import requests
import argparse
import matplotlib.pyplot as plt

from PIL import Image
from StringIO import StringIO
from astropy.table import Table
from matplotlib.ticker import NullFormatter

DECALS_API = "http://legacysurvey.org/viewer/jpeg-cutout/?"


def getDecalsCutout(ra, dec, name=None, zoom=13):
    """
    Get DECaLS cutout JPEG images.
    """

    if name is None:
        name = "decals_ra-%s_dec-%sf" % (('%8.4f' % ra).strip(),
                                         ('%8.4f' % dec).strip())

    # Organize the URL of the JPEG file
    raStr = ("%10.5f" % ra).strip()
    decStr = ("%10.5f" % dec).strip()
    zoomStr = ("%2d" % zoom).strip()

    decalsStr = "ra=%s&dec=%s&zoom=%s&layer=decals-dr3" % (raStr,
                                                           decStr,
                                                           zoomStr)

    try:
        # URL of the JPG file
        jpgUrl = DECALS_API + decalsStr
        # Get the JPG image
        jpgImg = Image.open(StringIO(requests.request('GET',
                                                      jpgUrl).content))

        # Show the figure and save the file
        fig = plt.figure(figsize=(6, 6))
        ax1 = fig.add_axes([0.0, 0.0, 1.0, 1.0])
        ax1.imshow(jpgImg, aspect='auto', interpolation=None,
                   origin='lower', alpha=1.0)
        ax1.xaxis.set_major_formatter(NullFormatter())
        ax1.yaxis.set_major_formatter(NullFormatter())

        fig.savefig('%s.png' % name, format='png')

        plt.close(fig)

    except KeyError:
        pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=str, help="Name of the FITS table")
    parser.add_argument("--ra_col", type=str, help="Column name for RA",
                        default='ra', dest='ra_col')
    parser.add_argument("--dec_col", type=str, help="Column name for Dec",
                        default='dec', dest='dec_col')
    parser.add_argument("--name_col", type=str,
                        help="Column Name for ID",
                        default='object_id', dest='name_col')
    parser.add_argument('--zoom', type=int, help="Zoom in level",
                        default=13, dest='zoom')

    args = parser.parse_args()

    data = Table.read(args.table, format='fits')

    for obj in data:
        if args.name_col in data.colnames:
            getDecalsCutout(obj[args.ra_col],
                            obj[args.dec_col],
                            name=obj[args.name_col],
                            zoom=args.zoom)
        else:
            getDecalsCutout(obj[args.ra_col],
                            obj[args.dec_col],
                            name=None,
                            zoom=args.zoom)


#!/usr/bin/env python
# encoding: utf-8

"""Get DECALS JPEG Cutout Images."""

import os
import argparse

from astropy.table import Table

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

        # Name of the JPG file
        jpgName = '%s.jpg' % name

        # Download the JPG file using wget
        jpgCommand = 'wget "' + jpgUrl + '" -O ' + jpgName
        os.system(jpgCommand)

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

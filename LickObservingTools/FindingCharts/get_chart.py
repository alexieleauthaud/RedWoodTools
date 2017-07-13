from astroquery.sdss import SDSS
import os
import PIL
import requests
from PIL import Image
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy import units as u
from cStringIO import StringIO
from matplotlib import pyplot as plt
import numpy as np
import calc_offset
import sqlcl

try:
	from xastropy.xutils import xdebug as xdb
except:
	print "xastropy is not installed!!"

# Generate the SDSS URL (default is 202" on a side)
def sdsshttp(ra, dec, imsize, scale=0.39612, grid=None, label=None, invert=True):#, xs, ys):

    # Pixels
    npix = round(imsize*60./scale)
    xs = npix
    ys = npix
    #from StringIO import StringIO

    # Generate the http call
    name1='http://skyservice.pha.jhu.edu/DR12/ImgCutout/'
    name='getjpeg.aspx?ra='
    
    name+=str(ra)     #setting the ra
    name+='&dec='
    name+=str(dec)    #setting the declination
    name+='&scale='
    name+=str(scale) #setting the scale
    name+='&width='
    name+=str(int(xs))    #setting the width
    name+='&height='
    name+=str(int(ys))     #setting the height
    
    #------ Options
    options = ''
    if grid != None:
        options+='G'
    if label != None: 
        options+='L'
    if invert != None: 
        options+='I'
    if len(options) > 0: 
        name+='&opt='+options
        
    name+='&query='

    url = name1+name
    return url

# Generate the SDSS URL (default is 202" on a side)
def dsshttp(ra, dec, imsize):

    #https://archive.stsci.edu/cgi-bin/dss_search?v=poss2ukstu_red&r=00:42:44.35&d=+41:16:08.6&e=J2000&h=15.0&w=15.0&f=gif&c=none&fov=NONE&v3=

    Equinox = 'J2000'
    dss = 'poss2ukstu_red'
    url = "http://archive.stsci.edu/cgi-bin/dss_search?"
    url += "v="+dss+'&r='+str(ra)+'&d='+str(dec)
    url += "&e="+Equinox
    url += '&h='+str(imsize)+"&w="+str(imsize)
    url += "&f=gif"
    url += "&c=none"
    url += "&fov=NONE"
    url += "&v3="

    return url

# Calculate offset between Offset and Target
def offset(tra, tdec, ora, odec):
    if tra >= ora:
        ewtxt = "E"
    else:
        ewtxt = "W"
    if tdec >= odec:
        nstxt = "N"
    else:
        nstxt = "S"
    del_ra = abs(3600.0*(ora-tra)*np.cos(tdec*np.pi/180.0))
    del_dec = abs(3600.0*(odec-tdec))
    return del_ra, ewtxt, del_dec, nstxt

# ##########################################
def getimg(ira, idec, imsize, BW=False, DSS=None, fullname=False, slitangle="Parallactic"):
    ''' Grab an SDSS image from the given URL, if possible

    Parameters:
    ----------
    ira: (float or Quantity) RA in decimal degrees
    idec: (float or Quantity) DEC in decimal degrees
    '''

    # Strip units as need be
    try:
        ra = ira.value
    except KeyError:
        ra = ira
        dec = idec
    except AttributeError:
        ra = ira
        dec = idec
    else:
        dec = idec.value
    
    # Get URL
    if DSS == None:  # Default
        url = sdsshttp(ra,dec,imsize)
    else:
        url = dsshttp(ra,dec,imsize) # DSS

    # Request
    rtv = requests.get(url) 

# Commenting out the next section for now because it crashes in SDSS.query_region and this does not affect finder chart generation
    # Query for photometry
#    coord = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
#    phot = SDSS.query_region(coord, radius=0.02*u.deg)
    #print phot

 #   if phot is None:
 #       print('getimg: Pulling from DSS instead of SDSS')
 #       BW = 1
 #       url = dsshttp(ra,dec,imsize) # DSS
 #       rtv = requests.get(url) 

    img = Image.open(StringIO(rtv.content))

    # B&W ?
    if BW:
        import PIL.ImageOps
        img2 = img.convert("L")
        img2 = PIL.ImageOps.invert(img2)
        img = img2

    # Find offset by submitting a query through sqlcl.py, saving it as all_offsets.da t, and searching through it
    with open('all_offsets.dat', 'w') as query:
        conditions="SELECT r, ra, dec FROM Star WHERE ra BETWEEN " + str(ira-imsize/120.0) + " AND " + str(ira+imsize/120.0) + " AND dec BETWEEN " + str(idec-imsize/120.0) + " AND " + str(idec+imsize/120.0) + " and (r < 19) and (r > 7)"
        query_results=sqlcl.query(conditions).read()
        query.write(query_results)
    query.close()

    offsets = Table.read('all_offsets.dat', format='ascii', names=('r_mag','RA','DEC'))
#    xdb.set_trace()
#    min_distance = 0.4
#       if abs(ra-off_ra) <= 0.035 and abs(dec-off_dec) <= 0.035:
#           distance=(((ra-off_ra)**2)+((dec-off_dec)**2))**(1./2.)
#           if distance < min_distance:
#               min_distance = distance
#               min_r_mag = off_r_mag
#               min_off_ra = off_ra
#               min_off_dec = off_dec

    min_r_mag = 19

    if len(offsets) == 0:
        print "No offsets found within +/-0.03 in RA and DEC with r_mag <", min_r_mag

    if len(offsets) >= 1:
        for j in range(0, len(offsets)):
            off_r_mag = offsets['r_mag'][j]
            off_ra = offsets['RA'][j]
            off_dec = offsets['DEC'][j]

            if off_r_mag <= min_r_mag:
                min_r_mag = off_r_mag
                min_off_ra = off_ra
                min_off_dec = off_dec
            
        # Change object coordinates from decimal degrees to HMS/DMS
        string_ra = str(ira)
        string_dec = str(idec)
        hms_ra, dms_dec, other = calc_offset.decdeg_to_radec(string_ra, string_dec)

        # Change target coordinates from decimal degrees to HMS/DMS
        string_off_ra = str(min_off_ra)
        string_off_dec = str(min_off_dec)
        hms_off_ra, dms_off_dec, off_other = calc_offset.decdeg_to_radec(string_off_ra, string_off_dec)

        # Calculate offset move
        del_ra, e_or_w, del_dec, n_or_s = offset(ra, dec, min_off_ra, min_off_dec)

        # Obtain a name for the file
        if fullname:
        	outfil = "../finding_charts/"
        	outfil += "J" + hms_ra[0] + hms_ra[1] + hms_ra[2].split(".")[0]
        	outfil += "_"
        	outfil += dms_dec[0].replace("-","m").replace("+","p") + dms_dec[1] + dms_dec[2].split(".")[0]
        	outfil += ".pdf"
        else:
        	outfil = "J" + hms_ra[0] + hms_ra[1] + dms_dec[0] + dms_dec[1] + ".pdf"
        # Check if the file already exists
        if os.path.exists(outfil):
        	ans=""
        	while (ans!="n") and (ans!="y"):
        		ans = raw_input("\nFile already exists:\n"+outfil+"\nOverwrite (y/n): ")
        	if ans == "n":
        		print "Finder not written!"
        		return
        # Plot the figure
        fig = plt.figure(dpi=1200)
        fig.set_size_inches(8.0,10.5)

        # Font
        plt.rcParams['font.family']= 'times new roman'
        ax = plt.gca()

        # Image
        if BW == 1:  cmm = cm.Greys_r
        else: cmm = None 
        cradius = imsize / 30. 
        plt.imshow(img, cmap=cmm, aspect='equal', extent=(-imsize/2., imsize/2, -imsize/2.,imsize/2))

        # Axes
        plt.xlim(-imsize/2., imsize/2.)
        plt.ylim(-imsize/2., imsize/2.)

        # Label
        plt.xlabel('Relative ArcMin', fontsize=20)
        xpos = 0.12*imsize
        ypos = 0.02*imsize
        plt.text(-imsize/2.-xpos, 0., 'EAST', rotation=90., fontsize=20)
        plt.text(0., imsize/2.+ypos, 'NORTH', fontsize=20, horizontalalignment='center')
        plt.text(0., -imsize/2.-8*ypos, 'Slit Angle = '+slitangle, fontsize=20, horizontalalignment='center')

        # Title
        plt.text(0.25, 1.28, 'Object Coordinates:', fontsize=18,
        horizontalalignment='center', transform=ax.transAxes)
        plt.text(0.25, 1.23, 'RA = ' + str(hms_ra[0]) + ":" + str(hms_ra[1]) + ":" + str(hms_ra[2]), fontsize=20, 
        horizontalalignment='center', transform=ax.transAxes)
        plt.text(0.25, 1.18, 'DEC = '+ str(dms_dec[0]) + ":" + str(dms_dec[1]) + ":" + str(dms_dec[2]), fontsize=20, 
        horizontalalignment='center', transform=ax.transAxes)
        plt.text(0.75, 1.28, 'Offset Coordinates (r=' + str(format(min_r_mag,'.2f')) + '):', fontsize=18,
        horizontalalignment='center', transform=ax.transAxes)
        plt.text(0.75, 1.23, 'RA = ' + str(hms_off_ra[0]) + ":" + str(hms_off_ra[1]) + ":" + str(hms_off_ra[2]), fontsize=20, 
        horizontalalignment='center', transform=ax.transAxes)
        plt.text(0.75, 1.18, 'DEC = '+ str(dms_off_dec[0]) + ":" + str(dms_off_dec[1]) + ":" + str(dms_off_dec[2]), fontsize=20, 
        horizontalalignment='center', transform=ax.transAxes)
        plt.text(0.5, 1.13, 'From Offset, move to get to Object:', fontsize=18,
        horizontalalignment='center', transform=ax.transAxes)
        plt.text(0.5, 1.08, str(format(del_ra, '.2f')) + "'' " + e_or_w + " and " +  str(format(del_dec, '.2f')) + "'' " + n_or_s, fontsize=20,
        horizontalalignment='center', transform=ax.transAxes)

        # Circle for target, then offset
        circle=plt.Circle((0,0), cradius, color='y', fill=False)
        plt.gca().add_artist(circle)

        if e_or_w == 'W' and n_or_s == 'S':
            circle_offset=plt.Circle((-del_ra/60, del_dec/60), cradius, color='g', fill=False)
            plt.gca().add_artist(circle_offset)
        elif e_or_w == 'W' and n_or_s == 'N':
            circle_offset=plt.Circle((-del_ra/60, -del_dec/60), cradius, color='g', fill=False)
            plt.gca().add_artist(circle_offset)
        elif e_or_w == 'E' and n_or_s == 'S':
            circle_offset=plt.Circle((del_ra/60, del_dec/60), cradius, color='g', fill=False)
            plt.gca().add_artist(circle_offset)
        elif e_or_w == 'E' and n_or_s == 'N':
            circle_offset=plt.Circle((del_ra/60, -del_dec/60), cradius, color='g', fill=False)
            plt.gca().add_artist(circle_offset)

        # Spectrum??
        show_spec=False
        if show_spec:
            spec_img = xgs.get_spec_img(ra_tab['RA'][qq], ra_tab['DEC'][qq]) 
            plt.imshow(spec_img,extent=(-imsize/2.1, imsize*(-0.1), -imsize/2.1, imsize*(-0.2)))

        # Write
        if show_spec:
            plt.savefig(outfil, dpi=300)
        else:
            plt.savefig(outfil)
        print 'finder: Wrote '+outfil

###################################

#ira = 193.111
#idec = 0.695
#imsize=3.5

#getimg(ira, idec, imsize)

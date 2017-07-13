import numpy as np

target_ra  = "13:07:29.94"
target_dec = "+03:49:21.01"

offsetstar_ra  = "13:07:34.96"
offsetstar_dec = "+03:49:03.73"

"""
EXAMPLES
--------------------------------
target_ra  = "11 36 19.58"
target_dec = "-10 52:37.4"
offsetstar_ra  = "11:36:13.33"
offsetstar_dec = "-10:53:28.0"

target_ra  = "174.06904167"
target_dec = "-10.87963889"
offsetstar_ra  = "174.05554167"
offsetstar_dec = "-10.89111111"
"""

def radec_to_decdeg(ra, dec):
	raspl = ra.split()
	raout = 15.0*(float(raspl[0]) + float(raspl[1])/60.0 + float(raspl[2])/3600.0)
	dcspl = dec.split()
	if "-" in dcspl[0]:
		dcout = float(dcspl[0]) - float(dcspl[1])/60.0 - float(dcspl[2])/3600.0
	else:
		dcout = float(dcspl[0]) + float(dcspl[1])/60.0 + float(dcspl[2])/3600.0
	return raout,dcout,"{0:s}  {1:s} ---> {2:13.8f}, {3:+13.8f}".format(ra,dec,raout,dcout)

def decdeg_to_radec(ra, dec):
	raf = float(ra)/15.0
	raA = int(raf)
	raB = int((raf - float(raA))*60.0)
	raC = float(raf - float(raA) - float(raB)/60.0)*3600.0
	dcf = float(dec)
	dcA = int(dcf)
	dcB = int((dcf - float(dcA))*60.0)
	dcC = (dcf - float(dcA) - float(dcB)/60.0)*3600.0
	# print RA values to a string
	raal = "{0:02d}".format(raA)
	rabl = "{0:02d}".format(raB)
	if raC < 10.0: racl = "0"
	else: racl = ""
	racl += "{0:5.3f}".format(raC)
	# print DEC values to a string
	if dcf < 0.0:
		dcA *= -1
		dcB *= -1
		dcC *= -1.0
		if dcf > -1.0:
			dcal = "-"
		else:
			dcal = "-"
	else: dcal = "+"
	dcal += "{0:02d}".format(dcA)
	dcbl = "{0:02d}".format(dcB)
	if dcC < 10.0: dccl = "0"
	else: dccl = ""
	dccl += "{0:5.3f}".format(dcC)
	ralist = [raal,rabl,racl]
	dclist = [dcal,dcbl,dccl]
	return ralist,dclist, "{0:s}, {1:s}  ---> {2:s} {3:s} {4:s}  {5:s} {6:s} {7:s}".format(ra,dec,raal,rabl,racl,dcal,dcbl,dccl)

# Run the code directly if called by executing this file
if __name__ == '__main__':

	target_ra  = target_ra.replace(":"," ")
	target_dec = target_dec.replace(":"," ")
	offsetstar_ra  = offsetstar_ra.replace(":"," ")
	offsetstar_dec = offsetstar_dec.replace(":"," ")

	# Set the default parameters
    # Change Target HMS/DMS to DecDeg if needed
	if " " in target_ra and " " in target_dec:
		trao, tdeco, null = radec_to_decdeg(target_ra, target_dec)

	else:
		trao = float(target_ra)
		tdeco = float(target_dec)
    # Change Offset HMS/DMS to DecDeg if needed
	if " " in offsetstar_ra and " " in offsetstar_dec:
		orao, odeco, null = radec_to_decdeg(offsetstar_ra, offsetstar_dec)
		if trao >= orao:
			ewtxt = "E"
		else:
			ewtxt = "W"
		if tdeco >= odeco:
			nstxt = "N"
		else:
			nstxt = "S"
		print "From Offset star ({0:s}, {1:s}), move:".format(offsetstar_ra,offsetstar_dec)
		print "{0:4.2f}'' {1:s}".format(abs(3600.0*(odeco-tdeco)),nstxt)
		print "{0:4.2f}'' {1:s}".format(abs(3600.0*(orao-trao)*np.cos(tdeco*np.pi/180.0)),ewtxt)
	else:
		orao = float(offsetstar_ra)
		odeco = float(offsetstar_dec)
		rao, deco, strv = decdeg_to_radec(offsetstar_ra, offsetstar_dec)
		if trao >= orao:
			ewtxt = "E"
		else:
			ewtxt = "W"
		if tdeco >= odeco:
			nstxt = "N"
		else:
			nstxt = "S"
		print "From Offset star ({0:s}:{1:s}:{2:s}, {3:s}:{4:s}:{5:s}), move:".format(rao[0],rao[1],rao[2],deco[0],deco[1],deco[2])
		print "{0:4.2f}'' {1:s}".format(abs(3600.0*(odeco-tdeco)),nstxt)
		print "{0:4.2f}'' {1:s}".format(abs(3600.0*(orao-trao)*np.cos(tdeco*np.pi/180.0)),ewtxt)


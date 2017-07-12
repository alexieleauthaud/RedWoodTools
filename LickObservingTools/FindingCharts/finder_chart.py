from astropy.table import Table
import numpy as np
import calc_offset
import get_chart

try:
	from xastropy.xutils import xdebug as xdb
except:
	print "xastropy is not installed!!"

target_list = Table.read('target_list.dat', format = 'ascii.no_header', delimiter = ',', names = ('RA','DEC'))

for i in range(0, len(target_list)):
	imsize = 4.0

#	xdb.set_trace()
	if ":" in str(target_list['RA'][i]) and ":" in str(target_list['DEC'][i]):
		target_RA = target_list['RA'][i].replace(":", " ")
		target_DEC = target_list['DEC'][i].replace(":", " ")
		t_RA, t_DEC, other = calc_offset.radec_to_decdeg(target_RA, target_DEC)
		print "in decimal degrees:", t_RA, t_DEC
		get_chart.getimg(t_RA, t_DEC, imsize, fullname=True, slitangle="0 degrees (i.e. oriented North-South)")
		#get_chart.getimg(t_RA, t_DEC, imsize)
	else:
		get_chart.getimg(target_list['RA'][i], target_list['DEC'][i], imsize)
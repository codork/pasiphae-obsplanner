#Code to calculate dome merit;
#simulated on a set of random coordinates

from astropy.coordinates import SkyCoord, ICRS
from astropy import units as u
from astropy.table import Table
import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz

#convert RA from hms to deg
def hms2dec(h,m,s):
  deg = 15*(h+(m/60)+(s/(60*60)))
  return deg

#convert DEC from dms to degrees
def dms2dec(d,arcm,arcs):
  if(d>=0):
    deg = d+(arcm/60) + (arcs/(60*60))
  else:
    deg = -(-d+(arcm/60) + (arcs/(60*60)))
  return deg

#returns list of field coordinates read from table2.dat
def import_coords():
  cat = np.loadtxt('table2.dat', usecols=range(1,7)) #random list of coordinates for the purpose of simulation
  coordlist = []
  for i in range(cat.shape[0]):
      #convert ra and dec to degrees
    ra = hms2dec(cat[i][0],cat[i][1],cat[i][2])
    dec = dms2dec(cat[i][3],cat[i][4],cat[i][5])
    mytuple = (i+1, ra, dec)
    coordlist.append(mytuple)
  t = Table(rows=coordlist, names=('#','RA','DEC'), meta={'name': 'Coords'}, dtype=('i4','f8','f8'))
  return t

#calculate slew time and dome rotation time
def get_slewtime(ctable):
    dome_rate = 3 #in degrees/second
    slew_time = 15 #telescope takes 15 seconds to slew between two farthest points
    readout = 30 #instrument readout time = 30 seconds
    slewlist = []
    i = 1
    time = Time('2019-10-01 00:00:00')
    mysite = EarthLocation.from_geodetic(lon=24.899166666666666, lat=35.21194444444445, height=1750)    #Skinakas Observatory

    for j in range(0,50):    #for initial 2500 possible coordinate combinations
        for k in range(0,50):
            if j!=k:
                #create SKyCoord objects for the two coords and convert to alt-az
                f1 = SkyCoord(ra=ctable['RA'][j], dec=ctable['DEC'][j], frame='icrs', unit='deg')
                f1_altaz = f1.transform_to(AltAz(obstime=time, location=mysite))
                f2 = SkyCoord(ra=ctable['RA'][k], dec=ctable['DEC'][k], frame='icrs', unit='deg')
                f2_altaz = f2.transform_to(AltAz(obstime=time, location=mysite))

                #get angular separation between current and candidate field center coords
                sep = np.absolute(f2_altaz.az.deg - f1_altaz.az.deg) #-wrong - get ANGULAR sep
                #get time needed to rotate through the sep
                dome_time = dome_rate * sep
                #check is dome rotation time is greater than telescope slew time
                if dome_time > slew_time:
                    higher_than_slew = True
                else:
                    higher_than_slew = False

                #if maximum of the dome and telescope slew is lesser than readout, merit value is 0
                if(max(dome_time, slew_time)  <= readout):
                    merit_val = 0
                else:
                    delay = readout - max(dome_time, slew_time)
                    merit_val = 1/delay #merit value is the inverse of the delay

                slew = (i, "%.2f" %ctable['RA'][j], "%.2f" %ctable['DEC'][j], "%.2f" %ctable['RA'][k], "%.2f" %ctable['DEC'][k], "%.2f" %sep, "%.2f" %dome_time, higher_than_slew, "%.2f" %merit_val)
                slewlist.append(slew)
                i += 1

    slewtime = Table(rows=slewlist, names=('#','From RA','From DEC','To RA','To DEC','Separation', 'Dome Rotation Time', 'Higher than slew', 'Merit Value'))
    return slewtime

if __name__ == '__main__':
    t = import_coords()
    slew_table = get_slewtime(t)
    display(slew_table)

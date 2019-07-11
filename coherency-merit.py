import numpy as np
import mysql

#separate function because moment need not be newly calculated every time a field merit is calculated;
#moment can be calculated once in the beginning of the night and have global access 
def get_coherency_moment(field_db):
    
    #from mysql database of fields, get fields that have OBS STATUS > 0
    
    #calculate weighted moment of fields already observed as weight*field_coords, where
    #weight = obs_status (in percentage) 
    for field in fields:
        weighted_moment_ra += field.OBS_STATUS * field.RA
        weighted_moment_dec += field.OBS_STATUS * field.DEC
    
    moment = (weighted_moment_ra/len(fields), weighted_moment_dec/len(fields))
    
    return moment #return a tuple of (ra, dec)

def angular_dist(ra1,dec1,ra2,dec2):
      r1=np.radians(ra1)
      r2=np.radians(ra2)
      d1=np.radians(dec1)
      d2=np.radians(dec2)
      a = np.sin(np.abs(d1-d2)/2)**2
      b = np.cos(d1)*np.cos(d2)*(np.sin(np.abs(r1-r2)/2)**2)
      d = 2*np.arcsin(np.sqrt(a+b))
      d = np.degrees(d)
      return d

def get_coherency_merit(self):
    d = angular_dist(self.ra, self.dec, moment[0], moment[1])
    return 1/d
    

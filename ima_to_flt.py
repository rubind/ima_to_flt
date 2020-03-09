from astropy.io import fits
from numpy import *
import glob

minimum_time = 20 # In seconds

for fltname in glob.glob("*_flt.fits"):
    fflt = fits.open(fltname)
    print(fflt[0].header["EXPTIME"])
    print(fflt.info())
    
    
    fima = fits.open(fltname.replace("_flt.", "_ima."))
    print(fima.info())
    
    last_frame = 0.
    
    for i in range(len(fima) - 10, 0, -5):
        sampnum = fima[i].header["SAMPNUM"]
        samptime = fima[i].header["SAMPTIME"]
        deltatime = fima[i].header["DELTATIM"]
        
        print(i, sampnum, deltatime, samptime)
        
        fflt["SCI"].data = (fima[i].data[5:-5,5:-5]*samptime - last_frame)/deltatime
        fflt["DQ"].data = fima[i+2].data[5:-5,5:-5]
        
        newname = fltname.replace("_flt", "_%02i_flt" % sampnum)
        assert newname != fltname, "Couldn't come up with a name!"
        
        for j in range(len(fflt)):
            try:
                fflt[j].header["EXPTIME"] = deltatime
            except:
                pass

        if deltatime >= minimum_time:
            fflt.writeto(newname, clobber = True)
        last_frame = fima[i].data[5:-5,5:-5]*samptime
    

    fima.close()
    fflt.close()

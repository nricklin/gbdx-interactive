# gbdx-interactive
Like gbdxtools, but interactive and "real-time"

```python
from gbdx_interactive import gbdx_interactive
gbdx = gbdx_interactive.lets_go_insane()

# let's acomp some landsat data and then play with it
data = 's3://landsat-pds/L8/141/042/LC81410422015104LGN00/'
acomp = gbdx.Task('AComp', params={'data': data})
results = acomp.execute()   # happens synchronously

# list the objects created during the acomp run
for file in results['data'].list():
    print file
    # lists objects that look like: gbdx://workflow_output/4515188909926013460/AComp_b4f67d2c/data/LC81410422015104LGN00_B1_ACOMP.TIF

# pull an acomped landsat file locally to take a look at
f = gbdx.remote_file('gbdx://workflow_output/4515188909926013460/AComp_b4f67d2c/data/LC81410422015104LGN00_B1_ACOMP.TIF')
f.getFile('file.TIF')

# crop and manipulate locally
b7local = gdal.Open('file.TIF')
img = b7local.ReadAsArray()
img2 = img[3000:4000,1000:4000]

# save as a file and push the file remotely to be operated on once again by gbdx
import scipy.misc
scipy.misc.imsave('cropped.tif', img2)
new_image = gbdx.remote_file('gbdx://cropped.tif')
new_image.putFile('cropped.tif')

# run another gbdx task on the data I just pushed up
colorslice = gbdx.Task('ENVI_ColorSliceClassification', params={'input_raster': new_image})
results2 = colorslice.execute()

# see what happened after colorslice classification:
print results2['output_raster_uri'].list() # I get stuff like this: gbdx://workflow_output/4515118701306662276/ENVI_ColorSliceClassification_ffed94ba/output_raster_uri/data.tif

# move those results local so I can take a look at them:
output_tif = gbdx.remote_file(results2['output_raster_uri'].list()[1])
output_tif.getFile('output.tif')
output_img = gdal.Open('output.tif').ReadAsArray()
```

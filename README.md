# gbdx-interactive
Like gbdxtools, but interactive and "real-time"

```python
from gbdx_interactive import gbdx_interactive
gbdx = gbdx_interactive.lets_go_insane()

data = 's3://landsat-pds/L8/141/042/LC81410422015104LGN00/'
acomp = gbdx.Task('AComp', params={'data': data})
results = acomp.execute()   # happens synchronously

# list the objects created during the acomp run
for file in results['data'].list():
    print file
    # lists objects that look like: gbdx://workflow_output/4515188909926013460/AComp_b4f67d2c/data/LC81410422015104LGN00_B1_ACOMP.TIF

# pull a file locally to take a look at
f = gbdx.remote_file('gbdx://workflow_output/4515188909926013460/AComp_b4f67d2c/data/LC81410422015104LGN00_B1_ACOMP.TIF')
f.getFile('file.TIF')

# crop and manipulate 
b7local = gdal.Open('file.TIF')
img = b7local.ReadAsArray()
img2 = img[3000:4000,1000:4000]

```

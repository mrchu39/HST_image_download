from astroquery.mast import Observations
import numpy as np
from astropy.time import Time
import datetime
import os
from astropy.time import Time
from shutil import rmtree

def get_files(date_since, dir=None):
    if dir == None:
        file_dump = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")
    else:
        file_dump = dir

    os.mkdir('downloads/'+file_dump)
    os.chdir('downloads/'+file_dump)

    date = Time(date_since, format='isot', scale='utc').mjd

    obs_table = Observations.query_criteria(dataproduct_type=["image"], proposal_pi="Fremling*")

    parents = [True if i[:3] == 'iep' else False for i in np.array(obs_table['obs_id'])]

    obs_table = obs_table[parents]
    obs_table = obs_table[np.array(obs_table['t_obs_release']) > date]

    for i in range(len(obs_table)):
        obsids = obs_table['obsid'][i]
        name = obs_table['target_name'][i]

        data_products_by_id = Observations.get_product_list(obsids)

        files = Observations.download_products(data_products_by_id,productType="SCIENCE",productSubGroupDescription=["DRC"],extension="fits",curl_flag=True)

        stream = os.popen(files['Local Path'][0])
        output = stream.read()

        temps = os.listdir()

        for t in temps:
            if '.sh' in t:
                shell = t
            if 'MAST_' in t:
                mast_down = t

        os.remove(shell)

        os.mkdir(name)

        all_files = os.listdir(mast_down+'/HST')

        for f in all_files:
            os.rename(mast_down+"/HST/"+f+'/'+f+'_drc.fits', name+'/'+f+'.fits')

        rmtree(mast_down)

import pandas as pd
import numpy as np
import os
pathfiledir='.\\traj'
stayfdir='.\\stayPointlast'
storedir='.\\tag'
for root, dirks, files in os.walk(pathfiledir):
    for filename in files:
        if os.path.exists(os.path.join(stayfdir,filename)):
            traj=pd.read_csv(os.path.join(pathfiledir,filename))
            period=pd.read_csv(os.path.join(stayfdir,filename),usecols=["arriving time","leaving time"])
            # tag=[period[["arriving time","leaving time"]][(date >= period["arriving time"]) & (date <= period["leaving time"])] for date in traj['timestamp']]
            tag=[period[["arriving time","leaving time"]][(traj.loc[each-1,'timestamp'] <= period["arriving time"]) & (traj.loc[each,'timestamp'] >= period["arriving time"])] for each in range(1,len(traj))]
            # blank=pd.DataFrame()
            # tag.append(blank)
            tag1=[0 if each.empty else 1 for each in tag]
            tag1.insert(0,0)
            traj['status']=tag1
            traj.to_csv(os.path.join(storedir,filename),index=0)
#normalized cooccurence mean
import numpy as np
import json
import pandas as pd
import time
from scipy import sparse
time_start=time.time()

#read file
durations=pd.read_csv('durations.csv')
#test_set=pd.read_csv('test_durations.csv')


#build rating matrix
playlist_num=1000

#calculate from data.py
track_num=34443
#track_num=2262292


##method 1: fill in the matrix, taking too long time

cooccur_mat=np.zeros([track_num,playlist_num])
for _, row in durations.iterrows():
	# since the value of co-occurence mean is between 0-1, using a number <0
    cooccur_mat[row.track_index,row.playlist] = -1


def fill_mat():
	for pid in range(playlist_num):
		for track in range(track_num):
			if cooccur_mat[track][pid] != -1:
				cooccur_mean=0
				n_track=np.nonzero(cooccur_mat[track])[0]
				
				for rated in np.nonzero(cooccur_mat[:,pid])[0]:
					n_rated=np.nonzero(cooccur_mat[rated])[0]
					n_randt = set(n_rated) & set(n_track)
					if len(n_randt)==0:
						cooccur_mean=0
					else:
						cooccur_mean += len(n_randt)/len(n_rated)

				cooccur_mean = cooccur_mean/len(np.nonzero(cooccur_mat[:,pid])[0])
				cooccur_mat[track][pid]=cooccur_mean
				print(cooccur_mean)


fill_mat()
print(cooccur_mat)
time_end=time.time()
print('total:',time_end-time_start)


##method 2: add a new column called co_occur_norm_mean


















import numpy as np
import json
import pandas as pd
import time
from scipy import sparse
time_start=time.time()

#read file
slice1=pd.read_csv('durations.csv')
test_set=pd.read_csv('test_durations.csv')



#build rating matrix
#playlist_num=1000000
playlist_num=1000

#calculate from data.py
track_num=34443
#track_num=2262292


ratings_mat = sparse.lil_matrix((playlist_num, track_num))
for _, row in slice1.iterrows():
    ratings_mat[row.playlist,row.track_index] = row.duration



test_playlist_num=200
test_ratings_mat=sparse.lil_matrix((playlist_num, track_num))
for _, row in test_set.iterrows():
    test_ratings_mat[row.playlist,row.track_index] = row.duration


time_end=time.time()
print('total:',time_end-time_start)



time_start=time.time()

def train(factors,epochs=50,theta=1e-4,lr=0.01,beta=0.02):
	print('start')
	old_rmse=0
	p=np.ones([playlist_num,factors])/10	
	q=np.ones([track_num,factors])/10
	#train factor by factor
	for f in range(factors):
		#print("factors",f)
		for epoch in range(epochs):
			#print('epoch',epoch)
			current_rmse=0	
			
			total_nonzero=0
			for i in range(playlist_num):
				total_nonzero+=len(ratings_mat.rows[i])
				for j in ratings_mat.rows[i]:

					true_r=ratings_mat[i,j]
					pred_r=np.dot(p[i],q[j])
					
					err=true_r-pred_r

					p[i][f]+=lr*(err*q[j][f]-beta*p[i][f])
					q[j][f]+=lr*(err*p[i][f]-beta*q[j][f])
				
					current_rmse+=pow(err,2)

			current_rmse=pow(current_rmse/total_nonzero,0.5)
			
			# print('factor',f)
			# print('epoch',epoch)
			# print('cost is {}'.format(current_mse))

			if abs(current_rmse-old_rmse)<theta:	
				break
			old_rmse=current_rmse

	print('train:',current_rmse)
	return p,q



def test(f):
	p,q=train(f)
	q_t=np.transpose(q)
	pred_rating_mat=np.dot(p,q_t)

	current_rmse=0		
	total_nonzero=0
	for i in range(test_playlist_num):
		total_nonzero+=len(test_ratings_mat.rows[i])
		for j in test_ratings_mat.rows[i]:

			true_r=test_ratings_mat[i,j]
			pred_r=pred_rating_mat[i][j]
			
			err=true_r-pred_r
		
			current_rmse+=pow(err,2)

	current_rmse=pow(current_rmse/total_nonzero,0.5)
	print('test_set',current_rmse)




def change_factor_num(factors):
	for f in factors:
		print('change_factor_num',f)
		test(f)
			

change_factor_num([10,150,160,170,180])









#get ranking matrix

# p,q=train(50)
# q_t=np.transpose(q)

# pred_rating_mat=np.dot(p,q_t)
# print(pred_rating_mat)


# pred_index_mat=np.argsort(pred_rating_mat[0])[track_num-500:]
# for i in range(1,playlist_num):
# 	index_rank=np.argsort(pred_rating_mat[i])[track_num-500:]
	
# 	print(index_rank)
# 	pred_index_mat=np.vstack((pred_index_mat,index_rank))
# #m=np.array(m)
# print(pred_index_mat)
# print(type(pred_index_mat))






time_end=time.time()
print('total:',time_end-time_start)



















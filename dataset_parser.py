# File: dataset_parser.py
# Author: Kevin Khieu
# Assignment: CS224W Project Milestone

import sys
import os
from json import loads
from re import sub
import snap
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import pickle

# Deletes filename if exists then creates a text file to be read in as a UNDIRECTED Snap Graph
# Bipartite: User <---> Business based on reviews
# Files Created:
# filename.txt  -   snap node edge graph
# filename_elite.txt - list of elite node numbers
def UserBusinessReviewsTxt(filename, json_file):
	snap_file = filename + '.txt'
	elite_file = filename + '_elite.txt'
	try:
		os.remove(snap_file)
	except OSError:
		pass

	try:
		os.remove(elite_file)
	except OSError:
		pass

	users = None
	with open("pickled_users.txt", "rb") as fp1:   # Unpickling
		users = pickle.load(fp1)

	businesses = None
	with open("pickled_businesses.txt", "rb") as fp:   # Unpickling
		businesses = pickle.load(fp)

	print len(users)
	print len(businesses)
	snap_fp = open(snap_file, "w")
	snap_fp.write('# Aggregated Undirected Bipartite Graph: Users to Businesses (Reviews)\n')
	snap_fp.write('# Tab-separated list of edges. Refer to filename_elite.txt for elite mapping\n')
	snap_fp.write('# NodeId  NodeId\n')


	elite_fp = open(elite_file, "w")
	with open(json_file, 'r') as f:
		count = 1
		for line in f:
			review = loads(line.strip()) # creates a Python dictionary of Items for the supplied json file
			user_node = review['user_id'].encode('ascii', 'ignore')
			business_node = review['business_id'].encode('ascii', 'ignore')
			file_str = "%s\t%s\t%s\n" % (str(users[user_node]['nodeId']), str(businesses[business_node]['nodeId']), str(review['stars']))
			#print file_str
			print count
			count += 1
			snap_fp.write(file_str)

def ReadUsers():
	users = {}
	count = 0
	with open('dataset/user.json', 'r') as f:
		for line in f:
			user = loads(line.strip()) # creates a Python dictionary of Items for the supplied json file
			new_user = {}

			# ADDED NODEID FIELD
			new_user['nodeId'] = count
			if 'elite' in user:
				new_user['elite'] = user['elite']
			
			if 'user_id' in user:
				new_user['user_id'] = user['user_id']
			
			if 'review_count' in user:
				new_user['review_count'] = user['review_count']
			
			if 'fans' in user:
				new_user['fans'] = user['fans']
			
			if 'average_stars' in user:
				new_user['average_stars'] = user['average_stars']

			print new_user
			users[user['user_id']] = new_user
			count += 1

	with open("pickled_users.txt", "wb") as fp:
		pickle.dump(users, fp, protocol=pickle.HIGHEST_PROTOCOL)

def ReadBusinesses():
	businesses = {}
	count = 1183361 + 5 # UPDATE IF WE GET MORE USERS FOR SOME REASON. 5 is buffer
	with open('dataset/business.json', 'r') as f:
		for line in f:
			business = loads(line.strip()) # creates a Python dictionary of Items for the supplied json file
			new_business = {}

			# ADDED NODEID FIELD
			new_business['nodeId'] = count

			if 'review_count' in business:
				new_business['review_count'] = business['review_count']
			
			if 'business_id' in business:
				new_business['business_id'] = business['business_id']
			
			if 'name' in business:
				new_business['name'] = business['name']
			
			if 'stars' in business:
				new_business['stars'] = business['stars']

			print new_business
			businesses[business['business_id']] = new_business
			count += 1

	with open("pickled_businesses.txt", "wb") as fp:
		pickle.dump(businesses, fp, protocol=pickle.HIGHEST_PROTOCOL)

#ReadUsers()
#ReadBusinesses()
UserBusinessReviewsTxt('user_business', 'dataset/review.json')
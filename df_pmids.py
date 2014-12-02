'''

First pass at combining @almetric scores for an article and its referencese using pandas

Data collected from http://www.altmetric.com/ and https://pmc-ref.herokuapp.com

pmc-ref is a prototype with limited data available. Any performance issues with this script will probably be due to pmc-ref.

Suggestions for improvements welcome! 

Use ipython --pylab

'''
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time



pmc_ref_request = requests.get('https://pmc-ref.herokuapp.com/api/v1/articles/doi/10.1007%2Fs00439-013-1358-4') #10.1038/nature10158

article = pmc_ref_request.json()

article_pmid = str(article['article'][0]['pmid'])

article_references = article['article'][0]['references']# a list

pmids = []
pmids.append(article_pmid)

for reference in article_references:
	if reference['pmid'] != 0: #pmids might be 0 
		pmids.append(str(reference['pmid']))
		



#build a dict of Series

dict_of_series = {}

for pmid in pmids:

	altmetric_request = requests.get('http://api.altmetric.com/v1/pmid/'+pmid)
	#check response
	if altmetric_request.status_code == 200:
		altmetric_response_dict = altmetric_request.json()
		altmetric_data = pd.Series(altmetric_response_dict)
		dict_of_series[pmid] = altmetric_data
		print('collected data for '+pmid)
	else:
		print('no data for '+ pmid)

	time.sleep(2.0)# so api isn't hammered



frame = pd.DataFrame(dict_of_series)
altmetric_data_frame = frame.T

fig, ax = plt.subplots(1,1)
ax.set_xlabel('pmids')
ax.set_ylabel('altmetric score')

altmetric_data_frame.score.plot(kind="bar", ax=ax, title="Altmetric scores for pmid "+article_pmid+" and its references", rot=75)#score is a Series


#use altmetric_data_frame.ix[''] and a pmid to see more info on articles 






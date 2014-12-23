'''

A bit of fun combinging altmetric and text-processing APIs to get sentiment of tq (top quote) field 
from altmetric response.

APIs used and rate limits:
http://www.altmetric.com/ one per second
http://text-processing.com/api/sentiment/ 1000 calls per IP per day
https://pmc-ref.herokuapp.com/ none but pmc-ref is a prototype with limited data available and any performance issues with this script will probably be due to pmc-ref.


Results stored in pandas DataFrame called altmetric_data_frame.

text-processing sentiment analyser is trained on movie reviews. 

tq field can store more than one top quote. In these cases each elem of the list is joined 
together. The asuumption is the sentiment of tq is the same but that could be wrong.

Have found that sentiment doesn't necessarily concern the article but can in some cases be agreeing with the conclusion of the article.

For example, some extracts considered negative sentiment: 

"pesky little genome acquisitions which make our energy are showing signs of influencing 1:500 childhood disease", 
"27&percent; of mutations found to be common polymorphs or misannotated. Need better mutation dbs 4 carrier testing (Kingsmore)", 
"Not a 'knockout'? Guo et al. provide insight into the molecular mechanisms by which mutant alleles cause disease"

To read:

http://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-856.pdf by @awaisathar

Suggestions for improvements welcome! 




'''
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time



pmc_ref_request = requests.get('https://pmc-ref.herokuapp.com/api/v1/articles/doi/10.1007%2Fs00439-013-1358-4') #implement /citations/ endpoint rather than getting references

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

# get sentiment analysis results of top quotes, add as a column to altmetric_data_frame

top_quotes_values = altmetric_data_frame.tq.dropna()
text_processing_base_url = 'http://text-processing.com/api/sentiment/'

empty_str = ''
sentiment = {}

for key in top_quotes_values.keys():
	text_data = {'text': empty_str.join(str(elem) for elem in top_quotes_values[key])}
	text_processing_request = requests.post(text_processing_base_url, data=text_data)
	sentiment[key] = text_processing_request.json()
	

altmetric_data_frame['sentiment'] = ''

for pmid in altmetric_data_frame.pmid:
	if pmid in sentiment.keys():
		altmetric_data_frame.ix[pmid]['sentiment'] = sentiment[pmid]['label'] # discarding probablity values
	else:
		altmetric_data_frame.ix[pmid]['sentiment'] = None


positive_sentiment = altmetric_data_frame[altmetric_data_frame.sentiment == 'pos']
negative_sentiment = altmetric_data_frame[altmetric_data_frame.sentiment == 'neg']
neutral_sentiment = altmetric_data_frame[altmetric_data_frame.sentiment == 'neutral']






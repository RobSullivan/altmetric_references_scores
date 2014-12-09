#Plotting the Almetric scores for an article and its references

##What is it?

This script plots a histogram of the altmetric scores for an article and its references

##How does it work?
Using a doi (digital object identifier) this script requests the references of an article from the pmc-ref API (https://pmc-ref.herokuapp.com/). It then extracts the pmids of the article and references. 

Using the pmids it requests data from  requesting  and then goes to http://api.altmetric.com/v1/pmid/ for altmetric data.

Each response from almetric.com is stored as a pandas Series in a dict_of_series in order to initiate a pandas DataFrame. 

From the DataFrame a simple histogram can be generated.


###Dependencies
ipython==2.3.1
requests==2.4.3
pandas==0.15.1
numpy==1.9.1
matplotlib==1.4.2



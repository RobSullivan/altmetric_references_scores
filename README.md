altmetric_references_scores
===========================

#Plotting the Almetric scores for an article and its references

##What is it?

This script plots a histogram of the altmetric scores for an article and its references

##How does it work?
Using a doi (digital object identifier) this script requests the references of an article from the pmc-ref API (https://pmc-ref.herokuapp.com/). It then extracts the pmids of the article and references. 

Using the pmids it requests data from  requesting  and then goes to http://api.altmetric.com/v1/pmid/ for altmetric data.

Each response from almetric.com is stored as a series in a dict_of_series in order to initiate a DataFrame. 

From the DataFrame a simple histogram can be generated.




# nhscausalknolwedgegraph
NHS causal knolwedge graph with evaluation and clustering

1. DatagenerationAndEvaluation.ipynb is the main file you can see the process of generating NHS causality knoweldge graph and the data evaluation and clustering. 

2. The main code also uses our developed NHS crawler NHSsearchv5.py and our health information NLP processing libary NHStextNLPprocessAPIv1.py 

3. The generated CPKG triples are in zip file of cknns where contains 383 individul KG and also a integrated KG - nhskg

4. The PKG runtim generation and prediction algorithms are in PGKAndprediction.ipynb file

5. The nhscausalknowledgegraph.owl is the CPKL-based NHS disease ontology

6. There are two datasets for testing, one is without noisy inputs and the other one is with noisy. 

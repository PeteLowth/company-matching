# company-matching

### Exercise
- Develop a model to match "informal" British company names to official company records from Companies House
- The model may consider company name, location, and any relevant information
- An extract of all currently registered companies can be downloaded from here: http://download.companieshouse.gov.uk/en_output.html

### Files:
- data/test_companies.csv - test file generated manually
- postcodes.py - postcode cleaning helper functions
- Companies House Matching.ipynb - Notebook exploring a few approaches to the company matching task
- Companies House Matching.html - An HTML snapshot of a completely run notebook
- model.py - functions used to deploy the k-NN model as a Flask app
- app.py - basic Flask app to deploy the k-NN model as an API
- test_model.py - script to make inferences from the model API

### Model usage:
- To run the Flask app to host model as an API: `python app.py`
- To query the model for some test companies, eg: `python test_model.py "HISCOX", "MUNICH RE DIGITAL PARTNERS"`
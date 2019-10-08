# Predicting Brooklyn Apartment Prices

This project is a regression based modeling project to predict apartment rental prices in Brooklyn. The data used for this project was webscraped from [Trulia](https://www.trulia.com/).

## Files
Below you can find the purpose for each file in this repo:

### Predicting_Brooklyn_Rental_Prices.pdf
Formal project slide deck.

### Trulia_Get_Links.py
Used this file to scrape the links to each listing from the first 200 pages on Trulia. Specifically it receives links for open apartment rentals in brooklyn. 
Steps include:
* Create a user agent to use for the website requests
* Use BeautifulSoup to scrape all links from each search page that contain a specific url string that corresponds to listings
* Save the list of links in a pickle file. (done every so often as well as at the end)

### Trulia_Link_Scrape.py
Used this file to scrape the information of each specific listing. 
**NOTE:** Due to many consistency issues on the website, there will be many times when the information is not grabbed or grabbed incorrectly. The data is actually cleaned in the [Create_Clean_DataFrame.ipynb](https://github.com/Danielo-B/Brooklyn-Apt-Prices/blob/master/Create_Clean_DataFrame.ipynb) file
Steps include:
* Opening the pickled list of links
* Using Selenium and BeautifulSoup together to extract all of the necessary data from each listing
* Create/append to a dataframe that stores the data for each listing

### Create_Clean_DataFrame.ipynb
Used this file to combine and clean the dataframe compiled of each listing:
Steps include:
* Combining smaller dataframes into one large one (I performed the webscrapping over many different runs, so this was necessary)
* Extract needed data from the strings found on the listings. Due to lack of consistency, corrections are made for cases where data was extracted or not present on the listing. Such as: Filling in missing data with the neighborhood mean/medians.
* Save dataframe for future use.

### EDA + Modeling Results.ipynb
Used this file to perform EDA on the cleaned data set as well as to perform various regression/regularization techniques.
Steps include:
* Using a correlation matrix and pairplots to determine the correlation between features
* Use training and validation data set to iteratively find which hyperparameters lead to the best model 
* Evaluate the performance of regression models and calculate metrics that explain business case usability

## Extras


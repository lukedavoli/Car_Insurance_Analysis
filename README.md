# Car Insurance Analysis
A project for some practice with the data science workflow. [Please read the report of my findings!](https://github.com/lukedavoli/Car_Insurance_Analysis/blob/master/Report.md)

## Project Intro/Objective
This analysis aims to provide a brief insight into the relationship of factors such as age and gender with car insurance quote prices. The analysis limits its scope to the individual applying for the quote and assumptions insurance companies may make about them based on these characteristics, rather than what car is being insured.

## Disciplines and Technologies
The project allowed me the opportunity to learn more aboutthe following areas:
* Web automation and web scraping
* Exploratory data analysis
* Inferential statistics
* Data visualization

and improve my skills in the use of:
* Python
* Selenium
* Beautiful Soup
* Pandas
* Matplotlib

## Project Description
### Gathering Data
Data for the project was gathered using web automation tools to retrieve quotes for combinations of personas and cars. The list of personas is found in `people.csv`, each with a name, age and gender. The provided set includes 164 instances, one male and one female for every age between 18 and 98. The list of cars is simply a list of registration numbers for real cars registered in Victoria, Australia, so the `cars.csv` file has been ommitted from the repository for the privacy of the car owners and replaced with `example_cars.csv`.

In order to produce the data in `quotes.csv`, `quote_scraper.py` uses [https://www.comparethemarket.com.au/car-insurance/journey/start](https://www.comparethemarket.com.au/car-insurance/journey/start) to retrieve a number of quotes for each combination of a person and a car.

### Cleaning Data
As can be seen in `cleaning_data.ipynb` i cleaned and cut the data down to the specific focus of the exercise: to examine the relationship between age, gender and comprehensive car insurance quote prices. The resulting dataframe is written out to `quotesByAgeGender.csv`.

### Analysis
All code for plotting the the data from `quotesByAgeGender.csv` can be found in `analysis.ipynb`. Please read the report of my findings [here](https://github.com/lukedavoli/Car_Insurance_Analysis/blob/master/Report.md).

## Disclaimer
I am learning! Please take any findings from this project with a grain of salt. If you have any feedback for me or constructive criticisms of my work please, please reach out I'd love to hear them: ldavoli.mail@gmail.com

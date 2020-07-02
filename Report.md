# Car Insurance Quote Prices: Age and Gender

![RhondaAndKhetut](https://cdn.newsapi.com.au/image/v1/de0f50a298f203baa9c32eaee62917c7)

## Why car insurance? :car:
I recently recieved a quote for the renewal of my comprehensive car insurance in the mail from my insurer. I was shocked by how expensive it was going to be to insure my 8 year old, second hand Volkswagen Passat for the next 12 months. If I continued to pay the same premium for a few more years, I would end up spending the car's value in insurance which I may never make a claim on. Clearly my insurer does not think I am "hot like a sunrise."

There's not much that can be done about this other than to call around to a few different insurers and browse the web to gather some new quotes, and so I did. What I found was that the quote my insurer had given me was fairly standard across the board, with some quoting me over \$5,000. It seemed obvious to me that it shouldn't cost so much to insure a car of this value, so when I got my mum to fetch a quote for my car with her details, it didn't surprise me that she was quoted a touch over \$1,000. 

At this point I should mention that I am a 19 year old male and I am aware of the fact that younger drivers are charged more for car insurance, but I did not expect a discrepancy of this magnitude. I decided to dig a little deeper into how large a role age and gender play in quote prices for comprehensive car insurance.


## Getting the quotes :robot:
I started by gathering a dataset of roughly 6,560 quotes for comprehensive car insurance using Compare The Market's online quote tool. My web automation script filled out their survey 1,640 times using 10 different cars and 164 personas, half male and half female, for ages 18 to 98, recording quotes from Woolworths, Budget Direct, Real and Huddle.

This data could then be aggregated and tidied up to provide us with an average quote price for both genders for every age between 18 and 98.


## Findings :chart:
### Age :girl: :white_haired_woman:
![qpByAge](https://raw.githubusercontent.com/lukedavoli/Car_Insurance_Analysis/master/plots/qpByAge.png)

Based on the results, it is quite clear that age is highly influential to the quote at each extreme of young and old. Prices begin at their peak and sharply decrease as drivers age from 18 to 30, followed by a steady decrease from 35 to 60. Prices begin to surge again once drivers reach the age of 70. The sharp spike between ages 95 and 96 can be explained by Huddle quoting 2 to 3 times more than competitors for drivers past this age (Huddle **really** mustn't want to insure the elderly).


### Gender :female_sign: :male_sign:
![qpByGender](https://raw.githubusercontent.com/lukedavoli/Car_Insurance_Analysis/master/plots/avgByGender.png)

Overall, there seems to be little difference between quote prices for male and female drivers. Across all ages, the average quote for a female driver was $1,934.18, while male drivers were quoted $1,912.87, however, it is not as straightforward as this.


![qpByGenderAge](https://raw.githubusercontent.com/lukedavoli/Car_Insurance_Analysis/master/plots/qpDiffByAgeGender.png)

A closer look suggests that each gender is charged more than the other at different points. For drivers new to the road, males will be charged significantly higher premiums than females. Gradually this gap closes, and eventually female drivers must pay the more costly premium as they age.


![qpByGenderAge](https://raw.githubusercontent.com/lukedavoli/Car_Insurance_Analysis/master/plots/qpGenderCrossover.png)

The crossover takes place at 48 years of age where these values meet. Before and after this point, each gender will consistently pay a higher or lower premium with very few exceptions.


## Conclusion
My findings confirm almost exactly what I expected: insurers hate me and my demographic. Unfortunately, my combined age and gender identity make me an unfavourable insurance risk in the eyes of major car insurance companies, and I will continue to pay a hefty premium for quite a few years to come.

It seems to be no coincidence that AAMI's famous [Rhonda](https://www.youtube.com/watch?v=DL0T_zFaHwU), their ideal customer, is a roughly 50 year old woman and not a fresh P-plater named Jono revving his souped up 2008 Holden Commodore in the VicRoads parking lot.

All the code and data collected as well as a full description of the research process can be found here in [this GitHub Repository](https://github.com/lukedavoli/Car_Insurance_Analysis) :octocat:

Disclaimer: I'm still learning; this project is for practice. Please take what you read here with a grain of salt. If you have any feedback, criticisms or questions please send me an email: ldavoli.mail@gmail.com




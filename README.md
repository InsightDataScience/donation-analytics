**Introduction:**

This repository -- created for a coding challennge -- contains code and associated files designed to sort through political donation data available at the Federal Election Commission's (FEC) website (see here: https://classic.fec.gov/finance/disclosure/ftpdet.shtml#a2017_2018). This program could help political campaigns identify trends in their donations that would be useful for understanding how to target potential donors in the future. The input file for the code can be any of the tables from the FEC's website that is labelled Individual Contributors. The final output file from the code provides data showing trends in the zip codes in which political campaigns received repeat donations. The data should provide useful insights into which zip codes might be especially fruitful for targeting individuals for future donations.

Instructions for the coding challenge are available here: https://github.com/InsightDataScience/donation-analytics

**Required packages:**

The following packages are required to run my program:

pandas  
numpy

**Columns:**

The columns in the output data include, in order:

1) The recipient of the contribution (or CMTE_ID from the input file)
2) The 5-digit zip code of the contributor.
3) The 4-digit year of the contribution
4) The running 30th percentile of contributions received from repeat donors to a recipient streamed in so far for the zip code and calendar year.
5) The total dollar amount of contributions received by a recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
6) The total number of transactions received by a recipient from the contributor's zip code streamed in so far this calendar year from repeat donors.

**Code is well-documented**

Because each line in the code is documented in detail, the easiest way to see how my program works to wrangle the data is to open '/src/donation-analytics.py' and read the code and comments line-by-line.

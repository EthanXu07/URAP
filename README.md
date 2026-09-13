Data Processing and Pipeline for Project

Task Prompt:

Sample data collection task: Choose one of the top finance or economics journal 
(Journal of Political Economy, American Economic Review, Quarterly Journal of Economics, 
Review of Economic Studies, Econometrica, Journal of Finance, Journal of Financial 
Economics, Review of Financial Studies), go through all papers published in that journal's
issues in 2024 or 2025 (do both years if you have time) and put together a table with 
citations (use Google Scholar), ranking the papers from most to least cited. 

Tools:
BeautifulSoup, CrossRef API

Journal: American Economic Review

Timeline: 2024-2025

Code works like this:
Run DataPreparation.py to create articles.csv which is stores all the articles and there relevant information.
Then Run PostProcessing.py to create articles_sorted.csv which is sorted by citation count in descending order.

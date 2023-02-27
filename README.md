# SU_WebScraper
Basic WebScraper for campus staff pages. Missing things like the validators library for URL validation, abstract parent class since 
webscrapers have to change based on the site they pull from, etc. A nice simple proof of concept though with basic documentation within the single .py.

Requires pandas, requests, and beautifulsoup. Uses a recursive loop and writes the output of the dataframe it makes based on staff webscraped pages regardless of
whether the operation was successful or not.

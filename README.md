# visual-testing
Small tool for visual testing with python &amp; selenium

To run the layout tests use: 

`py.test -m --browser=firefox --html=report.html --domain_staging=stepik.org --domain_production=https://stepik.org`

You need [geckodriver](https://github.com/mozilla/geckodriver/releases) to run on Firefox and [chromedriver](http://chromedriver.chromium.org/downloads) to run on Google chrome. Put them as the PATH variable on your computer (or just in your working directory).

Enjoy! 

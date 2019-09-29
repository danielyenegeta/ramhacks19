# Stock5

Stock5 allows users to assess the health of stock symbols. It does this by first scraping economical sites
to retrieve information on how the economy is doing (GDP, Unemployment Rate), then it creates a forecast using FBProphet from that data. In the end, the user gets a report on the forecast and 
how the stock is doing. 

We wanted to make a helper that allows a user to see how well or bad a stock might do in the near future. We came up 
with this through our own pursuits of trying to get rich quick. What better way then a machine telling you where to spend 
your money :). 


Through this project, we learned the difficulty of connecting to a database, how difficult it can be when a service 
your project depends on just doesnt work, and that hardwork prevails. 
 
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
python3+
```

### Installing

First download all modules from the requirements.txt. 
```
pip install -r requirements.txt
```
Although this is not recommended, listed out our public keys in the repository. In order to run the app, you must have downloaded aws cli in the command line. Once you have that type
```
aws configure
```
after that it will ask for an access key. Use this.

```
Access key = AKIAIC5X5TGNGNZBRTEA
Secret key = hU+Hn/KJUkKjy5KF6xY4loINbJkVIRVmQwKdhMoX
```

after that, click enter all the way till your out of the menu. 

Then type 

```
export FLASK_APP=hello.py
```

finally 
```
flask run
```
If you get any errors, please look through your terminal and try to debug the code. Most of the times you will get an error for 
not downloading the modules correctly. 
## Deployment

This site can be hosted either on Heroku, or using Docker and going through the ECS setup. 
## Built With

* [Flask](https://palletsprojects.com/p/flask/) - The web framework used
* [AWS](https://aws.com/) - Cloud Software
* [Pandas](https://pandas.pydata.org/) - Data Analytics Tool

## Authors

* **Zabih Yousuf** - *Developer* - [Linkedin](https://www.linkedin.com/in/zabihyousuf/)
* **Daniel Yenegeta** - *Developer* - [Linkedin](https://www.linkedin.com/in/daniel-yenegeta/)


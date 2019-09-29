# Stock5

Stock5 allows users to assess the health of stock symbols. It does this by first scraping economical sites
            to retrieve information on how the economy is doing (GDP, Unemployment Rate), then it
            creates a forecast using FBProphet from that data. In the end, the user gets a report on the forecast and
            how the stock is doing.
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
aws configure (it will then ask for 
```
then type 

```
export FLASK_APP=hello.py
```

finally 
```
flask run
```

## Deployment

This site can be hosted either on Heroku, or using Docker and going through the ECS setup. 
## Built With

* [Flask](https://palletsprojects.com/p/flask/) - The web framework used
* [AWS](https://aws.com/) - Cloud Software
* [Pandas](https://pandas.pydata.org/) - Data Analytics Tool

## Authors

* **Zabih Yousuf** - *Developer* - [Linkedin](https://www.linkedin.com/in/zabihyousuf/)
* **Daniel Yenegeta** - *Developer* - [Linkedin](https://www.linkedin.com/in/daniel-yenegeta/)


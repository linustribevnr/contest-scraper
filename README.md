# Contest Scraper

[Contest Scraper](https://contest-scraper.herokuapp.com/) fetches details of contests hosted on CodeChef, Codeforces and many others.

Please don't hesitate to file an issue or contribute if you see anything missing.

## Use Case
Currently, the data fetched by the API is used to post stories on Turing Hut's [instagram page](https://instagram.com/turing.hut)

## Installation
```
git clone https://github.com/linustribevnr/ContestScraper.git
```
(Virtual Environment Recommended)
```
sudo apt-get install python-virtualenv
python3 -m venv venv
. venv/bin/activate
```
```
pip install -r requirements.txt
```

## Running
```
python3 server.py
```
This launches a simple local server for development.

## Usage
* GET /contests - fetches details of contests happening on that day
* GET /allcontests - fetches the details all the upcoming contests
* POST /download?json=`<contest-data>` - generates the image representation of the contest details to post on instagram
<img src="https://raw.githubusercontent.com/linustribevnr/contest-scraper/master/imgs/example.jpeg" alt="Example Image" width="250">





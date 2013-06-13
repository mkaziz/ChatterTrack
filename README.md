ChatterTrack
============

# Overview

Simply put, ChatterTrack identifies trends among a certain user's twitter followers. It allows publishers to track all tweets tweeted by a subset of a twitter user's followers, and store them. It then uses KnightLab's tweet classifier: http://classify.knilab.com/ to classify the tweets, and also performs other analyses on them.

We are building this app for the Spring 2013 edition of Northwestern University's EECS 395 - Technology and Innovation in Journalism, hoster by Professors Larry Birnbaum and Rich Gordon.

Team:
Bryan Lowry (Journalist)
Liu Liu
Khalid Aziz


# Installation

The application runs off of Django and Apache. You may need to adapt it to get it running off of your favourite webserver. Here is a link to the django documentation that will help you set up your Django installation with Apache: https://docs.djangoproject.com/en/1.2/howto/deployment/modwsgi/

## Installation Steps

1. Make sure you have python (we used version 2.7) and pip installed.
2. (recommended but not required) Set up a virtualenv to run the application in.
3. Use pip to install the packages in the requirements.txt file: `pip install -r requirements.txt` This will install all python-related libraries required for the application to work.
4. You may need to install some dependenices that don't come with your default python configuration. We had to install `python-dev` and the latest version of `gcc` for `python-nltk` on Ubuntu. `python-nltk` may also prompt you to download a corpus that it requires to function, in which case, it will guide you through the download. 
5. This project requires an account with the Twitter content provider Datasift: http://www.datasift.com Set up an account with Datasift, and add the username and the license key of your account to the Django settings file under the commented datasift heading.

# Contact

For any questions about the project, feel free to contact kaziz@u.northwestern.edu

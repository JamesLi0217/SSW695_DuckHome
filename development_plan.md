# Apartment Finder Website
Jun Zhe  
Ziang Lin  
Pan Chen  

Team Name: Duck Home

| No. | Date    |  Content                    | Version |
|:---:|:-------:|-----------------------------|:-------:|
| 1   | Feb 7th | Initialize development plan | V 1.0   |

## INTRODUCTION
Many students come to Stevens over the world. Since school doesn’t have enough dormitory, they need to find an ideal apartment themselves.  But there are few websites help students find a safe, affordable and accessible apartment easily.

We aim to build an Apartment Finder Website collecting data from communities around Stevens campus, which includes the following features:
* House Owners could post ad (house information, the format can be text, picture, and video)
* Search communities’ information around the campus about communities by distance, price, and evaluation. Communities’ streetscape can be provided through Google Map API.
* A Forum for communication, users can thumb and forward other’s comments. (text only) E.g. Reddit 
* Recommendation: according to the users' behavior, post source they may interest in. Related tech: Machine learning.
* Navigation: show the path between user and destination and provide navigation for the user based on Google Map API.
* Appointment(link with Email): Users could make an appointment with the landlord(House Owner) and send inbox message. Require sign in with email.

##  ROLES AND RESPONSIBILITIES
Development Lead (Jun Zhe)  
Buildmeister (Ziang Lin)  
Architect (Zhe Jun)  
Developers (ALL)  
Test Lead (Ziang Lin)  
Testers (ALL)  
Documentation (ALL)  
Documentation Editor (ALL)  
Designer (Pan Chen)  
User advocate (Ziang Lin)  
Risk Management (Ziang Lin)  
System Administrator (Jun Zhe)  
Modification Request Board (Pan Chen, ALL)  
Requirements Resource (Pan Chen)  
Customer Representative (ALL)  
Customer responsible for acceptance testing  

##  METHOD
### Software:
* Language: Python 3.6  
* Operation System: macOS Mojave version 10.14
* Software Packages: 
Django v2.1.5, pyfirebase v1.3, pymango v3.7, react v4.3, tensorflow v1.13, Boto3 v1.9, GoogleMapsApi v0.02, BeautifulSoup4 v4.7, urllib3 v1.24
* Code Conventions: PEP-8 Style Guide for Python


###  Hardware:
* Development Hardware: MacBook
* Test Hardware: MacBook
* Target / Deployment Hardware: MacBook


###  Back up plan: 
* GitHub Repository


###  Review Process:
* An agile team includes 3 members, review the requirements during the life cycle.

###  Build Plan:
* Revision control system and repository used: GitHub Repository
* Regularity of the builds: daily
* Deadlines for the builds: each Wednesday
* Multiplicity of builds


###  Modification Request Process:
* MR tool: GitHub branch
* Decision process: Teammates vote
* Two develope stream work simultaneously(front-end and back-end)

##  Virtual and Real Work Space
* Virtual Work Space: Google Drive, GitHub, Wechat  
* Real Work Space: Library Study Space

##  COMMUNICATION PLAN
We will divide our project into some sprints, and we have some meetings in every sprint.
* Sprint Planning: We will identify our needed features in the sprint, compute time needed and assign the work to everyone.
* Daily Standup Meeting: Everyone should create a new build at least once per day, and we should describe what we have done and what we will do.
* Review meeting: Every sprint we should compare planned features to actual features, update the product architecture and requirements, re-estimate the incomplete features.

##  TIMELINE AND MILESTONES
* Week of Feb 14th – the first demo
* Week of Mar14th - the second demo
* Week of Mar 28th - the third demo
* Week of Apr 18rd - presentation expectations
* Week of Apr 25th - final presentation
* Week of May 9th - Project Due

##  RISKS
* Database crash - Create a backup database to copy the dataset weekly in case the main database crashes and data missing. The tool we use to monitor the database is mongostat. The mongostat utility provides a quick overview of the status of a currently running mongod or mongosinstance. mongostat is functionally similar to the UNIX/Linux file system utility vmstat, but provides data regarding mongod and mongos instances.
* Account information disclosure - we can use Fire performance Monitoring to trace the status of user account. Firebase Performance Monitoring is a service that helps you to gain insight into the performance characteristics of your iOS and Android project. You use the Performance Monitoring SDK to collect performance data from your system, and then review and analyze that data in the Firebase console. Performance Monitoring helps you to understand where and when the performance of your system can be improved so that you can use that information to fix performance issues.

##  ASSUMPTIONS
* Each developer could work 15 ~ 20 hours per week for the project.
* Django could satisfy all tech requirements in the project.
* The learning time of prerequisite knowledge is 2 weeks.

##  DISTRIBUTION LIST
Zhe Jun  
Ziang Lin  
Pan Chen

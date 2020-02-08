# Expenses tracker
Expenses tracker is a web app designed to track my expenses every day, it uses firebase as Database and python flask as backend.

## TO DO
* Plots
* Filters
* Sign in
* Comparisons
* ~~Docker~~

## Features
Right now Expenses tracker has 3 sections

### Login System
Every user has an individual tracking, they can not track each others.
![Login](/images/login.png)

### Summary
Here you can register your expenses, and see a little summary of your tracking.
![Summary](/images/summary.png)

### Detail (See all)
Here you can see all your expenses, watch some stats and download in CSV format all your tracking. 
Soon you will see filters and ranges.
![Detail](/images/complete_register.png)

## How to install
1. Install all dependecies using the command ">>pip install -r requirements.txt"
2. Go to your firebase console, create a new project
3. Go to configuration, download a json Key
4. Configure it in your "const.py" file
5. Run the project using the command ">>python main.py"

### If you want to run it with docker...
1. Do everything above 
2. Go to "src" folder
3. Build the Image using the command ">> docker build -t yourusername/expensestracker ."
4. Run the Docker using the command ">>docker run -d -p 8888:5000 yourusername/expensestracker"

## License
This project is under MIT License, use it as you want.

## More interesting projects
I have a lot of fun projects, check this:

### Blockchain
- https://github.com/HectorPulido/Amazon-QLDB-Login-Example
- https://github.com/HectorPulido/Decentralized-Twitter-with-blockchain-as-base

### Machine learning
- https://github.com/HectorPulido/Machine-learning-Framework-Csharp
- https://github.com/HectorPulido/Evolutionary-Neural-Networks-on-unity-for-bots
- https://github.com/HectorPulido/Imitation-learning-in-unity
- https://github.com/HectorPulido/Chatbot-seq2seq-C-

### You also can follow me in social networks
- Twitter: https://twitter.com/Hector_Pulido_
- Youtube: http://youtube.com/c/hectorandrespulidopalmar
- Twitch: https://www.twitch.tv/hector_pulido_
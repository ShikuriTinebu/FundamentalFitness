# FundamentalFitness - SB Hacks X Project

## ☁ Inspiration ☁️
With every new year comes the recurring "New Year's Resolutions" and one of the most popular New Year's resolution of all time is the promise to go to the gym more often. However, getting started is not an easy task considering the amount of planning, dedication, and perserverance it requires. That's where we come in. 

## 🚧 What it does 🚧
FundamentalFitness is an AI driven app which utilizes TensorFlow and Google's Movenet to help with every aspect of a prospective gym-goer's needs. We used pose estimation to generate body point data over a multitude of camera frames then trained our very own datasets and implemented stochastic processes and logistic regression based techniques to achieve binary classification of positive and negative movements. We then integrated these models into the SwiftUI application, supplementarily to the average work-out app's features (ex. scheduling, customized routine, calorie counter, pedometer, etc.) to create a comprehensive beginner friendly exercise app that allows users to learn the fundamentals of fitness. 
(TLDR; It's the best fitness app you will ever use)

## 👷 Challenges we ran into 👷
A couple of challenges we ran into while coding this project were with the front-end and back-end respectively. 
For the front-end, the UI was very difficult to build because none of us had ever coded with Swift and there was a lot of difficulty learning the syntax. For example, when we tried to click one button all the buttons were activated and we had no clue why. After about a dozen hours and countless tutorials, we finally figured out how to correctly implement buttons in Swift. A crucial realization was that at this moment in time, none of us are too great at front-end development.
For the backend, some of the struggles we ran into was training our own dataset and solving the calculations for logistic regression at the probabilistic level. Since none of the datasets we needed were pre-existing, a large chunk of time was dedicated creating a dataset and training our own model to classify to what extent a given exercise is acceptable or not. 

## 🎉 Accomplishments we're proud of 🎉
We're very proud of how much we've been able to implement and learn within the past day. Everything listed above was no easy task, especially for a team that was formed somewhat last minute, and we were able to accomplish a lot. We're proud of that.

## 📙 What we learned 📙
We were able to quickly learn and iterate through new machine learning techniques that we were previously unfamiliar with. Additionally, we were able to integrate a wide variety of services such as TensorFlow, Movenet, and Apple's HealthKit. Finally, we were able to create classifications and analysis of exercise form based only on the provided video sequence. 


## 🔜 What's next for FundamentalFitness 🔜
Moving forward we'd like to make improvements to the UI and diversify the model to accomodate for a larger variety of exercises.


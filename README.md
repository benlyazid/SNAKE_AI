# **BUILD  AI THAT PLAY SNAKE GAME**

### **Short description:**
In this Project I have build a AI that can play snake game using Deep reinforcement learning based on Deep Q-learning Algorithm .

### **DEEP-Q-LEARNING Algorithm:**
The Algo It's one of the most populer algo used in Reinforecement learning, it's start by making a random move then he take a reward for each move like 10 for eating an apple and -0.03 for a simpel move and -1 if he lose then wa save the state, action, reward, next state in a memmory that we will use it to correct the nueral.
### **Nuarl Network Architecteur:**
For the Nueral architecteur I have use **Convolutional neural network (cnn)** taht take a resized  Screenshot of the board-game in shape (10, 10, 1) then he transfere the input to Flatten layer that return the Q value of each action, then we take the action that have the most Q value.
###  **requirements:**
To run the project you should have Python3,Tensorflow, pygame, matplotlib and numpy.
### **Train the Module:**
Training the model take between 25k and 30k epoche then he wille be able to eat 6 apple until 13 apple in one epoch. The model will generate h5 file where he wille save his neural value each time he get 3 in scor, to use this file after in test part, and after each 10 epoch the model will generate a graph of score and steps average in image. 

To train the model use `python3 train.py`.

There is also ` Kaggel_file` if you whant to train the model in server like kaggel or google_colab or any others platform.
### **Test the Module:**
In testing we will upload the generated file to use it 

to test the model use `python3 test.py`.

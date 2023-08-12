# Experimentation Process
(Note: All of the following loss and accuracy numbers refer to the model's performance on the testing set)

To start, I used the same convolutional neural network that handwriting.py used (1 convolutional layer with 32 filters using a 3x3 kernel, 1 max-pooling layer using a 2x2 pool size, a hidden layer with 128 units and 0.5 dropout, and an output layer with output units for all of the sign categories). However, this resulted in a loss of 3.4920 and an accuracy of only 0.0543.

Because of the extremely low accuracy, I decided to add another convolutional layer with 32 filters using a 3x3 kernel and another max-pooling layer using a 2x2 pool size. This resulted in a loss of 0.1607 and an accuracy of 0.9541. Since this greatly improved the accuracy of the model, I tried adding a third convolutional layer with 32 filters using a 3x3 kernel and a third max-pooling layer using a 2x2 pool size; however, this resulted in a loss of 0.2086 and an accuracy of 0.9443, leading me to conclude that the optimal number of convolutional and max-pooling layers were 2.

Next, I tried using 2 hidden layers with 128 units and 0.5 dropout, but this resulted in a loss of 0.3249 and an accuracy of 0.9079, leading me to conlcude that the optimal number of hidden layers and dropout was 1.

I also tried increasing the pool size for my max-pooling layers to 3x3, but this resulted in a loss of 0.9078 and an accuracy of 0.6969. I then tried making the pool size 1x1, and this resulted in a loss of 0.1672 and 0.9612 (my highest accuracy yet), but the training time for this was over 5 minutes; thus, I concluded that the slight increase in accuracy did not warrant the significant increase in training time, so I reverted to using a 2x2 pooling size.

Ultimately, after all of my testing, I found increasing the filters to 64 on the convolutional layers and increasing the number of units on my hidden layer to 256, as well as slightly decreasing the dropout to 0.4, resulted in the best outcome (a loss of 0.1287 and 0.9695). 
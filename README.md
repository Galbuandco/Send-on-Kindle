Send on kindle 
Implemented with socket in python 

This simple script is just a client implementation with socket of a gmail client used to send your pdf (or any other fole supported by Amazon) to your kindle.

It considers two options: 
- amazon don't send a verification mail
- amazon sends you a verification mail

In the first case the code is tested and correctely working while in the second scenario gmail's pop3 protocol seems not to follow the RFC and keep sending the same chunk of mail every time, so it doesn't work yet.

The code is splitted in two sockets modules, one for the smtp socket and the other for the pop3.

The main is just a call to the two functions in the modules, to use it fill the variables and then run it. 

NB: to use it you should disable in your google Account the option of let you access only by official gmail application

The project was mainly made for educational purpose but feel free to use it as you prefer.

# DHT11-main
Python Code: The python code is on py, it does read arduino data sent via serial separated by ";" and CRLF. 
    Time is gathered by python program constantly and written into the csv, with the data received at that time.
    To write the received data into a CSV python needs to decode this data by means of 1) strip (remove unwanted characters) 2)decode (convert to string) .
    The first two data sent by the arduino "data1;data2;...\r\n" will be plotted respect to time, for that it needs to be split(;), converted to float.
    Then these are stacked in an array and plotted, the program can be modified to plot as many graphs or lines as needed.
    
    One of the main features, is that you can power off the arduino readings, or what you need, by means of the PC keyboard keys, which are detected by python. 
    This feature will start on by default, this can be changed in the setup. While working, up key will turn on, and down key will turn off.
    The program will not start plotting until arduino sends the end signal, this must be matched in both programs.
  
Arduino Code: Arduino code will basically do the setup and send it to python code, then, start seeing if theres any data on the serial read, and start printing data
    The sensor used is DHT11 so it uses its libraries, but this can be used to send any other data, this code sends error messages when there's not a valid reading.
    RX is the signal received by the PC, basically configured to be either 1 or 0, activating or deactivating the data transmission
    

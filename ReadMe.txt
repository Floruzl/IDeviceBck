Contents of this Folder:

ReadMe.txt		You are looking at it
IDeviceBck.py 	The source code feel free to browse it's well commented and fairly straight forward.
IDeviceBck.exe 	The executable

Disclaimer:

While there is no code in the program that could result in data loss (it only copies, does not move/remove/delete or anything ever) the changes of anything bad happening are practically zero. But should you somehow manage to lose data or suffer any harm, from using this simple copy script, that is on you. I as the author take no responsibility for any misuse or damage suffered. 





How it works:

IDeviceBck.exe was made a last resort after failing to copy files from my iPhone with other options. The program loops through all the folders of you iPhones DCIM directory and copy those directories and all the files in them to the destination folder.


STEP 1: Make sure your iPhone is not busy/unresponsive and visible from Windows.

The best way to test this is to open an image file from your iPhone through Windows Explorer. (just seeing the folders is not enough)
The most surefire way of getting it back to responsive is restarting it (internet search -> restarting iPhone whichever you have)
This take long and then mounting it in windows take long as well. (please petition Apple to get their stuff together)
 
(Note: to be safe, you can make sure it does not go to autlock after 30 secs and breaks the connection. (internet search -> turning off auto lock on iPhone))


STEP 2: Run the Program

(If there is no config.ini in the folder of the executable the program will make one and prompt you to change the destination path. Source file generally should work)

If the source and destination folders are valid. The program will start going through and copying files until it reaches a corrupt file. 
At this point it will stop and add the file to the skiplist in the destination folder. (you can delete the skiplist of you think non corrupted files got added to it.


STEP 3: Repeat STEP 1 and STEP 2 until the program finishes without hitting a corrupt file. 

Then run it one more time to be sure and check the size of the destination folder to be roughly what you expect. You should now have a complete copy of your files on your windows machine.


Please make a donation to charity of your choosing if this helped you and you wish to pay it forward! Thank you!





More info:


The Problem:

Copying in windows and in other downloaded apps would fail and lock up my iPhone. Causing we to have to start over. What tthis program does differently is that it adds the corrupt file it locks up on to a skip list in nthe destination folder. This way the next time you run, that file will be skipped and the program will carry on where it left off beyond the corrupted file. 


The Solution:

This method still requires you to get your iPhone in a usable state and restart this program manually everytime you hit a corrupt file, which is still very annoying. But since the iPhone often becomes "busy" / unresponsive after hitting a corrupted file it is the best I can do. (please petition Apple to fix their shit, in their support forums they appear to pretend the problem corrupt files do not exist, while the internet is full of people with this problem. 

Given the amount of times I restarted and failed with all the other methods. This method at least has a light at the end of the tunnel and requires minimal managing of files or copying individual folders. And everytime you do restart you get a little closer to a full copy of your files.










  

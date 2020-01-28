# Process_Log
---
#### Gui application to track running processes
The process log is like the task manager. It pulls up a list of running processes. You can select the 3 processes that you would like to track. The program makes and saves a cvs file using the three process names as the name of the file. After the file has been created the gui has a button to view the file as a chart. The button brings up a matplotlib chart ploting the private memory from each process.

#### Easy to use
1. Select a process from the list.
2. Press the selectPid button
3. Repeat two more times
4. Select the time interval 
5. Press the Start. 
6. After a file has been created press the big button to see a chart

Just run the project.py file to start the program. 
Or create an executable with [PyInstaller](https://www.pyinstaller.org/)
#### Remeber the start is the small button
![Start button](https://github.com/HeberCooke/Process_Log/blob/master/images/processLog2.png)
#### Favorite code
```python
class Log(Thread):
  def__init__(self, pid1, pid2, pid3, time):
    Thread.__init__(self)
```
The log class creates a new thread so that the main gui can continue to run
The log object calls the make file method to run the start method
```python
def makeFile(self):
  self.start()

```
I did this after because after the file was created the gui was just stuck while the process continued in the loop to collect data for the file.



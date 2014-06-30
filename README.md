#glass-teach

glass-teach provides a system that allows a teacher (using google glass) to leverage greater control over a lab of computers.

##Commands
Right now, four commands are implemented and are working:

  * **Turn Off Monitors** - Turns off all of the monitors in the lab, blocks keyboard input.
  
  * **Turn On Monitors** - Turns on all of the monitors in the lab, unblocks keyboard input
    
  * **Push A File** - Allows a file to be copied from the teacher computer to all student computers. This is 
                      useful for when a teacher wants to assign a project, or show every student a code example or pdf.
    
  * **Pull A File** - Allows a file to be copied from all student computers to the teacher computer. The main use case for
                      this is for automated assignment turn in.
    
    
One command works most of the time, but fails occasionally due to what I believe is an issue in using tcp for large file
transfers (I plan to iron this out soon):

  * **Record A Lecture** - Begins recording a lecture, automatically labels and uploads the video to the teacher computer.

##What's Here
A system of python scripts (and batch scripts to auto run and hide them), sockets, an AWS server, and glassware.
  * **GlassTeach-ManageFiles-Glassware** - The .apk to be run on Google Glass (these apps are called "Glassware"). This provides the interface for the teacher to issue voice commands. Eclipse project.

  * **glass-teach-server.py** - Bare metal server implementation using python sockets. I ran it on an EC2 instance with a static IP. This is how the glassware communicates with the teacher and student computers. With sockets you have to write your own protocol and I've included some notes about the size and format of packets in comments in the file. Prints are scattered about, so that's the first thing to check if something goes wrong.

  * **glass-teach-student.pyw** - The script to be run on student computers. .pyw extension hides the console while executing.

  * **glass-teach-teacher.pyw** - The script to be run on teacher computers. Both of these files are heavily commented.

  * **glass-teach.exe** - compiled from monitorOff.c, this is what glass-teach-student calls out to when it recieves the command to turn off monitors and block keyboard input. Uses some WinAPI magic. I've included it here becasue it made distrobution throughout the lab easy, but you'll probably have to recompile it.

  * **monitorOff.c** - WinAPI magic. "Disables monitors" by making a full screen black window, and disabling keyboard input. I've included a line about compiling with MinGW and linking with the right libraries.
  
  * **student-init-hide.vbs** - Script placed in the startup directory on student computers to run and hide student-init.bat on startup.
  
  * **student-init.bat** - Script that runs glass-teach-student.pyw 

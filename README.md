glass-teach
===========

glass-teach provides a system that allows a teacher (using google glass) to leverage greater control over a lab of computers.

Right now, four commands are implemented and are working:

  * Turn Off Monitors
    Turns off all of the monitors in the lab, blocks keyboard input.
  
  * Turn On Monitors
    Turns on all of the monitors in the lab, unblocks keyboard input
    
  * Push A File
    Allows a file to be copied from the teacher computer to all student computers. This is useful for when a teacher
    wants to assign a project, or show every student a code example or pdf.
    
  * Pull A File
    Allows a file to be copied from all Student computers to the teacher computer. The main use case for this is for
    automated assignment turn in.
    
    
One command works most of the time, but fails occasionally due to what I believe is an issue in using tcp for large file
transfers (I plan to iron this out soon):

  * Record A Lecture
    Begins recording a lecture, automatically labels and uploads the video to the teacher computer
    

Installation and Configuratation instructions coming soon.

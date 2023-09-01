>**Remote System Cleaner**

RSC stands for remote system cleaner. It is a micro interactive 
shell software designed to maintain the file systems of the servers
in the datacenter. It has two versions available as below:

1) SGD version(RSC_SGD_beta.sh)
2) PuTTy version(RSC_puTTY_beta.sh)
3) id.sh
4) GCS.sh

1. SGD version : This shell software is by default compatible with SGD(Secure global desktop) as the display of the shell is integrated 
   with the local computer in the SGD session. Users who are using SGD for operating the script need to just run the script and proceed.

2. PuTTy version : The scripts is also useful for users who prefer using puTTy application for their daily work, the only condition in the 
                   beta version is that the user should have access to the secure global desktop application also. The puTTy application 
                   does not integrate the shell display with the local computer, which is a problem considering the utility of this 
                   script. To overcome this problem, a mix use of puTTy and SGD has been considered here for leveraging the GUI capabilities
                   of the linux shell.

3. id.sh         : It stands for integrate display, it genrates the display varibale for the current SGD session.

4. GCS.sh        : It stands for garbage collector script, it is an auxilary script which is used in case the script is terminated abruptly 
                   by using "ctrl+z". It makes the further functioning of script smooth and error free. make sure to run this script
                   if in case you have used "ctrl+z" to terminate the script before running the script again.


A) About the application architecture :-
     -This is a centralized program, it stays on the jump server at a single location and as per demand it logs on to a remote s
      erver to fetch realtime data and do the neccesary processing. The functional steps are mentioned below:-
       
       --It takes a server name as input(make sure that you have passwordless access to the server).
       --Then it logs on to the server and fetches the current state of the file systems on that server which are more than 70% full.
       --Then it asks the user for their choice to explore a particular partition and dig deeper. 
       --Once a choice is entered, it runs back to the server and fetches the complete file system information, in the form of recur
         sive listing of the file system hirearchy.
       --Then a logical data processing takes place where the file system partition is analysed logically(Basically parsing data).
       --Then right after that a virtual model of the original remote file system is built on the local server .i.e. script home .
       --Here we leverage the GUI features of the linux shell to accelerate the process of manual file system exploration. Once the
         partition is built up completely, the script asks the user to explore the virtual model and make decisions for managing the 
         actual remote file system.
       --Based on the decisions the user takes the script genrates an execution plan, by following several methods for mapping the 
         virtual model to the original remote file system.
       --Once the user has completed the decision making process they can give ***"N"***(caps only) as input to see the execution pla
         n and either proceed or terminate further.
       --Once the execution plan is shown to the user they are asked for confirmation, if you confirm then the script will proceed 
         further to the remote server and perform the intended action choosen by you. If you reject the execution plan the script 
         clean up and terminate.
       --Once the script has completed one cycle of cleaning, it will show the file systems again to you, for exploration . You can e
         ither keep exploring the file systems of that remote server or you can quit th script by typing ******"q" or "Q"******.
 
                         
  
B) The execution plan :-
     -Execution plan is the list of options and inputs that the user has selected or provided in text. It has the following parts:-
       
         --Age option : It is the a positive integer which represents the number of days. Files older than "age" number of days will
                        be processed.
                        WARNING NOTE: Always keep the age as positive integer only keeping in mind the purpose of script.
         --extension  : It is a free style text input and it totally depends upon the user as what they give in the form of input.
                        This option will be processed accordingly, it is the same as we use in the find command as "-name" option.                   

         --zip or remove : These are the two options offered to the user for a particular file batch(always enter numeric values 
                            1 for zip and 2 for remove).
         --file system : This option is automatic, it gets registered when you first select the file system for exploration.
         --remote server : It is the remote server name that you have provided. 




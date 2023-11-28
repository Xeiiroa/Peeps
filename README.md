# Python security camera cli application

## A python security cameara program that uses opencv to detect faces and starts recording when detected

This project was an intro for my learning of machine learning models as well as computer vision and managing of specific funcitonalities that smaller projects didnt let me use in a more common setting such as 

* File management
* Sqlite
* dynamic use of a command line interfaces


## Commands

since this runs as a script i made it in a way that it could run in commands as thats what im most comfortable with as well as the person i made this for so here are the commands:

### Get commands

* help: Prints out all the commands

* get_video_save_path: Prints where your recordings will be saved to
 
* get_phone_number: prints the current phone number thats saved
note that you will need to have a twilio account to be able to be sent messages

* get_delay: Gives you the current delay time you have set to give you time to leave the room before recording can start 

### Change Commands

* change_video_save_path: opens a file dialog to allow you to choose a new video save path

* change_phone_number

* change_delay




## How to run 

1. Clone the repository
2. Create a twilio account to register phone number and get account id
3. change the env variables that are labeled in red to your id and token in notificatioins.py in the utils folder 
4. all commands run under an argparser so if you want to change a setting you would run "python main.py --settings (command)"


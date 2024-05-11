**ABOUT SCRIPT AND SECURITY**

> **SCRIPT:**
         The script in main.py is responsible to run your discord bot and create a slash command in your bot.
>        The slash command will be used to setup a ticket panel in selected channel.
>        A button will be sent in selected channel.
>        The button will be responsible for opening ticket and logging it channel.
>        The button will also send a ticket control button in the created ticket.
>        Ticket channel will be stored in JSON file(ticket_data.json) to keep track of ticket activities such as total messages sent and by what user.
>        The script also imports some of the inputs and settings from ticket_setup.py
>        The script uses on_message event on your bot which helps keeps tracks of ticket messages and user messages count and helps update them.
>        The ticket information stored in JSON file(ticket_data.json) is displayed on logging message when ticket is closed.
>        The script will send logging in detail. Covering user info, ticket info and messages sent in ticket info.
>        The script requires you to give it a ticket manager role ID. Ticket manager role gets access to every ticket that is opened.
>        The script tells you to put both, Logging channel ID and ticket manager role ID and also asks you to paste in your bots token.
>        Your logging channel ID is used to send logs of every ticket that is opened/closed.
>        Your Manager role ID is given access to every ticket that is opened.
>        Your bot token is used to implement this all in your discord bot.


> **SECURITY:**
>         Please make sure to always keep your discord bot token private. Do not share it with anyone online.
>         If you understand Python i'd strongly recommend you to create a environment file where you can put your secrets and import them in main file.
>         The script is NOT made to steal anyones token or anything. Do not fell for anyone telling you this. They are most likely trying to get your token.
>         The main goal of the script is to make a ticketing system inside your discord bot.
>         Please NEVER put anyone else script inside this one. Only paste it if you understand the script and trust the author.
>         If you are running this script in replit then i HIGHLY suggest you to use "secrets" built-in feature of replit as anyone can access your repl and grab 
>         your bot token if your repl is public.
>
>                                                    **PLEASE USE THIS SCRIPT WITH CAUTION**



> **EXTRAS:**
>
>   There are some extra things i'd like to mention.
>
>         **RIGHTS & OTHERS:**
>                You have full rights to use this script. But you are not allowed to claim ownership of this script by yourself.
>                it'll be very kind of you to give me credits. This script is my hard work.
>                Please remember that i will not be responsible for anything caused by this script after you pasted somebody else script or if you leak your bot token.
>                As mentioned above. The scripts main goal is to create a working ticketing system on your bot. Nothing else...
>
>                If you love the script please considering liking this repository This will motivate me. Script made by: mr_baconhat(Discord) :]
>
>                Feel free to reach out to me if you have any questions (i may not always accept your request)

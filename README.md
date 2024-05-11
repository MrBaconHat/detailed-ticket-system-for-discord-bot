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

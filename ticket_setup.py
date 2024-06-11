"""
____________________________________________________NOTE________________________________________________________________

PLEASE DO NOT RENAME ANYTHING INSIDE THIS FILE. THE FILE TAKES CARE OF A LOT OF THINGS.
PLEASE DO NOT REPLACE ANYTHING WITH ANYTHING....

IF YOU ARE NOT SURE ABOUT WHAT TO DO PLEASE WATCH MY YOUTUBE VIDEO ON THE SCRIPT.

                                                 NAME: Mr_BaconHat

"""


"""___________________________________________TICKET FUNCTION SETTINGS_______________________________________________"""

ticket_category_id = ""
# ^  category where you want tickets to be made. (OPTIONAL)


ticket_manager_role_id = ['1231778425060982815']  # separate with coma.
# ^  ticket managers will get access to tickets. (REQUIRED)


ticket_logging_channel_id = "1232312201126219806"
# ^  this is where tickets will be logged if ticket is created or closed. (REQUIRED)

seconds_before_deleting_ticket = 15
# ^  after how many seconds ticket should be deleted when closing? (REQUIRED)

ticket_limit_per_user = 2

include_bot_messages_in_logs = True  # this effects every single bot.
include_bot_ticket_messages_count = False  # this effects every single bot.

dm_transcript_to_ticket_author = True


"""___________________________________________TICKET BUTTON CUSTOMIZATION____________________________________________"""


create_ticket_button_text = "Create a ticket"
create_ticket_button_color = 'green'
create_ticket_button_emoji = None

close_ticket_button_text = "Close ticket"
close_ticket_button_color = 'red'
close_ticket_button_emoji = None

view_transcript_button_text = 'View Transcript File'
view_transcript_button_color = 'green'
view_transcript_button_emoji = None


#  you can only use the following colors: red, green, gray, blue


"""___________________________________________TICKET MESSAGES CUSTOMIZATION__________________________________________"""


message_on_creation = "Hey, {user_mention} Please be patient and explain your issue. {manager_role}"
message_on_creation_ephemeral = "Successfully created your ticket: {ticket_mention}"
# the message you want to send when ticket is created. (REQUIRED)
#  ^ you can put "{server_name}" to display your server name. this will be replaced by your server name
#  ^ you can also use: "{user_name}" or "{user_mention}" or "{user_id}" to get user info
#  ^ you can also use: "{manager_role}" to mention the ticket manager role!
#  ^ you can also use: "{ticket_name}" to display ticket name!
#  ^ you can also use: "{ticket_id}" to display ticket ID!
#  ^ you can also use: "{ticket_mention}" to tag the ticket!


message_on_deletion = 'ticket will be deleted in: {seconds_countdown} {user_mention}'
#  ^ the message you want to send when ticket is being closed. (REQUIRED)
#  ^ you can also use: "{seconds}" or "{seconds_countdown}" to display how many seconds until ticket closes.
#  ^ you can put "{server_name}" to display your server name. this will be replaced by your server name
#  ^ you can also use: "{user_name}" or "{user_mention}" or "{user_id}" to get user info
#  ^ you can also use: "{manager_role}" to mention the ticket manager role!
#  ^ you can also use: "{ticket_name}" to display ticket name!
#  ^ you can also use: "{ticket_id}" to display ticket ID!
#  ^ you can also use: "{ticket_mention}" to tag the ticket!


description_on_button_embed = 'press button below to create a ticket.'
title_on_button_embed = "{server_name}'s ticket support."
footer_on_button_embed = "Do not open tickets for no reason..."
#  ^ you can use "{server_name}" and "{server_id}"

ticket_transcript_display_on_file = ('Message Info:\n'
                                     ' |\n'
                                     ' | Author: {user_name}\n'
                                     ' | Message: "{content}"\n'
                                     ' | Sent at: {sent_at}\n\n'
                                     'User Info:\n |\n'
                                     ' | User ID: {user_id}\n'
                                     '----------------------------------------\n\n')

ticket_limit_exceed_message = "You have exceeded the ticket limit. You've currently opened: {ticket_user_limit} tickets"

"""___________________________________________SCRIPT SETTINGS (SENSITIVE)____________________________________________"""
"""
NOTE: DO NOT MAKE ANY CHANGES, ONLY MODIFY IF YOU KNOW WHAT YOU ARE DOING.
"""

reactivate_ticket_creation_buttons_on_startup = True

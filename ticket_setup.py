"""
____________________________________________________NOTE________________________________________________________________

PLEASE DO NOT RENAME ANYTHING INSIDE THIS FILE. THE FILE WILL TAKE CARE OF A LOT OF THINGS.
PLEASE DO NOT REPLACE ANYTHING WITH ANYTHING....

"""


"""___________________________________________TICKET FUNCTION SETTINGS_______________________________________________"""

ticket_category_id = ""
# ^  category where you want tickets to be made. (OPTIONAL)


ticket_manager_role_id = "12345"
# ^  ticket managers will get access to tickets. (REQUIRED)


ticket_logging_channel_id = "12345"
# ^  this is where tickets will be logged if ticket is created or closed. (REQUIRED)

seconds_before_deleting_ticket = 15
# ^  after how many seconds ticket should be deleted when closing? (REQUIRED)


"""___________________________________________TICKET MESSAGES SETTINGS_______________________________________________"""


message_on_creation = "Hey, {interaction.user.mention} Please be patient and explain your issue"
# the message you want to send when ticket is created. (REQUIRED)
#  ^ you can put "{interaction.guild.name}" to display your server name. this will be replaced by your server name
#  ^ you can also use: "{interaction.user.name}" or "{interaction.user.mention}" to ping user who opened the ticket.


message_on_deletion = 'ticket will be deleted in: {seconds_before_deleting_ticket} seconds'
#  ^ the message you want to send when ticket is being closed. (REQUIRED)
#  ^ you can also use: "{seconds_before_deleting_ticket}" to display how many seconds until ticket closes.


description_on_button_embed = 'press button below to create a ticket.'
title_on_button_embed = "{ctx.guild.name}'s ticket support."
footer_on_button_embed = "Do not open tickets for no reason..."

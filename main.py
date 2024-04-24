import discord
import asyncio
import sys
import json
import time
from datetime import datetime, timedelta
from discord.ext import commands
from typing import NoReturn


intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
intents.message_content = True


"""
___________________________________________________________NOTE_________________________________________________________

PLEASE USE THIS CODE WITH CAUTION. DO NOT ATTEMPT TO CHANGE ANYTHING UNLESS YOU KNOW AND UNDERSTAND THE SCRIPT PURPOSE.
TO NOT PASTE ANY SCRIPT IN THIS ZONE. THE SCRIPT CAN BE MALICIOUS AND CAN RESULT IN DAMAGING THE BOT AND GIVING 
UNAUTHORIZED ACCESS TO SOMEBODY OF YOUR BOT. DO NOT SHARE THIS SCRIPT WITH ANYONE IF YOU HAVE YOUR BOT TOKEN PLACED.
DOING THAT WILL RESULT IN GIVING BACKDOOR OF YOUR BOT TO SOMEBODY.

CREATOR OF THIS SCRIPT(mr_baconhat, me) WILL NOT BE RESPONSIBLE IF YOU ENDED UP LEAKING SOMETHING IMPORTANT 
SUCH AS YOUR BOT TOKEN.

                                                    YOU HAVE BEEN WARNED..                                                    

IF YOU UNDERSTAND PYTHON YOU SHOULD CREATE .env(environment) FILE TO SECURE YOUR BOT TOKEN. 
BUT IF YOU DON'T UNDERSTAND PYTHON AT ALL YOU CAN CONTINUE USING SCRIPT LIKE THIS BUT BE SURE TO NOT SHARE THIS SCRIPT
WITH ANYONE WITH YOUR BOT TOKEN PLACED INSIDE IT.
              
                                                   made by: mr_baconhat :]
                                                   
IF YOU HAVE ANY QUESTIONS ABOUT THE SCRIPT OR WANT TO SUGGEST SOMETHING PLEASE CONTACT: mr_baconhat(discord)
________________________________________________________________________________________________________________________
"""


ticket_category_id = "12345"  # category where you want tickets to be made. (OPTIONAL)
ticket_manager_role_id = ""  # ticket managers will get access to tickets. (REQUIRED)
ticket_logging_channel_id = "12345"  # this is where tickets will be logged if ticket is created or closed. (REQUIRED)

BOT_TOKEN = "your bot token here"  # the token of your bot. it will be used to run the bot and add the commands to it.
# ^ (REQUIRED)

"""
ONLY ENTER THIS ZONE IF YOU UNDERSTAND EVERYTHING.
"""

if not ticket_manager_role_id.isdigit():
    sys.exit('Please put your manager role ID.... It is a required input....')

if not ticket_logging_channel_id:
    sys.exit("Please paste a logging channel ID....")


def save_ticket_to_json(ticket_channel_id: str) -> NoReturn:

    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    ticket_data['opened_tickets'][str(ticket_channel_id)] = {}

    with open('ticket_data.json', 'w') as write_file:
        json.dump(ticket_data, write_file, indent=4)


def clear_ticket_from_json(ticket_channel_id: str) -> NoReturn:
    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    del ticket_data['opened_tickets'][str(ticket_channel_id)]

    with open('ticket_data.json', 'w') as write_file:
        json.dump(ticket_data, write_file, indent=4)


def add_members_to_json(ticket_channel_id: str, member_id: str) -> NoReturn:
    str_ticket_channel_id = str(ticket_channel_id)
    member_id = str(member_id)
    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    if member_id not in ticket_data['opened_tickets'][str_ticket_channel_id]:
        ticket_data['opened_tickets'][str_ticket_channel_id] = {
            **{users_id: counter for users_id, counter in ticket_data['opened_tickets'][str_ticket_channel_id].items()},
            member_id: 1
        }

    else:
        counter = ticket_data['opened_tickets'][str_ticket_channel_id][member_id]
        counter += 1
        ticket_data['opened_tickets'][str_ticket_channel_id] = {
            **{users_id: counter for users_id, counter in ticket_data['opened_tickets'][str_ticket_channel_id].items()},
            member_id: counter
        }

    with open('ticket_data.json', 'w') as write_file:
        json.dump(ticket_data, write_file, indent=4)


def get_ticket_total_msgs(ticket_channel_id):
    ticket_channel_id = str(ticket_channel_id)
    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    counter: int = 0
    for counts in ticket_data['opened_tickets'][ticket_channel_id].values():
        counter += counts
    print(counter)
    return counter


def get_all_ticket_users(ticket_channel_id) -> dict:
    ticket_channel_id = str(ticket_channel_id)

    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    user_all_msgs_count = ticket_data['opened_tickets'][ticket_channel_id]

    dictionary = {f"<@{users}>": counter for users, counter in user_all_msgs_count.items()} \
        if user_all_msgs_count.items() else {"No Messages were sent": 0}

    return dictionary


class CreateAChannelButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=7776000)

    @discord.ui.button(label='Create a ticket', style=discord.ButtonStyle.success)
    async def create_channel(self, interaction: discord.Interaction, button: discord.ui.Button) -> NoReturn:
        if button:
            pass

        guild_category = None if not ticket_category_id.isdigit() else await bot.fetch_channel(int(ticket_category_id))
        guild_role: discord.Role = interaction.guild.get_role(int(ticket_manager_role_id))
        guild_everyone_role: discord.Role = interaction.guild.get_role(interaction.guild.id)
        logging_channel = bot.get_channel(int(ticket_logging_channel_id))

        role_overwrite = discord.PermissionOverwrite.from_pair(
            discord.Permissions(117824),
            discord.Permissions.none()
        )

        user_overwrite = discord.PermissionOverwrite.from_pair(
            discord.Permissions(117824),
            discord.Permissions.none()
        )

        everyone_role_overwrite = discord.PermissionOverwrite.from_pair(
            discord.Permissions.none(),
            discord.Permissions.all()
        )

        guild_permission_format = {

            guild_role: role_overwrite,
            interaction.user: user_overwrite,
            guild_everyone_role: everyone_role_overwrite

        }

        created_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}",
                                                                      category=guild_category,
                                                                      topic=f'This is a ticket of: '
                                                                            f'<@{interaction.user.id}>',
                                                                      overwrites=guild_permission_format)
        save_ticket_to_json(str(created_channel.id))
        start_time = time.time()

        await interaction.response.send_message(f"Successfully created your ticket: {created_channel.mention}",
                                                ephemeral=True)

        ticket_created_formatted_date = datetime.strftime(created_channel.created_at, '%Y/%m/%d %H-%M-%S')
        ticket_created_formatted_date = datetime.strptime(str(ticket_created_formatted_date),
                                                          '%Y/%m/%d %H-%M-%S')

        user_creation_formatted_date = datetime.strftime(interaction.user.created_at, "%Y/%m/%d %H-%M-%S")
        user_creation_formatted_date = datetime.strptime(user_creation_formatted_date, '%Y/%m/%d %H-%M-%S')

        user_guild_creation_formatted_date = datetime.strftime(interaction.user.guild.created_at, "%Y/%m/%d %H-%M-%S")
        user_guild_creation_formatted_date = datetime.strptime(user_guild_creation_formatted_date,
                                                               '%Y/%m/%d %H-%M-%S')

        embed = discord.Embed(
            title='Ticket Created',
            description=f"Ticket opened by: {interaction.user.name}\n\n"
                        f"__User Info:__\n\n"
                        f"- **User ID:** {interaction.user.id}\n"
                        f"- **User Mention:** {interaction.user.mention}\n"
                        f"- **Creation Date:** <t:{int(user_creation_formatted_date.timestamp())}:f>\n"
                        f"- **Server Member:** <t:{int(user_guild_creation_formatted_date.timestamp())}:f>\n\n"
                        f"__Ticket Info:__\n\n"
                        f"- **Ticket Name:** {created_channel.name}\n"
                        f"- **Ticket Creation:** <t:{int(ticket_created_formatted_date.timestamp())}:f>\n"
                        f"- **Ticket Channel ID:** {created_channel.id}\n"
                        f"- **Ticket Mention:** {created_channel.mention}",
            color=discord.Color.brand_green()
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_author(icon_url=interaction.user.avatar, name=interaction.user.name,
                         url=f'https://discord.com/users/{interaction.user.id}')
        logging_message = await logging_channel.send(embed=embed)

        view = CloseTicketButton(channel_object=created_channel, ticket_author_object=interaction.user,
                                 guild_object=interaction.guild, ticket_category_object=guild_category,
                                 ticket_manager_role_object=guild_role, start_time=start_time,
                                 ticket_creation=ticket_created_formatted_date, logging_message_object=logging_message,
                                 guild_joined_date=user_guild_creation_formatted_date,
                                 user_join_date=user_creation_formatted_date, logging_channel=logging_channel)

        await created_channel.send(f"""Welcome! {interaction.user.mention} 
Please explain your issue and one of our staff will be with you to assist you.
Please make sure to follow server rules and be patient. do not spam ping any of our {guild_role.mention}. 

Thanks! -{interaction.guild.name} team.
""",
                                   view=view)


class CloseTicketButton(discord.ui.View):

    def __init__(self, channel_object, ticket_author_object, guild_object, ticket_category_object,
                 ticket_manager_role_object, start_time, ticket_creation, logging_message_object,
                 guild_joined_date, user_join_date, logging_channel):
        super().__init__(timeout=7776000)

        self.user_channel = channel_object
        self.ticket_creator = ticket_author_object
        self.ticket_guild = guild_object
        self.ticket_category = ticket_category_object
        self.ticket_manager_role = ticket_manager_role_object
        self.ticket_start_time = start_time
        self.ticket_created_time = ticket_creation
        self.logging_message = logging_message_object
        self.guild_joined_date = guild_joined_date
        self.user_join_date = user_join_date
        self.logging_channel = logging_channel

    @discord.ui.button(label='Close ticket', style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.button) -> NoReturn:
        if button:
            pass
        await interaction.response.send_message('This ticket will be deleted in 15 seconds...')
        await asyncio.sleep(15)
        await self.user_channel.delete()

        total_msgs = get_ticket_total_msgs(self.user_channel.id)
        all_users_msgs = 0 if not get_all_ticket_users(self.user_channel.id) \
            else get_all_ticket_users(self.user_channel.id)
        end_time = time.time()
        ticket_end_time = datetime.now()

        ticket_deleted_formatted_date = datetime.strftime(ticket_end_time, '%Y-%m-%d')
        ticket_deleted_formatted_date_unix = datetime.strptime(str(ticket_deleted_formatted_date), '%Y-%m-%d')

        active_duration_seconds = int(end_time) - int(self.ticket_start_time)
        formatted = timedelta(seconds=active_duration_seconds)

        formatting_datetime = datetime.strptime(str(formatted), '%H:%M:%S')

        formatting = (f'{formatting_datetime.hour}H '
                      f'{formatting_datetime.minute}M '
                      f'{formatting_datetime.second}S')

        embed = discord.Embed(
                title='Ticket Deleted',
                description=f"Ticket opened by: {self.ticket_creator.name}\n\n"
                            f"__User Info:__\n\n"
                            f"- **User ID:** {self.ticket_creator.id}\n"
                            f"- **User Mention:** {self.ticket_creator.mention}\n"
                            f"- **User Creation Date:** <t:{int(self.user_join_date.timestamp())}:f>\n"
                            f"- **Server Member Since:** <t:{int(self.guild_joined_date.timestamp())}:f>\n\n"
                            f"__Ticket Info:__\n\n"
                            f"- **Ticket Name:** {self.user_channel.name}\n"
                            f"- **Ticket Creation:** {self.ticket_created_time.timestamp()}\n"
                            f"- **Ticket Channel ID:** {self.user_channel.id}\n"
                            f"- **Ticket Mention:** {self.user_channel.mention}\n\n"
                            f"- **Ticket Closed by:** {interaction.user.mention}\n"
                            f"- **Ticket Closed At:** <t:{int(ticket_deleted_formatted_date_unix.timestamp())}:f>\n"
                            f"- **Ticket Active Duration:** {formatting}\n"
                            f"- **Ticket Opening Log:** "
                            f"https://discord.com/channels/{interaction.guild.id}/{self.logging_channel.id}/"
                            f"{self.logging_message.id}\n\n"
                            f"__Ticket Chat Info:__\n\n"
                            f"- **Total Messages Sent:** {total_msgs}\n"
                            f"- **Messages By Users:**\n " + "".join(f"\n> - {users}: {counter}"
                                                                     for users, counter in all_users_msgs.items()),
                color=discord.Color.brand_red()
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_author(icon_url=interaction.user.avatar, name=interaction.user.name,
                         url=f'https://discord.com/users/{interaction.user.id}')

        await self.logging_channel.send(embed=embed)
        clear_ticket_from_json(self.user_channel.id)


@bot.hybrid_command(name='ticket-setup')
async def ok(ctx, ticket_panel: discord.TextChannel):

    embed = discord.Embed(
        title=f"{ctx.guild.name}'s support system.",
        description=f"Please press the button below to contact staff.\n"
                    f"Avoid opening tickets for no reason.\n"
                    f"Do not false report somebody.\n"
                    f"Do not make false claims or pretend to be someone\n"
                    f"Not following them will result in punishment.",
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.set_footer(text='Not every rule is listed. Please use common sense.')

    view = CreateAChannelButton()

    try:
        ticket_panel_message = await ticket_panel.send(view=view, embed=embed)
    except discord.errors.Forbidden:
        await ctx.send(f"I don't have permission to send messages in: {ticket_panel.mention}. Please make sure i have"
                       f" **Send Messages** permission...", ephemeral=True)
    else:
        await ctx.send(f'Successfully placed ticket button in: [{ticket_panel.name}]'
                       f'(https://discord.com/channels/{ctx.guild.id}/{ticket_panel.id}/{ticket_panel_message.id})',
                       ephemeral=True)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    if str(message.channel.id) in ticket_data['opened_tickets']:
        add_members_to_json(message.channel.id, message.author.id)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print('Successfully logged in as:', bot.user.name)


bot.run(BOT_TOKEN)

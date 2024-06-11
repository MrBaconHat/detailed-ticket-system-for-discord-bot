import platform
import logging
import discord
import asyncio
import sys
import json
import time
import io
from typing import NoReturn
from ticket_setup import *
from datetime import datetime, timedelta
from discord.ext import commands


BOT_TOKEN = "paste your bot token here"
# ^  the token of your bot. it will be used to run the bot and add the commands to it. (REQUIRED)


class MyApp(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.moderation = True

        super().__init__(command_prefix='!', intents=intents)

    if reactivate_ticket_creation_buttons_on_startup:
        async def setup_hook(self) -> None:
            self.add_view(CreateAChannelButton())


bot = MyApp()


"""
___________________________________________________________NOTE_________________________________________________________
                                                                                                                       |
PLEASE USE THIS CODE WITH CAUTION. DO NOT ATTEMPT TO CHANGE ANYTHING UNLESS YOU KNOW AND UNDERSTAND THE SCRIPT PURPOSE.|
DO NOT PASTE ANY SCRIPT IN THIS ZONE. THE SCRIPT CAN BE MALICIOUS AND CAN RESULT IN DAMAGING THE BOT AND GIVING        |
UNAUTHORIZED ACCESS TO SOMEBODY OF YOUR BOT. DO NOT SHARE THIS SCRIPT WITH ANYONE IF YOU HAVE YOUR BOT TOKEN PLACED.   |
DOING THAT WILL RESULT IN GIVING BACKDOOR OF YOUR BOT TO SOMEBODY.                                                     |
                                                                                                                       |
CREATOR OF THIS SCRIPT(mr_baconhat, me) WILL NOT BE RESPONSIBLE IF YOU ENDED UP LEAKING SOMETHING IMPORTANT            |
SUCH AS YOUR BOT TOKEN.                                                                                                |
                                                                                                                       |
                                                   YOU HAVE BEEN WARNED.                                               | 
-----------------------------------------------------------------------------------------------------------------------|
                                                                                                                       |
IF YOU UNDERSTAND PYTHON YOU SHOULD CREATE .env(environment) FILE TO SECURE YOUR BOT TOKEN.                            |
BUT IF YOU DON'T UNDERSTAND PYTHON AT ALL YOU CAN CONTINUE USING SCRIPT LIKE THIS BUT BE SURE TO NOT SHARE THIS SCRIPT |
WITH ANYONE WITH YOUR BOT TOKEN PLACED INSIDE IT.                                                                      |
                                                                                                                       |
                                                   made by: mr_baconhat :]                                             |
                                                                                                                       |
IF YOU HAVE ANY QUESTIONS ABOUT THE SCRIPT OR WANT TO SUGGEST SOMETHING PLEASE CONTACT: mr_baconhat(discord)           |
_______________________________________________________________________________________________________________________|
                                                                                                                       |
PLEASE ONLY MAKE CHANGES BELOW IF YOU UNDERSTAND EVERYTHING.. MAKING CHANGES WHICH YOU DON'T UNDERSTAND CAN RESULT IN  |
SCRIPT RETURNING ERRORS.                                                                                               |
                                                                                                                       |
-----------------------------------------------------------------------------------------------------------------------|
"""

mandatory_configs = [
    ("ticket_manager_role_id", "Please put your manager role ID. It is a required input."),
    ("ticket_logging_channel_id", "Please paste a logging channel ID."),
    ("seconds_before_deleting_ticket", "Please enter a ticket closing duration in ticket_setup.py. "
                                       "Error: Missing \"seconds_before_deleting_ticket\""),
    ("ticket_limit_exceed_message", "Ticket limit exceed message shouldn't be empty. Please include a message"),
    ("message_on_deletion", "Ticket deletion message shouldn't be empty. Please include a message"),
    ("message_on_creation", "Ticket messages on creation shouldn't be empty. Please include a message"),
    ("message_on_creation_ephemeral", "Ticket messages on creation shouldn't be empty. Please include a message")
]

for roles in ticket_manager_role_id:
    if not roles.isdigit():
        sys.exit(f'Your manager role ID: {roles} is incorrect.. Please enter it correctly')

for config, error_message in mandatory_configs:
    value = globals().get(config)
    if not value:
        sys.exit(error_message)

try:
    seconds = int(seconds_before_deleting_ticket)
    assert seconds >= 3, ("Seconds before deleting ticket must be higher or equal to 3. "
                          "Please set it to 3 or higher in ticket_setup.py")
except (TypeError, ValueError):
    sys.exit("Error: time should be in integer.")
except AssertionError as error_message:
    sys.exit(error_message)

if any(color not in ["red", "blue", "green", "gray", "grey"]
       for color in [close_ticket_button_color, create_ticket_button_color, view_transcript_button_color]):
    sys.exit("Please only use the provided colors for the buttons because they are the supported ones.")

class Colors:
    BLACK = '\x1b[30m'
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    YELLOW = '\x1b[33m'
    BLUE = '\x1b[34m'
    MEGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    WHITE_RESET = '\033[0m'


discord_button_colors = {
        "green": discord.ButtonStyle.green,
        "red": discord.ButtonStyle.red,
        "gray": discord.ButtonStyle.gray,
        "grey": discord.ButtonStyle.grey,
        "blue": discord.ButtonStyle.blurple,
        "blurple": discord.ButtonStyle.blurple
    }

async def save_ticket_to_json(ticket_channel_id: str, user_id: int) -> NoReturn:
    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    ticket_data['opened_tickets'][str(ticket_channel_id)] = {
        "usersMessagesCount": {},
        'ticketAuthorId': user_id
    }

    with open('ticket_data.json', 'w') as write_file:
        json.dump(ticket_data, write_file, indent=4)

def getUnixAhead():
    return time.time() - -seconds_before_deleting_ticket

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

    opened_ticket = ticket_data['opened_tickets'][str_ticket_channel_id]['usersMessagesCount']

    if member_id not in opened_ticket:
        opened_ticket[member_id] = 1

    else:
        opened_ticket[member_id] += 1

    with open('ticket_data.json', 'w') as write_file:
        json.dump(ticket_data, write_file, indent=4)

def get_ticket_total_msgs(ticket_channel_id) -> int:
    ticket_channel_id = str(ticket_channel_id)
    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    return sum(ticket_data['opened_tickets'][ticket_channel_id]['usersMessagesCount'].values())


def get_all_ticket_users(ticket_channel_id) -> dict:
    ticket_channel_id = str(ticket_channel_id)

    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    user_all_msgs_count = ticket_data['opened_tickets'][ticket_channel_id]['usersMessagesCount']

    dictionary = {f"<@{users}>": counter for users, counter in user_all_msgs_count.items()} \
        if user_all_msgs_count.items() else {"No Messages were sent": 0}

    return dictionary


def variable_management(message, **kwargs):
    for key, value in kwargs.items():
        message = message.replace(f'{{{key}}}', str(value))
    return message


async def save_transcript(ticket_channel_object: discord.TextChannel):
    ticket_channel_id = str(ticket_channel_object.id)

    with open('ticket_data.json', 'r') as read_file:
        json_data = json.load(read_file)

    dictionary_1 = json_data['closed_tickets']

    opened_ticket = json_data['opened_tickets'][ticket_channel_id]
    closed_ticket = json_data['closed_tickets']

    all_messages = []

    async for msg in ticket_channel_object.history(limit=None, oldest_first=True):

        if msg.author.bot and not include_bot_messages_in_logs:
            print("in if condition")
            continue

        message_log = {
            "content": msg.content,
            "author": msg.author.id,
            "author_name": msg.author.name,
            "time": str(msg.created_at.strftime('%b %d(%a), %Y'))
        }

        all_messages.append(message_log)

    transfer_var = closed_ticket[f"{ticket_channel_id}"] = opened_ticket
    transfer_var["totalMessagesInLogs"] = len(all_messages)
    transfer_var["messagesLogs"] = all_messages

    json_data['closed_tickets'] = dictionary_1

    with open('ticket_data.json', 'w') as write_file:
        json.dump(json_data, write_file, indent=4)

def clear_ticket_transcripts(ticket_id):
    ticket_id = str(ticket_id)
    with open('ticket_data.json', 'r') as read_file:
        data_json = json.load(read_file)

    ticket_data = data_json['closed_tickets'][ticket_id]

    if ticket_data:

        ticket_data['messagesLogs'].clear()

        with open('ticket_data.json', 'w') as write_file:
            json.dump(data_json, write_file, indent=4)

def moveCloseDataToOpenData(ticket_id):
    ticket_id = str(ticket_id)
    with open('ticket_data.json', 'r') as read_file:
        data_json = json.load(read_file)

    closed_data = data_json['closed_tickets']
    opened_data = data_json['opened_tickets']

    if ticket_id in closed_data:
        ticket_logs = closed_data[ticket_id]
        ticket_logs.pop('messagesLogs')

        opened_data.update(**opened_data, **closed_data)
        del closed_data[ticket_id]

        with open('ticket_data.json', 'w') as update_file:
            json.dump(data_json, update_file, indent=4)

def checkUserTickets(user_id):
    if ticket_limit_per_user:
        with open('ticket_data.json', 'r') as read_file:
            json_data = json.load(read_file)

        opened_tickets_json = json_data['opened_tickets']

        total_user_tickets = 0

        for tickets in opened_tickets_json:
            if total_user_tickets == ticket_limit_per_user-1:
                raise ValueError(
                    variable_management(ticket_limit_exceed_message, ticket_user_limit=ticket_limit_per_user)
                )

            ticket_author = opened_tickets_json[tickets].get('ticketAuthorId')
            if ticket_author == user_id:
                total_user_tickets += 1

class CreateAChannelButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Create a ticket', style=discord_button_colors.get(create_ticket_button_color),
                       custom_id="createAChannel",
                       emoji=create_ticket_button_emoji)
    async def create_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if button:
            pass

        try:
            checkUserTickets(interaction.user.id)
        except ValueError as error_message:
            await interaction.response.send_message(content=error_message, ephemeral=True)
            return

        guild_category = bot.fetch_channel(int(ticket_category_id)) if ticket_category_id else None

        ticket_manager_role = [
            interaction.guild.get_role(int(role_id)) for role_id in ticket_manager_role_id
            if interaction.guild.get_role(int(role_id))
        ]

        if not ticket_manager_role:
            sys.exit("Manager IDs are incorrect... Please enter correct Manager IDs to continue\n\n\n\n")

        logging_channel = bot.get_channel(int(ticket_logging_channel_id))
        if not logging_channel:
            await interaction.response.send_message(f"Incorrect ticket logging ID: **{ticket_logging_channel_id}** "
                                                    f"Provided in: \"ticket_setup.py\". Please paste correct ID.",
                                                    ephemeral=True)
            return

        # Preparing to fit in roles and ticket permissions

        bot_role = next((role for role in interaction.guild.get_member(bot.user.id).roles if role.is_bot_managed()),
                        None)

        guild_everyone_role: discord.Role = interaction.guild.get_role(interaction.guild.id)

        manager_role_overwrite = discord.PermissionOverwrite.from_pair(
            discord.Permissions(117824),
            discord.Permissions.none()
        )

        bot_overwrite = discord.PermissionOverwrite.from_pair(
            discord.Permissions(2147609680),
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
            interaction.user: user_overwrite,
            guild_everyone_role: everyone_role_overwrite,
            bot_role: bot_overwrite,
        }
        for role in ticket_manager_role:
            guild_permission_format[role] = manager_role_overwrite

        try:
            created_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}",
                                                                          category=guild_category,
                                                                          topic=f'This is a ticket of: '
                                                                                f'<@{interaction.user.id}>',
                                                                          overwrites=guild_permission_format)
        except discord.errors.Forbidden:
            await interaction.response.send_message("I dont have permission to create channel.", ephemeral=True)
            return

        await save_ticket_to_json(str(created_channel.id), interaction.user.id)

        start_time = time.time()

        ephemeral_message_on_creation = variable_management(message=message_on_creation_ephemeral,
                                                            server_name=interaction.guild.name,
                                                            user_id=interaction.user.id,
                                                            user_name=interaction.user.name,
                                                            user_mention=interaction.user.mention,
                                                            ticket_id=created_channel.id,
                                                            ticket_name=created_channel.name,
                                                            ticket_mention=created_channel.mention
                                                            )
        await interaction.response.send_message(ephemeral_message_on_creation,
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
        try:
            logging_message = await logging_channel.send(embed=embed)
        except discord.errors.Forbidden:
            await interaction.response.send_message("I dont have permission to send messages in logging channel.")
            return

        view = CloseTicketButton(channel_object=created_channel, ticket_author_object=interaction.user,
                                 guild_object=interaction.guild, ticket_category_object=guild_category,
                                 ticket_manager_role_object=ticket_manager_role, start_time=start_time,
                                 ticket_creation=ticket_created_formatted_date, logging_message_object=logging_message,
                                 guild_joined_date=user_guild_creation_formatted_date,
                                 user_join_date=user_creation_formatted_date, logging_channel=logging_channel)

        modified_message_on_creation = variable_management(
            message=message_on_creation, server_name=interaction.guild.name,
            user_id=interaction.user.id, user_name=interaction.user.name,
            user_mention=interaction.user.mention,
            ticket_id=created_channel.id,
            ticket_name=created_channel.name,
            ticket_mention=created_channel.mention,
            manager_role="".join(f"<@&{role.id}>, " for role in ticket_manager_role))

        await created_channel.send(modified_message_on_creation,
                                   view=view)


class CloseTicketButton(discord.ui.View):

    def __init__(self, channel_object, ticket_author_object, guild_object, ticket_category_object,
                 ticket_manager_role_object, start_time, ticket_creation, logging_message_object,
                 guild_joined_date, user_join_date, logging_channel):
        super().__init__(timeout=None)

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

    @discord.ui.button(label='Close ticket', style=discord_button_colors.get(close_ticket_button_color),
                       emoji=close_ticket_button_emoji)
    async def close(self, interaction: discord.Interaction, button: discord.ui.button):
        if button:
            pass

        modified_message_on_deletion = variable_management(
            message=message_on_deletion, server_name=interaction.guild.name,
            user_id=str(interaction.user.id), user_name=interaction.user.name,
            user_mention=interaction.user.mention,
            ticket_id=self.user_channel.id,
            ticket_name=self.user_channel.name,
            ticket_mention=self.user_channel.mention,
            manager_role="".join(f"<@&{role.id}>, " for role in self.ticket_manager_role),
            seconds=seconds_before_deleting_ticket,
            seconds_countdown=f"<t:{int(getUnixAhead())}:R>"
        )

        await interaction.response.send_message(modified_message_on_deletion)
        await asyncio.sleep(int(seconds_before_deleting_ticket))
        try:
            await save_transcript(self.user_channel)
            await self.user_channel.delete()
        except discord.errors.Forbidden:
            clear_ticket_transcripts(self.user_channel.id)
            moveCloseDataToOpenData(self.user_channel.id)
            await self.user_channel.send("I dont have permission to delete channels.")

        total_msgs = get_ticket_total_msgs(self.user_channel.id)
        all_users_msgs = get_all_ticket_users(self.user_channel.id) or {"No Messages were sent": 0}

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
                        f"- **Ticket Creation:** {int(self.ticket_created_time.timestamp())}\n"
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

        view = RequestMessagesLogs(self.user_channel)

        try:
            await self.logging_channel.send(embed=embed, view=view)
        except discord.errors.Forbidden:
            await interaction.response.send_message("I dont have permission to send messages in logging channel.",
                                                    ephemeral=True)
            return
        if dm_transcript_to_ticket_author:
            await self.ticket_creator.send(view=view)
        clear_ticket_from_json(self.user_channel.id)


class RequestMessagesLogs(discord.ui.View):

    def __init__(self, ticket_channel_object):
        super().__init__(timeout=None)
        self.ticket_object = ticket_channel_object

    @discord.ui.button(label='View Transcript File', style=discord_button_colors.get(view_transcript_button_color),
                       emoji=view_transcript_button_emoji)
    async def request(self, interaction: discord.Interaction, button: discord.ui.button):
        if button:
            pass

        with open('ticket_data.json', 'r') as read_file:
            json_data = json.load(read_file)

        t_content_list = []
        all_messages = []
        try:
            all_messages = json_data['closed_tickets'][f'{self.ticket_object.id}']['messagesLogs']
        except KeyError as missing_channel:
            if missing_channel == f'{self.ticket_object.id}':
                pass

        if not all_messages:
            t_content_list.append('No Messages were sent: 0')
        else:
            t_content_list.extend(
                variable_management(
                    message=ticket_transcript_display_on_file,
                    user_id=stats.get("author"),
                    user_name=stats.get("author_name"),
                    content=stats.get("content"),
                    sent_at=stats.get("sent_at"),
                    ticket_id=self.ticket_object.id, ticket_name=self.ticket_object.name,
                    ticket_mention=self.ticket_object.mention, user_mention=f'<@{stats.get("author")}>'
                )for stats in all_messages
            )

        buffer = io.BytesIO()
        messages = ''.join(t_content_list)
        buffer.write(messages.encode('utf-8'))
        buffer.seek(0)
        file = discord.File(buffer, filename='transcript.ruby')
        await interaction.response.send_message(file=file, ephemeral=True)


@bot.hybrid_command(name='ticket-setup')
async def ticket(ctx, ticket_panel: discord.TextChannel):
    modified_embed_title = variable_management(message=title_on_button_embed, server_name=ctx.guild.name)
    modified_embed_description = variable_management(message=description_on_button_embed, server_name=ctx.guild.name,
                                                     server_id=ctx.guild.id)
    modified_embed_footer = variable_management(message=footer_on_button_embed, server_name=ctx.guild.name,
                                                server_id=ctx.guild.id)

    embed = discord.Embed(
        title=modified_embed_title,
        description=modified_embed_description,
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.set_footer(text=modified_embed_footer)

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


def getPythonTimingFormat():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

@bot.event
async def on_ready():
    print("Starting...")
    await bot.tree.sync()
    print(f'{Colors.RED}About Bot:{Colors.WHITE_RESET}\n'
          f'\t{Colors.YELLOW}Successfully logged in as: {Colors.WHITE_RESET}{bot.user.name} ({bot.user.id})\n'
          f'\t{Colors.YELLOW}Bot User: {Colors.WHITE_RESET}{bot.user.name}\n'
          f'\t{Colors.YELLOW}Bot ID: {Colors.WHITE_RESET}{bot.user.id}\n'
          f'\t{Colors.YELLOW}Bot Started At: {Colors.WHITE_RESET}{getPythonTimingFormat()}\n'
          f'{Colors.RED}{"-" * 60}{Colors.WHITE_RESET}\n'
          f'{Colors.RED}About Discord Module:{Colors.WHITE_RESET}\n'
          f'\t{Colors.CYAN}Discord Module Version: {Colors.WHITE_RESET}{discord.__version__}\n'
          f'\t{Colors.CYAN}Latency: {Colors.WHITE_RESET}{bot.latency * 1000:.2f} ms\n'
          f'\t{Colors.CYAN}Registered Commands: {Colors.WHITE_RESET}{len(bot.tree.get_commands())}\n'
          f'{Colors.RED}{"-" * 60}{Colors.WHITE_RESET}\n'
          f'{Colors.RED}About System:{Colors.WHITE_RESET}\n'
          f'\t{Colors.GREEN}Python Version: {Colors.WHITE_RESET}{platform.python_version()}\n'
          f'\t{Colors.GREEN}Operating System: {Colors.WHITE_RESET}{platform.system()} {platform.release()}\n')

    logging.warning("Now logging..\n")


@bot.event
async def on_message(message):
    if message.author.bot and not include_bot_ticket_messages_count:
        return

    with open('ticket_data.json', 'r') as read_file:
        ticket_data = json.load(read_file)

    if str(message.channel.id) in ticket_data['opened_tickets']:
        add_members_to_json(message.channel.id, message.author.id)


@bot.event
async def on_audit_log_entry_create(entry):

    if str(entry.action).lower() != "AuditLogAction.channel_delete".lower():
        return
    if entry.user_id == bot.user.id:
        return

    with open('ticket_data.json', 'r') as read_file:
        json_data = json.load(read_file)

    channel_id = entry.target.id
    opened_tickets = json_data['opened_tickets']

    if str(channel_id) in opened_tickets:
        del opened_tickets[str(channel_id)]

        with open('ticket_data.json', 'w') as update_file:
            json.dump(json_data, update_file, indent=4)

try:
    bot.run(BOT_TOKEN)

except discord.errors.LoginFailure:
    timing = getPythonTimingFormat()
    sys.exit(f"\n[{timing}] [ERROR   ] Could not start up: You've provided the incorrect bot token...\n\n"
             f"Incorrect bot token: \"{BOT_TOKEN}\"")


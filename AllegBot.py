import discord
import logging
import requests
from discord.ext import tasks, commands
import time
from key import DiscordToken, guild_id, steam_api

#TODO
#Future:
#Dropdown
#Beautify

intents = discord.Intents.default()
intents.message_content = True

# stockpiles bot
# Designate a channel as a stockpile channel
# 

TEST_GUILD = discord.Object(id = guild_id)
ALLEG_GUILD = discord.Object(id = 232218137330712577)

class DiscordClient(discord.Client):
    
    def __init__(self, *, intents: discord.Intents, **options: any) -> None:
        super().__init__(intents=intents, **options)
        self.tree = discord.app_commands.CommandTree(self)
        self.channels = 1146976402512564294, 680507105723154434
        self.last_player_num = -1
        self.num_checks_since_last_post = 0
    
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)
        self.tree.copy_global_to(guild=ALLEG_GUILD)
        await self.tree.sync(guild=ALLEG_GUILD)
    

handler = logging.FileHandler(filename="student-test.log", encoding='utf-8', mode='w')       
intents = discord.Intents.default()
client = DiscordClient(intents = intents)


def get_player_numbers():
    player_request = requests.get(url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid=700480?key={steam_api}",)
    player_json = player_request.json()
    print(player_json)
    return player_json["response"]["player_count"]

#helper function to log time, returns a string
def get_time(UTC: bool = False) -> str:
    if UTC:
        time_struct = time.gmtime()
    else:
        time_struct = time.localtime()
    
    return(time.strftime("UTC %z (%Y/%m/%d-%H:%M:%S):", time_struct))

@tasks.loop(minutes=2)
async def send_players():
    player_num = get_player_numbers()
    if player_num != client.last_player_num:
        client.last_player_num = player_num
        for channel in client.channels:
            if channel == 680507105723154434:
                #dev - skip the alleg server
                continue
            try:
                print(f"{get_time()} sending in {channel}: #{player_num}, times since last check: {client.num_checks_since_last_post}")
                await client.get_channel(channel).send(f"""Current Players: {player_num}\n(Checks since last post: {client.num_checks_since_last_post})""")
            except:
                print(f"{get_time()} Not a valid channel {channel}")
        client.num_checks_since_last_post = 0
    else:
        print(f"{get_time()} no change in player numbers")
        client.num_checks_since_last_post += 1


@client.event
async def on_ready():
    send_players.start()
    print("ready")

client.run(DiscordToken, log_handler=handler)

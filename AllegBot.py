import discord
import logging
import requests
from discord.ext import tasks, commands
from sys import stdout
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
        self.last_player_num = 0
    
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

@tasks.loop(minutes=2)
async def send_players():
    player_num = get_player_numbers()
    if player_num != client.last_player_num:
        client.last_player_num = player_num
        for channel in client.channels:
            try:
                print(f"sending in {channel}")
                await client.get_channel(channel).send(f"""Current Players: {player_num}""")
            except:
                print(f"Not a valid channel {channel}")

    else:
        print("no change in player numbers")


@client.event
async def on_ready():
    send_players.start()
    print("ready")

client.run(DiscordToken, log_handler=handler)

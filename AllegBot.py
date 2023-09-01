import discord
import logging
import requests
from sys import stdout
from key import DiscordToken, guild_id

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
    
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)
        self.tree.copy_global_to(guild=ALLEG_GUILD)
        await self.tree.sync(guild=ALLEG_GUILD)
    

handler = logging.FileHandler(filename="student-test.log", encoding='utf-8', mode='w')       
intents = discord.Intents.default()
intents.message_content = True
client = DiscordClient(intents = intents)

def get_player_numbers():
        player_request = requests.get(url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid=700480")
        player_json = player_request.json()
        print(player_json)
        return player_json["response"]["player_count"]

if __name__ == "__main__":
    print(get_player_numbers())

    #client.run(DiscordToken, log_handler=handler)

import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog, Greedy, CheckFailure, command, has_permissions, bot_has_permissions
import json
import requests

from metno_locationforecast import Place, Forecast

import os
from dotenv import load_dotenv
load_dotenv("keys.env")
weather_key = os.getenv("OPENWEATHER")

class weather(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "weather", brief = "hey what's the weather?")
    @cooldown(5, 60, BucketType.user)
    async def check_weather(self, ctx, *, input = "tromsø"):
        r = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={input}&limit=1&appid={weather_key}")
        request = json.loads(r.content)
        realoutput = request[0]
        lat = realoutput["lat"]
        lon = realoutput["lon"]

        place = Place(input, lat, lon)

        my_forecast = Forecast(place, "https://github.com/JustTemmie/space-bot, contact me on discord: https://discordapp.com/users/368423564229083137 or snassssssss@gmail.com")
        my_forecast.update()
        
        forecast = str(my_forecast.data.intervals[0]).split("\n")
    
        embed = Embed(title = f"{forecast[0]} in {input}", description = "", color = 0x00ff00)
        
        for a in forecast:
            x = a.split()
            if x[0] != "Forecast":
                embed.add_field(name = x[0].replace("_", " "), value = x[1], inline = False)
            
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(weather(bot))
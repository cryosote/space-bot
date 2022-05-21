from urllib import response
import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


from libraries.economyLib import *


class ecogeneration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="daily", brief="get your daily beaver coins here!")
    @cooldown(3, 15, BucketType.user)
    async def daily_command(self, ctx):
        await open_account(ctx.author)

        bank = await get_bank_data()
        daily_info = bank[str(ctx.author.id)]["daily"]

        if daily_info["day"] == (datetime.utcnow() - datetime(1970, 1, 1)).days:
            return await ctx.send("you already got your daily, come back tomorrow")

        streak = ""
        if (
            daily_info["streak"] != 0
            and daily_info["day"] < (datetime.utcnow() - datetime(1970, 1, 1)).days - 1
        ):
            if bank[str(ctx.author.id)]["inventory"]["insurance"] >= 1:
                await ctx.send(
                    f"you had a streak of {daily_info['streak']}\n\nbut you own {bank[str(ctx.author.id)]['inventory']['insurance']} insurance totems\ndo you wish to spend a totem in order to mentain your streak or do you want to restart from 0?"
                )
                response = await self.bot.wait_for(
                    "message", check=lambda m: m.author == ctx.author, timeout=45
                )

                if response.content.lower() in confirmations:
                    streak += f"**you used a totem, you have a {daily_info['streak']} day streak!**"
                    bank[str(ctx.author.id)]["inventory"]["insurance"] -= 1

                else:
                    streak += f"**you lost your streak of {daily_info['streak']} days :(**"
                    daily_info["streak"] = 0
            else:
                streak += f"**you lost your streak of {daily_info['streak']} days :(**"
                daily_info["streak"] = 0

        else:
            daily_info["streak"] += 1
            streak += f"**{daily_info['streak']} day streak!**"

        payout = random.randint(25, 75) + round(random.randrange(5, 10) * daily_info["streak"])
        if payout >= 500:
            payout = 500

        # skills
        if bank[str(ctx.author.id)]["dam"]["level"] >= 3:
            payout *= 2
            streak += "\n**you got double coins for having a lvl 3+ dam**"
        
        
        bank[str(ctx.author.id)]["wallet"] += payout
        daily_info["day"] = (datetime.utcnow() - datetime(1970, 1, 1)).days
        bank[str(ctx.author.id)]["daily"] = daily_info
        with open("data/bank.json", "w") as f:
            json.dump(bank, f)

        await ctx.send(f"you got +{payout} <:beaverCoin:968588341291397151>!\n{streak}")
        
        
        
    @commands.command(
        name="scavenge",
        aliases=["search", "find", "loot"],
        brief="go scavenge for some l ö g <:log:970325254461329438>",
    )
    @cooldown(1, 300, BucketType.user)
    async def scavenge_logs(self, ctx):
        await open_account(ctx.author)
        data = await get_bank_data()
        strength = 5#data[str(ctx.author.id)]["stats"]["strength"]
        
        try:            
            temporal = time.time() - data[str(ctx.author.id)]["scavenge_cooldown"] - 300
            payout = (strength * 0.0004 + 0.008) * temporal**0.8 + random.randrange(8, 11) + random.uniform(0.3, 0.8) * strength
        except:
            temporal = time.time() - data[str(ctx.author.id)]["scavenge_cooldown"]
            payout = (0.008 * temporal**0.8 + random.randrange(8, 11)) / 300 * temporal


        if payout >= 20000:
            payout = 20000

        # skills
        if data[str(ctx.author.id)]["dam"]["level"] >= 2:
            payout *= 1.25
        
        if data[str(ctx.author.id)]["dam"]["level"] >= 3:
            payout *= 1.25
        
        
        payout = round(payout)
        
        data = await get_bank_data()
        data[str(ctx.author.id)]["inventory"]["logs"] += payout
        data[str(ctx.author.id)]["scavenge_cooldown"] = time.time()

        with open("data/bank.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"you scavenged for <:log:970325254461329438>, and you found {payout} of them!")

        
def setup(bot):
    bot.add_cog(ecogeneration(bot))

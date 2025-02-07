from discord import Member
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import random
import libraries.standardLib as SL
from datetime import datetime
from math import floor


class shipcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ship", brief="Ship two users :)")
    @cooldown(2, 10, BucketType.user)
    async def ship_command(self, ctx, person1: Member, person2: Member = "author"):
        if person2 == "author":
            person2 = person1
            person1 = ctx.author

        if person1 == person2:
            await ctx.send("Please don't give me two of the same user")
            return

        random.seed(person1.id + person2.id + floor((datetime.utcnow() - datetime(1970, 1, 1)).days / 20))
        result = random.randint(0, 100)
        
        messageStr = ""

        if result <= 9:
            messageStr = random.choice([
                (f"sorry but.. the ship between {person1.display_name} and {person2.display_name} is as likely as a mango tree growing on a glacier, giving it a {result} / 100"),
                (f"{person1.display_name} and {person2.display_name} should just give up, it's not happening, {result} / 100")
            ])
        elif result <= 19:
            messageStr = random.choice([
                (f"the ship between {person1.display_name} and {person2.display_name} doesn't seem particularly likely, scoring a {result} / 100"),
            ])
        elif result <= 29:
            messageStr = random.choice([
                (f"{person1.display_name} and {person2.display_name} is not going to be a thing, with them scoring {result} / 100 i can't see how that would ever work"),
            ])
        elif result <= 39:
            messageStr = random.choice([
                (f"{person1.display_name} and {person2.display_name} are certainly not made for eachother, and i would not expect them to ever become a serious thing, especially not with a score of {result} / 100"),
            ])
        elif result <= 49:
            messageStr = random.choice([
                (f"a ship between {person1.display_name} and {person2.display_name} seems like it *might* possible... {result} / 100"),
            ])
        elif result <= 59:
            messageStr = random.choice([
                (f"a relationship among~~us~~ {person1.display_name} and {person2.display_name} seems very plausible, above average even, scoring a {result} / 100"),
            ])
        elif result < 69:
            messageStr = random.choice([
                (f"i give a ship between {person1.display_name} and {person2.display_name} a solid {result} / 100"),
            ])
        elif result == 69:
            messageStr = random.choice([
                (f"{person1.display_name} and {person2.display_name} are practically made for eachother, i mean they literally scored a {result} / 100"),
            ])
        elif result <= 79:
            messageStr = random.choice([
                (f"{person1.display_name} and {person2.display_name} seem to have a great future ahead of them, with a score of {result} / 100"),
            ])
        elif result <= 89:
            messageStr = random.choice([
                (f"the love between {person1.display_name} and {person2.display_name} burns as hot as the sun, scoring a {result} / 100")
                (f"the love of {person1.display_name} and {person2.display_name} is as strong as the love between a cat and a cardboard box, scoring a {result} / 100"),
            ])
        elif result <= 99:
            messageStr = random.choice([
                (f"the bond between {person1.display_name} and {person2.display_name} seems so strong, i'm rating it a {result} / 100"),
            ])
        elif result == 100:
            messageStr = random.choice([
                (f"wow.. {person1.display_name} and {person2.display_name} seem to be perfect for eachother getting an incredible {result} / 100 on my test"),
            ])
        else:
            messageStr = ("uhm... this shouldn't be possible but you somehow broke the command, uhm... sorry lmao")

        random.seed()
        
        await ctx.send(await SL.removeat(messageStr))

async def setup(bot):
    await bot.add_cog(shipcog(bot))

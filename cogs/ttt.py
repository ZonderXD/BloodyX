from discord.ext import commands
import discord
import asyncio
import datetime
from discord import Embed
import random
currentlyplaying = [1]
currentservers = [719939324686237737]
current_boxes = {}
filled_boxes = {}
servercurrentreactions = {}
editable_message = {}
currentturn = {}
def get_colour():
    return random.randint(0, 0xffffff)
class tictactoe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ttt(self, ctx, opponent : discord.Member):
        if ctx.author.bot is True:
            pass
        else:
            if ctx.guild.id in currentservers:
                await ctx.send("Извините, но только одна игра в крестики-нолики может быть воспроизведена на сервере.")
            elif opponent.id == self.bot.user.id:
                await ctx.send(f"{opponent.mention} это победитель. Ты даже не заметил.")
            elif opponent.bot is True:
                await ctx.send("Вы не можете играть с ботом.")
            else:
                def checkacceptance(message):
                    return message.author.id == opponent.id and  message.content == "tttaccept"
                try:
                    await ctx.send(f'{opponent.mention} напишите `tttaccept` чтобы принять вызов {ctx.author.mention}')
                    await self.bot.wait_for('message', timeout = 30, check = checkacceptance)
                    currentservers.append(ctx.guild.id)
                    await ctx.send(f"Игра в крестики-нолики началась {ctx.author.mention} против {opponent.mention}")
                    current_boxes[ctx.guild.id] = {1 : ":white_large_square:", 2 : ":white_large_square:", 3 : ":white_large_square:", 4 : ":white_large_square:", 5 : ":white_large_square:", 6 : ":white_large_square:", 7 : ":white_large_square:", 8 : ":white_large_square:", 9 : ":white_large_square:"}
                    current_msg = ''
                    count = 1
                    for box in current_boxes[ctx.guild.id].keys():
                        if count != 1:
                            if count%3 == 0:
                                current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                count+=1
                            else:
                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                count+=1
                        else:
                            current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                            count+=1
                    filled_boxes[ctx.guild.id] = {}
                    x = random.choice(seq = [ctx.author, opponent])
                    xlist = [ctx.author, opponent]
                    index = xlist.index(x)
                    if index == 1:
                        y = xlist[0]
                    elif index == 0:
                        y = xlist[1]
                    print(index)
                    initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь\nВы Случайно Получили X.")
                    message = await ctx.send(embed=initialembed)
                    currentturn[ctx.guild.id] = x.id
                    editable_message[ctx.guild.id] = message.id
                    await message.add_reaction("↖")
                    await message.add_reaction("⬆️")
                    await message.add_reaction("↗️")
                    await message.add_reaction("⬅️")
                    await message.add_reaction("⏺️")
                    await message.add_reaction("➡️")
                    await message.add_reaction("↙️")
                    await message.add_reaction("⬇️")
                    await message.add_reaction("↘️")
                    turn = x
                    servercurrentreactions[message.id] = []
                    def checkx(reaction, user):
                        return user.id == x.id and reaction.message.id == message.id and str(reaction.emoji) not in servercurrentreactions[reaction.message.id]
                    def checky(reaction, user):
                        return user.id == y.id and reaction.message.id == message.id and str(reaction.emoji) not in servercurrentreactions[reaction.message.id]
                    for variable in range(1,10):
                        if turn == x:
                            try:
                                reactionres = await self.bot.wait_for("reaction_add", check = checkx, timeout = 30)
                                servercurrentreactions[message.id].append(str(reactionres[0]))
                                clearemj = str(reactionres[0])
                                await message.clear_reaction(clearemj)





                                if str(reactionres[0]) == "↖":
                                    if 1 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][1] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _7 = current_boxes[ctx.guild.id][7]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        if (_1 == _2 == _3) or (_1 == _4 == _7) or (_1 == _5 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed = initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {1 : "❌"}
                                            turn = y






                                elif str(reactionres[0]) == "⬆️":
                                    if 2 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][2] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        if (_1 == _2 == _3) or (_2 == _5 == _8):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)

                                            filled_boxes[ctx.guild.id] = {2 : "❌"}
                                            turn = y




                                elif str(reactionres[0]) == "↗️":
                                    if 3 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][3] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _7 = current_boxes[ctx.guild.id][7]
                                        if (_1 == _2 == _3) or (_3 == _5 == _7) or (_3 == _6 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {3 : "❌"}
                                            turn = y





                                elif str(reactionres[0]) == "⬅️":
                                    if 4 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][4] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]
                                        if (_1 == _4 == _7) or (_4 == _5 == _6):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {4 : "❌"}
                                            turn = y


                            
                                elif str(reactionres[0]) == "⏺️":
                                    if 5 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][5] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_1 == _5 == _9) or (_2 == _5 == _8) or (_3 == _5 == _7) or (_4 == _5 == _6):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {5 : "❌"}
                                            turn = y



                                elif str(reactionres[0]) == "➡️":
                                    if 6 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][6] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_3 == _6 == _9) or (_4 == _5 == _6):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {6 : "❌"}
                                            turn = y



                                elif str(reactionres[0]) == "↙️":
                                    if 7 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][7] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_1 == _4 == _7) or (_7 == _5 == _3) or (_7 == _8 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {7 : "❌"}
                                            turn = y




                                elif str(reactionres[0]) == "⬇️":
                                    if 8 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][8] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_2 == _5 == _8) or (_7 == _8 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {8 : "❌"}
                                            turn = y





                                elif str(reactionres[0]) == "↘️":
                                    if 9 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][9] = "❌"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_3 == _6 == _9) or (_7 == _8 == _9) or (_1 == _5 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {x.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{y.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {9 : "❌"}
                                            turn = y
                            except asyncio.TimeoutError:
                                await ctx.send(f"{x.mention} Не сумел использовать свой ход, {y.mention} является Победителем!")
                                currentservers.remove(ctx.guild.id)
                                break
                        elif turn == y:
                            try:
                                reactionres = await self.bot.wait_for("reaction_add", check = checky, timeout = 30)
                                servercurrentreactions[message.id].append(str(reactionres[0]))
                                clearemj = str(reactionres[0])
                                await message.clear_reaction(clearemj)





                                if str(reactionres[0]) == "↖":
                                    if 1 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][1] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _7 = current_boxes[ctx.guild.id][7]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        if (_1 == _2 == _3) or (_1 == _4 == _7) or (_1 == _5 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed = initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {1 : "⭕"}
                                            turn = x






                                elif str(reactionres[0]) == "⬆️":
                                    if 2 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][2] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        if (_1 == _2 == _3) or (_2 == _5 == _8):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                                
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {2 : "⭕"}
                                            turn = x




                                elif str(reactionres[0]) == "↗️":
                                    if 3 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][3] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _7 = current_boxes[ctx.guild.id][7]
                                        if (_1 == _2 == _3) or (_3 == _5 == _7) or (_3 == _6 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {3 : "⭕"}
                                            turn = x





                                elif str(reactionres[0]) == "⬅️":
                                    if 4 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][4] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]
                                        if (_1 == _4 == _7) or (_4 == _5 == _6):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {4 : "⭕"}
                                            turn = x


                            
                                elif str(reactionres[0]) == "⏺️":
                                    if 5 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][5] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_1 == _5 == _9) or (_2 == _5 == _8) or (_3 == _5 == _7) or (_4 == _5 == _6):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {5 : "⭕"}
                                            turn = x



                                elif str(reactionres[0]) == "➡️":
                                    if 6 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][6] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_3 == _6 == _9) or (_4 == _5 == _6):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {6 : "⭕"}
                                            turn = x



                                elif str(reactionres[0]) == "↙️":
                                    if 7 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][7] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_1 == _4 == _7) or (_7 == _5 == _3) or (_7 == _8 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {7 : "⭕"}
                                            turn = x




                                elif str(reactionres[0]) == "⬇️":
                                    if 8 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][8] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_2 == _5 == _8) or (_7 == _8 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {8 : "⭕"}
                                            turn = x





                                elif str(reactionres[0]) == "↘️":
                                    if 9 not in filled_boxes[ctx.guild.id]:
                                        current_boxes[ctx.guild.id][9] = "⭕"
                                        current_msg = ''
                                        count = 1
                                        for box in current_boxes[ctx.guild.id].keys():
                                            if count != 1:
                                                if count%3 == 0:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}\n"
                                                    count+=1
                                                else:
                                                    current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                    count+=1
                                            else:
                                                current_msg+= f"{current_boxes[ctx.guild.id][box]}"
                                                count+=1
                                        _1 = current_boxes[ctx.guild.id][1]
                                        _5 = current_boxes[ctx.guild.id][5]
                                        _9 = current_boxes[ctx.guild.id][9]
                                        _2 = current_boxes[ctx.guild.id][2]
                                        _8 = current_boxes[ctx.guild.id][8]
                                        _3 = current_boxes[ctx.guild.id][3]
                                        _4 = current_boxes[ctx.guild.id][4]
                                        _6 = current_boxes[ctx.guild.id][6]
                                        _7 = current_boxes[ctx.guild.id][7]


                                        if (_3 == _6 == _9) or (_7 == _8 == _9) or (_1 == _5 == _9):
                                            initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nПобедитель : {y.mention}")
                                            await message.edit(embed=initialembed)
                                            currentservers.remove(ctx.guild.id)
                                            break
                                        else:
                                            if variable != 9:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\n{x.mention} ваша очередь")
                                                await message.edit(embed=initialembed)
                                            else:
                                                initialembed = discord.Embed(title = "Крестики Нолики", colour = get_colour(), description = f"{current_msg}\nМатч проходит вничью.")
                                                await message.edit(embed=initialembed)
                                                currentservers.remove(ctx.guild.id)
                                            filled_boxes[ctx.guild.id] = {9 : "⭕"}
                                            turn = x
                            except asyncio.TimeoutError:
                                await ctx.send(f"{y.mention} Не сумел использовать свой ход, {x.mention} является Победителем.")
                                currentservers.remove(ctx.guild.id)
                                break
                except asyncio.TimeoutError:
                    await ctx.send(f"{opponent.mention} Не принял ваш вызов.")

            


        
def setup(bot):
    bot.add_cog(tictactoe(bot))

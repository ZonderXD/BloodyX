    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            pass
        # вероятность срабатывания бота, тут на свой вкус и цвет как грся
        elif random.randint(0, 100) > 50:
            msgs = ["дарова", "ты далбаёб"]
            channel = ctx.channel
            # и так далее, фантазируйте как отвечать
            words_list = ['а ты ведешь себя как дурак', 'пошел ты балбес', 'а я твою кошку глажу!', 'привет бот']
            async for msg in channel.history(limit=(random.randint(10, 50))):
                if msg.author == self.bot.user:
                    pass
                else:
                    msgs.append(msg)
             if len(msgs) == 0:
                # костыль если не найдет сообщения в текстовом канале
                msgs.append('Слыш')
             msg = random.choice(msgs)
            # симулируем, что бот такой человечный и это он САМ печатает!!
            async with channel.typing():
                author = msg.author.mention
                await asyncio.sleep(random.randint(5, 15))
                await ctx.channel.send(f'{author} {random.choice(words_list)}')

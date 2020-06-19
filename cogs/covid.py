import requests
from bs4 import BeautifulSoup
from utils.codes import states

class covid(commands.Cog):

    def init(self, bot):
        self.bot = bot


    @commands.command(aliases=['коронка'])
    async def covid(self, ctx, state = ''):
        state = state.lower()
        rector = state
        if state in states:
                state = states[state]
        Corona = f'https://coronavirusstat.ru/country/{state}/#operational-data'
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        full_page = requests.get(Corona, headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("div", {"class": "h2"})
        hz = soup.find("h6",{"class":"text-muted"})
        hyra = soup.find("span",{"class":"font-weight-bold text-primary"})
        fixic = soup.find("span",{"class":"font-weight-bold text-success"})
        hyc = soup.find("span",{"class":"font-weight-bold text-danger"})
        heads = []
        for i in convert:
            heads.append(i.string)
        emb = discord.Embed(title=f"Короновирус - {rector} \n{hz.string}", color=16753920)
        emb.add_field(name="Случаев заболевания: ", value=heads[0], inline=False)
        emb.add_field(name="Заражено: ", value=heads[1], inline=True)
        emb.add_field(name="Заражено за сутки: ", value=hyra.string, inline=True)
        emb.add_field(name="Выздоровело: ", value=heads[2], inline=True)
        emb.add_field(name="Выздоровело за сутки: ", value=fixic.string, inline=True)
        emb.add_field(name="Умерло: ", value=heads[3], inline=True)
        emb.add_field(name="Умерло за сутки: ", value=hyc.string, inline=True)
        emb.set_thumbnail(url=
'https://pngimg.com/uploads/biohazard/biohazard_PNG85.png')
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(covid(bot))

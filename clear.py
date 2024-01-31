import nextcord
from nextcord.ext import commands



#clear chat 
def setup(bot):
   @bot.slash_command(name="clearmsg", description="sterge mesaje")
   @commands.has_permissions(manage_messages=True)  # Asigură-te că doar utilizatorii cu permisiunea de a gestiona mesajele pot folosi această comandă
   async def clear(ctx, num: int):
    if num < 1:
        await ctx.send("Te rog să specifici un număr valid de mesaje pentru a fi șterse.")
        return

    deleted = await ctx.channel.purge(limit=num)
    await ctx.send(f'Șterse {len(deleted)} mesaje.', delete_after=5)  # Mesajul de confirmare se va șterge automat după 5 secunde
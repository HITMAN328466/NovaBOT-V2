import nextcord
from nextcord.ext import commands
from skins import skinuri_samp

# Presupunând că ai variabila skinuri_samp definită undeva sau o importi

async def cauta_dupa_nume(ctx, nume_cautat):
    skin_gasit = None
    for id_skin, skin in skinuri_samp.items():
        if nume_cautat.lower() in skin["nume_skin"].lower():
            skin_gasit = skin
            await afiseaza_informatii_skin(ctx, id_skin, skin_gasit)
            return  # Întrerupe după prima potrivire
    if skin_gasit is None:
        await ctx.response.send_message(f'Skinul cu numele "{nume_cautat}" nu a fost găsit.', ephemeral=True)

async def afiseaza_informatii_skin(ctx, id_skin, skin):
    embed = nextcord.Embed(title=f'Informații despre skin (ID {id_skin})', color=0x3498db)
    embed.add_field(name="Nume Skin", value=skin["nume_skin"], inline=False)
    embed.add_field(name="Tip Skin", value=skin["tip_skin"], inline=False)
    embed.add_field(name="Gen", value=skin["gen"], inline=False)
    embed.add_field(name="Nume Model", value=skin["model_name"], inline=False)
    embed.set_image(url=skin["preview"])
    await ctx.response.send_message(embed=embed)

def setup(bot):
    @bot.slash_command(name='skin', description='Caută informații despre un skin.')
    async def cauta_skin(ctx, nume_cautat: str):
        try:
            nume_cautat = int(nume_cautat)
            skin = skinuri_samp.get(nume_cautat)
            if skin:
                await afiseaza_informatii_skin(ctx, nume_cautat, skin)
            else:
                await cauta_dupa_nume(ctx, nume_cautat)
        except ValueError:
            await cauta_dupa_nume(ctx, nume_cautat)

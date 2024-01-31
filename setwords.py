import nextcord
from nextcord.ext import commands
import json

# Funcții pentru gestionarea cuvintelor interzise
def incarca_cuvinte_interzise():
    try:
        with open('cuvinte_interzise.json', 'r') as f:
            data = json.load(f)
            return data["cuvinte"]
    except FileNotFoundError:
        return []

def salveaza_cuvinte_interzise(cuvinte):
    with open('cuvinte_interzise.json', 'w') as f:
        json.dump({"cuvinte": cuvinte}, f, indent=4)

def setup(bot):
    @bot.slash_command(name="setcuvinte", description="Actualizează lista de cuvinte interzise")
    @commands.has_permissions(administrator=True)
    async def setcuvinte(interaction: nextcord.Interaction, cuvinte: str):
        # Desparte cuvintele primite și actualizează lista
        cuvinte_lista = cuvinte.split(",")
        salveaza_cuvinte_interzise(cuvinte_lista)
        await interaction.response.send_message("Lista de cuvinte interzise a fost actualizată.", ephemeral=True)


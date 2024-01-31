import nextcord
from nextcord.ext import commands
import json

def incarca_cuvinte_interzise():
    try:
        with open('cuvinte_interzise.json', 'r') as f:
            data = json.load(f)
            return data.get("cuvinte", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
   

def salveaza_cuvinte_interzise(cuvinte):
    with open('cuvinte_interzise.json', 'w') as f:
        json.dump({"cuvinte": cuvinte}, f, indent=4)



def setup(bot):
    @bot.slash_command(name="setcuvinte", description="Adaugă cuvinte la lista de cuvinte interzise")
    @commands.has_permissions(administrator=True)
    async def setcuvinte(interaction: nextcord.Interaction, *, cuvinte: str):
        cuvinte_noi = cuvinte.split(",")
        cuvinte_curente = incarca_cuvinte_interzise()
        
        lista_actualizata = list(set(cuvinte_curente + cuvinte_noi))
        
        salveaza_cuvinte_interzise(lista_actualizata)
        
        await interaction.response.send_message("Lista de cuvinte interzise a fost actualizată.", ephemeral=True)

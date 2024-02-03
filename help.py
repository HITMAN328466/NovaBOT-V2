import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View

class HelpView(View):
    def __init__(self, *items, timeout=None):
        super().__init__(*items, timeout=timeout)

    async def show_category(self, interaction, category):
        embed = nextcord.Embed(title=f"🔷 Help: {category} 🔷", description=f"Descriere pentru {category}", color=0x3498db)
        if category == "General":
            embed.add_field(name="🔸 /avatar [membru]", value="Afișează avatarul membrului.", inline=False)
            embed.add_field(name="🔸 /ping", value="Arata ping-ul", inline=False)
            embed.add_field(name="🔸 /calc", value="calculeaza diferite calcule", inline=False)
            embed.add_field(name="🔸/feedback", value="Trimite un feedback sau o sugestie")
            embed.add_field(name="🔸/createticket", value="Creiaza un ticket" ,inline=False)
            # Continuă să adaugi alte comenzi pentru categoria General
        elif category == "Moderare":
            embed.add_field(name="🔸 /ban [membru]", value="Interzice un membru pe serverul Discord.", inline=False)
            # Continuă să adaugi alte comenzi pentru categoria Moderare
        # Adaugă aici alte categorii după necesități

        await interaction.response.edit_message(embed=embed, view=self)

class GeneralButton(Button):
    def __init__(self):
        super().__init__(label="General", style=nextcord.ButtonStyle.grey)

    async def callback(self, interaction: nextcord.Interaction):
        await self.view.show_category(interaction, "General")

class ModerareButton(Button):
    def __init__(self):
        super().__init__(label="Moderare", style=nextcord.ButtonStyle.grey)

    async def callback(self, interaction: nextcord.Interaction):
        await self.view.show_category(interaction, "Moderare")
def setup(bot):
   @bot.slash_command(name='help', description='Afișează comenzi disponibile')
   async def help_command(interaction: nextcord.Interaction):
    view = HelpView()
    view.add_item(GeneralButton())  # Ajustat pentru a nu mai include 'view' ca argument
    view.add_item(ModerareButton())  # Ajustat pentru a nu mai include 'view' ca argument
    embed = nextcord.Embed(title="🔷 Help: Categorii 🔷", description="Selectează o categorie pentru a vedea comenzi disponibile.", color=0x3498db)
    await interaction.response.send_message(embed=embed, view=view)
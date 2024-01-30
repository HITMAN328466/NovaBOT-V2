import nextcord
from nextcord.ext import commands
from datetime import datetime

def setup(bot):
    @bot.slash_command(name="feedback", description="Trimite un feedback sau o sugestie.")
    async def feedback(interaction: nextcord.Interaction, mesaj: str, rating: int = nextcord.SlashOption(description="Ratingul tău (1-5)", min_value=1, max_value=5)):
        channel = bot.get_channel(983067390998872114)  # Înlocuiește cu ID-ul real al canalului

        # Crearea unui embed pentru feedback
        embed = nextcord.Embed(title="Feedback Nou", color=0x00ff00)
        embed.add_field(name="Autor", value=interaction.user.mention, inline=False)
        embed.add_field(name="Mesaj", value=mesaj, inline=False)
        embed.add_field(name="Rating", value="⭐" * rating, inline=False)  # Adaugă stelele în funcție de rating
        embed.set_footer(text=f"Trimis de {interaction.user.name}")
        embed.timestamp = datetime.utcnow()

        # Trimiterea embed-ului către canal
        await channel.send(embed=embed)

        # Confirmarea pentru utilizator
        confirm_embed = nextcord.Embed(title="Feedback Trimis",
                                       description="Feedback-ul tău a fost trimis cu succes. Mulțumim pentru contribuție!",
                                       color=0x00ff00)
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

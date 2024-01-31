import nextcord
from nextcord.ext import commands

def setup(bot):
    @bot.slash_command(name="serverinfo", description="Afișează informații despre server")
    async def serverinfo(interaction: nextcord.Interaction):
        guild = interaction.guild
        if not guild:
            # Comanda a fost folosită în afara unui server
            await interaction.response.send_message("Această comandă trebuie utilizată într-un server.", ephemeral=True)
            return

        # Creează un embed cu informațiile despre server
        embed = nextcord.Embed(title=f"Informații despre {guild.name}", color=0x00ff00)
        embed.add_field(name="Proprietar", value=str(guild.owner), inline=True)
        embed.add_field(name="Creat pe", value=guild.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)
        embed.add_field(name="Membri", value=str(guild.member_count), inline=True)
        embed.add_field(name="Canale de voce", value=str(len(guild.voice_channels)), inline=True)
        embed.add_field(name="Canale text", value=str(len(guild.text_channels)), inline=True)
        embed.add_field(name="Nivel de securitate", value=str(guild.verification_level), inline=True)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        await interaction.response.send_message(embed=embed)

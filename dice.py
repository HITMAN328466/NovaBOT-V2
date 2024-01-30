import nextcord
from nextcord.ext import commands
import random

dice_images = {
    1: "https://www.calculatorsoup.com/images/dice/die_1.gif",
    2: "https://www.calculatorsoup.com/images/dice/die_2.gif",
    3: "https://www.calculatorsoup.com/images/dice/die_3.gif",
    4: "https://www.calculatorsoup.com/images/dice/die_4.gif",
    5: "https://www.calculatorsoup.com/images/dice/die_5.gif",
    6: "https://www.calculatorsoup.com/images/dice/die_6.gif"
}







def setup(bot):
    @bot.slash_command(name="dice", description="Aruncă un zar")
    async def dice(interaction: nextcord.Interaction):
        
        # Presupunând că ai un dicționar `dice_images` definit undeva în cod
        # De exemplu: dice_images = {1: "url1", 2: "url2", ..., 6: "url6"}
        number = random.randint(1, 6)
        image_url = dice_images[number]

        # Creează și trimite embed-ul
        embed = nextcord.Embed(title="Aruncarea zarului 🎲", description=f"Ai aruncat un {number}!")
        embed.set_image(url=image_url)
        await interaction.response.send_message(embed=embed)

import nextcord
from nextcord.ext import commands
import random

# Slot
class SlotMachineView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.emojis = ["🍒", "🍋", "🔔", "💎", "🍉"]

    @nextcord.ui.button(label="Spin", style=nextcord.ButtonStyle.green)
    async def spin_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Alege trei seturi de emoji aleatorii pentru rândurile sloturilor
        rows = [random.choices(self.emojis, k=3) for _ in range(3)]
        rows_str = [' | '.join(row) for row in rows]
        slot_display = "\n".join(rows_str)

        # Verifică dacă linia din mijloc este câștigătoare
        result = "WIN 🎉" if rows[1][0] == rows[1][1] == rows[1][2] else "LOST 😢"

        # Formează mesajul final
        result_display = f"**🎰 SLOTS 🎰**\n```\n{slot_display}\n```\n**{result}**"

        # Trimite rezultatul și reafișează butonul de Spin
        await interaction.response.edit_message(content=result_display, view=self)

# Slots
def setup(bot):
    @bot.slash_command(name="pacanele", description="Joacă la slot machine!")
    async def slots(interaction: nextcord.Interaction):
        view = SlotMachineView()
        await interaction.response.send_message("Apasă pe 'Spin' pentru a juca!", view=view)

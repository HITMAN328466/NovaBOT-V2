# Importuri Nextcord
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View, Select

#ticket button
class TicketView(nextcord.ui.View):
    def __init__(self, channel: nextcord.TextChannel):
        super().__init__()
        self.channel = channel

    @nextcord.ui.button(label="Închide Ticketul🔴", style=nextcord.ButtonStyle.red)
    async def close_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Verifică dacă persoana care apasă butonul este un administrator
        if interaction.user.guild_permissions.administrator:
            await self.channel.delete(reason="Ticket închis")
        else:
            await interaction.response.send_message("Doar un administrator poate închide acest ticket.", ephemeral=True)

class TicketCategoryView(nextcord.ui.View):
    def __init__(self, member: nextcord.Member, guild: nextcord.Guild):
        super().__init__()
        self.member = member
        self.guild = guild

    @nextcord.ui.select(placeholder="Alege categoria ticketului...", min_values=1, max_values=1,
                        options=[
                            nextcord.SelectOption(label="Suport Tehnic", description="Asistență tehnică", emoji="🔧"),
                            nextcord.SelectOption(label="Raportare Bug", description="Raportare de bug-uri", emoji="🐛"),
                            nextcord.SelectOption(label="General", description="Întrebări generale", emoji="❓")
                        ])
    async def select_callback(self, select: Select, interaction: nextcord.Interaction):
        category = select.values[0]
        await self.create_ticket(interaction, category)

    async def create_ticket(self, interaction: nextcord.Interaction, category: str):
        # Crează un nou canal pentru ticket
        overwrites = {
            self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self.member: nextcord.PermissionOverwrite(read_messages=True),
            self.guild.me: nextcord.PermissionOverwrite(read_messages=True)
        }
        
        ticket_channel = await self.guild.create_text_channel(f"ticket-{category.lower()}-{self.member.name}", overwrites=overwrites)

        # Adaugă butonul de închidere la canalul de ticket
        view = TicketView(channel=ticket_channel)
        await ticket_channel.send(f"{self.member.mention} Bine ai venit în ticketul tău pentru categoria '{category}'!", view=view)
        await interaction.response.send_message(f"Ticketul tău a fost creat: {ticket_channel.mention}", ephemeral=True)




def setup(bot):
    @bot.slash_command(name="createticket", description="Creează un nou ticket")
    async def create_ticket(interaction: nextcord.Interaction):
        view = TicketCategoryView(member=interaction.user, guild=interaction.guild)
        await interaction.response.send_message("Selectează categoria ticketului:", view=view, ephemeral=True)

















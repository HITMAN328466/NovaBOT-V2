import nextcord

import random
import os
import requests
import json
import datetime
from collections import Counter
from datetime import datetime, timedelta





from dotenv import load_dotenv
from nextcord.ext import commands
from nextcord.ui import View
from datetime import datetime, timedelta

from nextcord.ui import View, Button
from datetime import datetime
from pytz import timezone


from skins import skinuri_samp
from masini import masini_samp








        

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="g.", intents=intents)

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

#slost
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













@bot.event
async def on_ready():
    servers_count = len(bot.guilds)
    activity = nextcord.Game(name=f"pe {servers_count} servere")
    await bot.change_presence(activity=activity)
    
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

#comanda de avatar

@bot.slash_command(name="avatar", description="Arată avatarul tău sau al altui membru")
async def avatar(ctx, member: nextcord.Member = None):
    member = member or ctx.author

    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

    embed = nextcord.Embed(title=f"Avatarul lui {member.display_name}", color=nextcord.Color.blurple())
    embed.set_image(url=avatar_url)

    await ctx.send(embed=embed)

#comanda de ping

@bot.slash_command(name="ping", description="Verifică ping-ul botului")
async def ping(ctx):
    latency = bot.latency * 1000  # Convertim la milisecunde
    await ctx.send(f"Pong! Ping-ul botului este: {latency:.2f}ms")

@bot.slash_command(name="online", description="Afișează membrii online în server")
async def online_members(ctx):
    online_members = [member.name for member in ctx.guild.members if member.status == nextcord.Status.online]

    if online_members:
        online_list = "\n".join(online_members)
        embed = nextcord.Embed(
            title="Membri Online",
            description=f"Membri online în {ctx.guild.name}:\n{online_list}",
            color=0x00ff00  # Culoare verde
        )
    else:
        embed = nextcord.Embed(
            title="Membri Online",
            description=f"Niciun membru online în {ctx.guild.name} în acest moment.",
            color=0xff0000  # Culoare roșie
        )

    await ctx.send(embed=embed)



#comanda e ajutor

@bot.slash_command(name='help', description='Afișează comenzi disponibile')
async def help_command(ctx):
    help_embed = nextcord.Embed(title="🔷Commands Panel🔷", color=0x3498db)
    help_embed.add_field(name="🔸g.statusserver", value="Afișează statusul serverului Discord.")
    help_embed.add_field(name="🔸g.clear [numar_mesaje]", value="Șterge un număr specific de mesaje în canalul curent.")
    help_embed.add_field(name="🔸g.post [text/link]", value="Folosește !post pentru a face o postare pe canalul curent.")
    help_embed.add_field(name="🔸g.ban", value="Este folosită pentru a interzice un membru pe serverul Discord.")
    help_embed.add_field(name="🔸g.skin", value="Este folosită pentru a căuta un skin pentru SA-MP.")
    help_embed.add_field(name="🔸g.timeout", value="Este folosita de catre staff pentru a pune un membru pe pauza.")
    help_embed.add_field(name="🔸g.membru [membru]", value="Afișează informații despre un utilizator.")
    help_embed.add_field(name="🔸g.avatar [membru]", value="arata avatarul membrului .")
    help_embed.add_field(name="🔸g.lock [channel]", value="blocheaza accesul la canale (stffcommand).")
    help_embed.add_field(name="🔸g.unlock[channel]", value="deblocheaza accesul la canale (stffcommand).")

    help_embed.set_footer(text="Folosește g.ajutor [comandă] pentru detalii suplimentare.")

    bot_id = bot.user.id
    permissions = nextcord.Permissions.all()
    invite_link = nextcord.utils.oauth_url(bot_id, permissions=permissions)

    button = Button(label="📨Invită botul", url=invite_link)
    view = View()
    view.add_item(button)

    await ctx.send(embed=help_embed, view=view)

    async def on_button_click(interaction):
        if interaction.component.label == "📨Invită botul":
            await interaction.followup.send("Link de invitație: " + invite_link)

    bot.add_listener(on_button_click, 'on_button_click')

#comanda de post

@bot.command(name='post', description='Copiază un mesaj într-un alt canal.')
async def copiapost_command(ctx, canal_destinatie: nextcord.TextChannel, *, mesaj_de_copiat):
    if not mesaj_de_copiat and not ctx.message.attachments:
        await ctx.send("Vă rugăm să furnizați cel puțin un mesaj sau să încărcați o imagine.")
        return

    try:
        embed = nextcord.Embed(description=mesaj_de_copiat, color=0x3498db)

        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        if ctx.message.attachments:
            # Verificăm dacă există atașamente (imagini)
            image_url = None
            for attachment in ctx.message.attachments:
                if attachment.url.endswith(('png', 'jpeg', 'jpg', 'gif')):
                    image_url = attachment.url
                    break

            if image_url:
                # Dacă avem o imagine validă, o adăugăm la embed
                embed.set_image(url=image_url)

        await canal_destinatie.send(embed=embed)
    except nextcord.Forbidden:
        await ctx.send("Nu am permisiuni pentru a trimite mesaje în canalul specificat.")
    except nextcord.HTTPException:
        await ctx.send("A apărut o eroare în timpul copierii mesajului sau încărcării imaginii.")

#comanda de ban si unban

@bot.slash_command(name='ban', description='Interzice un membru.')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: nextcord.Member, *, reason="Fără motiv specificat."):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} a fost interzis. Motiv: {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nu aveți permisiuni pentru a interzice membrii.")

@bot.slash_command(name='unban', description='Deblochează un membru.')
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: str):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for entry in banned_users:
        user = entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} a fost deblocat.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nu aveți permisiuni pentru a debloca membrii.")

#commanda de cautat skinuri

@bot.slash_command(name='skin', description='Caută informații despre un skin.')
async def cauta_skin(ctx, nume_cautat: str):
    try:
        nume_cautat = int(nume_cautat)
        if nume_cautat in skinuri_samp:
            skin = skinuri_samp[nume_cautat]
            await afiseaza_informatii_skin(ctx, nume_cautat, skin)
        else:
            await cauta_dupa_nume(ctx, nume_cautat)
    except ValueError:
        await cauta_dupa_nume(ctx, nume_cautat)

async def cauta_dupa_nume(ctx, nume_cautat):
    skin_gasit = None
    for id_skin, skin in skinuri_samp.items():
        if nume_cautat.lower() in skin["nume_skin"].lower():
            skin_gasit = skin
            await afiseaza_informatii_skin(ctx, id_skin, skin_gasit)
    if skin_gasit is None:
        await ctx.send(f'Skinul cu numele "{nume_cautat}" nu a fost găsit.')

async def afiseaza_informatii_skin(ctx, id_skin, skin):
    embed = nextcord.Embed(title=f'Informații despre skin (ID {id_skin})', color=0x3498db)
    embed.add_field(name="Nume Skin", value=skin["nume_skin"])
    embed.add_field(name="Tip Skin", value=skin["tip_skin"])
    embed.add_field(name="Gen", value=skin["gen"])
    embed.add_field(name="Nume Model", value=skin["model_name"])
    embed.set_image(url=skin["preview"])
    await ctx.send(embed=embed)

#comanda pentru masini
    
@bot.slash_command(name='car' , description="cauta detali despre masina")
async def masina_info(ctx, masina_dorita):
    masina_dorita= masina_dorita.lower()
    vehicle_name   = ""
    id_masina = ""
    url_imagine = ""
    category = ""
    modifications = ""
    model_name = ""
    num_seats = ""

    if masina_dorita in masini_samp:
        mașină = masini_samp[masina_dorita]
        id_masina = mașină["id"]
        url_imagine = mașină["imagine"]
        vehicle_name = masina_dorita.capitalize()
        category = "Categorie: " + mașină.get("categoria", "Nedeterminată")
        modifications = "Modificări: " + mașină.get("modificari", "Niciuna")
        model_name = "Model name: " + mașină.get("model_name", masina_dorita)
        num_seats = "Number of seats: " + str(mașină.get("numar_scaune", 2))

    elif masina_dorita.isdigit():
        for nume, detalii_masina in masini_samp.items():
            if str(detalii_masina["id"]) == masina_dorita:
                vehicle_name = nume.capitalize()
                id_masina = detalii_masina["id"]
                url_imagine = detalii_masina.get("imagine", "")
                category = "Categorie: " + detalii_masina.get("categoria", "Nedeterminată")
                modifications = "Modificări: " + detalii_masina.get("modificari", "Niciuna")
                model_name = "Model name: " + detalii_masina.get("model_name", nume)
                num_seats = "Number of seats: " + str(detalii_masina.get("numar_scaune", 2))
                break

    if vehicle_name:
        embed = nextcord.Embed(title=f"Vehicle Model ID: {id_masina}", color=0x3498db)
        embed.set_image(url=url_imagine)
        embed.add_field(name="Vehicle Name", value=vehicle_name)
        embed.add_field(name="Category", value=category)
        embed.add_field(name="Modifications", value=modifications)
        embed.add_field(name="Model name", value=model_name)
        embed.add_field(name="Number of seats", value=num_seats)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Nu am putut găsi mașina cu numele sau ID-ul '{masina_dorita}'.")    
#comanda de lock si unlock

@bot.slash_command(name='lock')
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx, channel: nextcord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"Canalul {channel.mention} a fost blocat.")

@bot.slash_command(name='unlock')
@commands.has_permissions(manage_channels=True)
async def unlock_channel(ctx, channel: nextcord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"Canalul {channel.mention} a fost deblocat.")
      

@bot.slash_command(name="giverole", description="Oferă un rol unui membru")
@commands.has_permissions(manage_channels=True)
async def giverole(ctx, member: nextcord.Member, role: nextcord.Role):
    try:
        await member.add_roles(role)
        await ctx.send(f"Rolul {role.name} a fost adăugat cu succes membrului {member.display_name}.")
    except Exception as e:
        await ctx.send(f"A apărut o eroare: {e}")


@bot.slash_command(name="calc", description="calculeaza diferite calcule")
async def calculate(ctx, *, expression: str):
    try:
        result = eval(expression)
        await ctx.send(f"Rezultat: {result}")
    except Exception as e:
        await ctx.send(f"A apărut o eroare în timpul calculului: {e}")

@bot.slash_command(name="serverinfo", description="Arata date despre server")
async def serverinfo(ctx):
    guild = ctx.guild
    if not guild:
        # Comanda a fost folosită în afara unui server
        await ctx.send("Această comandă trebuie utilizată într-un server.")
        return

    # Creează un embed cu informațiile despre server
    embed = nextcord.Embed(title=f"Informații despre {guild.name}", color=0x00ff00)
    embed.add_field(name="Proprietar", value=str(guild.owner), inline=True)
    embed.add_field(name="Creat pe", value=guild.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)
    embed.add_field(name="Membri", value=str(guild.member_count), inline=True)
    embed.add_field(name="Canale de voce", value=str(len(guild.voice_channels)), inline=True)
    embed.add_field(name="Canale text", value=str(len(guild.text_channels)), inline=True)
    embed.add_field(name="Nivel de securitate", value=str(guild.verification_level), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else "")

    await ctx.send(embed=embed)

#tickt command 
@bot.slash_command(name="createticket", description="Creează un nou ticket")
async def create_ticket(interaction: nextcord.Interaction, subject: str):
    guild = interaction.guild
    member = interaction.user

    # Crează un nou canal pentru ticket
    overwrites = {
        guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        member: nextcord.PermissionOverwrite(read_messages=True),
        guild.me: nextcord.PermissionOverwrite(read_messages=True)
    }

    ticket_channel = await guild.create_text_channel(f"ticket-{member.name}", overwrites=overwrites)

    # Creează view-ul pentru butonul de închidere și adaugă-l la mesajul din canalul de ticket
    view = TicketView(channel=ticket_channel)
    await ticket_channel.send(f"{member.mention} Bine ai venit în ticketul tău! Subiect: {subject}", view=view)
    await interaction.response.send_message(f"Ticketul tău a fost creat: {ticket_channel.mention}", ephemeral=True)


#clear chat 
@bot.slash_command(name="clearmsg", description="sterge mesaje")
@commands.has_permissions(manage_messages=True)  # Asigură-te că doar utilizatorii cu permisiunea de a gestiona mesajele pot folosi această comandă
async def clear(ctx, num: int):
    if num < 1:
        await ctx.send("Te rog să specifici un număr valid de mesaje pentru a fi șterse.")
        return

    deleted = await ctx.channel.purge(limit=num)
    await ctx.send(f'Șterse {len(deleted)} mesaje.', delete_after=5)  # Mesajul de confirmare se va șterge automat după 5 secunde


#welcome settings

# Încarcă sau inițializează setările de welcome
def load_welcome_settings():
    try:
        with open("welcome_settings.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"channel_id": None, "welcome_message": "Bine ai venit, {member}!"}

welcome_settings = load_welcome_settings()

# Salvează setările de welcome
def save_welcome_settings():
    with open("welcome_settings.json", "w") as file:
        json.dump(welcome_settings, file, indent=4)

@bot.slash_command(name="setwelcome", description="seteaza cnalul de welcome")
@commands.has_permissions(administrator=True)
async def set_welcome(ctx, channel: nextcord.TextChannel, *, welcome_message: str):
    welcome_settings["channel_id"] = channel.id
    welcome_settings["welcome_message"] = welcome_message
    save_welcome_settings()
    await ctx.send(f"Canalul de welcome a fost setat la {channel.mention} cu mesajul: \"{welcome_message}\"")

@bot.event
async def on_member_join(member):
    channel_id = welcome_settings.get("channel_id")
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            welcome_message = welcome_settings["welcome_message"].format(member=member.mention)
            await channel.send(welcome_message)

#slots
@bot.slash_command(name="slots", description="Joacă la slot machine!")
async def slots(interaction: nextcord.Interaction):
    view = SlotMachineView()
    await interaction.response.send_message("Apasă pe 'Spin' pentru a juca!", view=view)

#dice
dice_images = {
    1: "https://www.calculatorsoup.com/images/dice/die_1.gif",
    2: "https://www.calculatorsoup.com/images/dice/die_2.gif",
    3: "https://www.calculatorsoup.com/images/dice/die_3.gif",
    4: "https://www.calculatorsoup.com/images/dice/die_4.gif",
    5: "https://www.calculatorsoup.com/images/dice/die_5.gif",
    6: "https://www.calculatorsoup.com/images/dice/die_6.gif"
}

@bot.slash_command(name="dice", description="Aruncă un zar")
async def dice(interaction: nextcord.Interaction):
    number = random.randint(1, 6)
    image_url = dice_images[number]

    # Creează și trimite embed-ul
    embed = nextcord.Embed(title="Aruncarea zarului 🎲", description=f"Ai aruncat un {number}!")
    embed.set_image(url=image_url)
    await interaction.response.send_message(embed=embed)


bot.run(DISCORD_TOKEN)

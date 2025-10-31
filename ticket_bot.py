import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ticket_count = 0  # shomaresh channel ticket ha


@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")


class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

        # button baraye sakhte ticket
        self.add_item(Button(label="Create Ticket 🎫", style=discord.ButtonStyle.green, custom_id="create_ticket"))

    @discord.ui.button(label="Create Ticket 🎫", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        global ticket_count
        guild = interaction.guild
        ticket_count += 1

        # esm channel jadid
        channel_name = f"ticket-{ticket_count:03}"

        # ijad channel jadid
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        # faghat admin ha betoonan bebinan
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(channel_name, overwrites=overwrites, reason="New support ticket")

        await interaction.response.send_message(
            f"✅ Ticket created: {channel.mention}", ephemeral=True
        )
        await channel.send(f"🎟️ Welcome {interaction.user.mention}! An admin will assist you soon.")


@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title="For Support or Test Click on Button",
        description="To create a ticket use the **Create Ticket** button below.",
        color=0x2ecc71
    )
    embed.set_footer(text="TicketTool.xyz - Ticketing without clutter")

    view = TicketView()
    await ctx.send(embed=embed, view=view)


bot.run("TOKEN_HERE")

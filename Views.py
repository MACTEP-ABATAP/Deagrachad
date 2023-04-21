import discord
class View(discord.ui.View):
    @discord.ui.button(label="Нажми на меня", style=discord.ButtonStyle.danger, emoji="☑️")
    async def button_callback(self, Button, interaction):
        await interaction.response.send_message("DO NOT CLICK THE BUTTON")
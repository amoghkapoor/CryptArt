import discord
from discord.ext import commands
from discord.ext.commands import bot
from user_nft import user_nft
from discord import app_commands

class display_nft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @app_commands.command(name="list", description="A command to list all NFTs stored in a crypto wallet")
    @app_commands.describe(wallet="The address of the wallet you want to see NFTs of")
    async def list(self, interaction, wallet: str):
        class choose_blockchain(discord.ui.View):
            def __init__(self, user_id):
                super().__init__()
                self.value = None
                self.og_user = user_id

            @discord.ui.button(label='Polygon', style=discord.ButtonStyle.blurple)
            async def poly(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.og_user:
                    await interaction.response.send_message(content="Hey you're not allowed to interact with this menu because you didn't start it.", ephemeral=True)
                    return
                self.value = 'polygon'
                await interaction.response.defer()
                self.stop()

            @discord.ui.button(label='Ethereum', style=discord.ButtonStyle.blurple)
            async def eth(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.og_user:
                    await interaction.response.send_message(content="Hey you're not allowed to interact with this menu because you didn't start it.", ephemeral=True)
                    return
                self.value = 'eth'
                await interaction.response.defer()
                self.stop()

        class control_embed(discord.ui.View):
            def __init__(self, embeds_list, user_id):
                super().__init__(timeout=300)
                self.value = 0
                self.embeds_list = embeds_list
                self.og_user = user_id

            @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.blurple)
            async def back(self, interaction: discord.Interaction, button):
                if interaction.user.id != self.og_user:
                    await interaction.response.send_message(content="Hey you're not allowed to interact with this menu because you didn't start it.", ephemeral=True)
                    return
                self.value -=1
                if self.value <0:
                    self.value = len(self.embeds_list)-1
                await interaction.response.edit_message(embed=self.embeds_list[self.value])

            @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.blurple)
            async def forward(self, interaction: discord.Interaction, button):
                if interaction.user.id != self.og_user:
                    await interaction.response.send_message(content="Hey you're not allowed to interact with this menu because you didn't start it.", ephemeral=True)
                    return
                self.value +=1
                if self.value == len(embed_list):
                    self.value = 0
                await interaction.response.edit_message(embed=self.embeds_list[self.value])

            async def on_timeout(self):
                for i in self.children:
                    i.disabled=True
                await interaction.edit_original_response(view=self)


        view = choose_blockchain(interaction.user.id)
        await interaction.response.send_message(content="Choose your blockchain!!", view=view, embed=None)
        await view.wait()

        blockchain = None
        if view.value == None:
            await interaction.edit_original_response(content="You didn't reply in time. Try again", view=None)
            return
        if view.value == 'polygon':
            blockchain="polygon"
        else:
            blockchain = "goerli"

        message = user_nft(wallet, blockchain)
        if message['response'] == "NOK":
            await interaction.edit_original_response(content="You entered a wrong wallet address", view=None, embed=None)
            return

        nfts_list = message["nfts"]
        length = int(message["total"])
        embed_list = []
        for i in range(length):
            embed = discord.Embed(title="Name: {}".format(nfts_list[i]["name"]),
                                  description="Description: {}".format(nfts_list[i]["description"]))
            embed.set_image(url=nfts_list[i]["file_url"])
            embed.set_footer(text="Contract Address: {}\nToken ID: {}\nNFT no. {}/{}".format(nfts_list[i]["contract_address"],
                                                                              nfts_list[i]["token_id"], i+1, length))
            embed.add_field(name="File Link: ", value=nfts_list[i]["file_url"])
            embed_list.append(embed)



        control = control_embed(embed_list, interaction.user.id)
        await interaction.edit_original_response(content=f"NFTs linked with {wallet}", view=control, embed=embed_list[0])


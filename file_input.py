import json

import discord
from discord.ext import commands
from minter import mint_on_polygon, mint_on_eth



class file_input(commands.Cog):
    def __init__(self, bot):
        self.bot = bot









    #yes no menu which returns true or false value. Add to any message

    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)
            self.value = None

        async def on_timeout(self):
            self.stop()

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            for i in self.children:
                i.disabled = True
            self.value = True
            await interaction.response.edit_message(view=self)
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            for i in self.children:
                i.disabled = True
            self.value = False
            await interaction.response.edit_message(view=self)
            self.stop()












    #discord listener which looks for any attachments in messages

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments == None:
            return
        favourable_files = [i for i in message.attachments if i.filename.split(".")[1] in ["gif", "png", "jpeg", "jpg", "mp4"]]
        if len(favourable_files) == 0:
            return

        view = self.Confirm()




        #asking if the user actually wants to mint a NFT

        msg = await message.channel.send('Do you want to mint NFT?', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value == True:
            await msg.edit(content="Ok please move over to DMs for providing details.\n\nWe move to DMs for security purposes.",view=None)
        elif view.value == False:
            await msg.edit(content="Ok I won't mint a NFT", view=None)
            return
        else:
            await msg.edit(content="I guess you didn't want to mint a NFT", view=None)
            return






        #choose which file to mint

        #store the file to mint in a variable
        file_to_mint = None

        class take_NFT_details(discord.ui.Modal,title="Give details for your NFT!!!"):
            name = discord.ui.TextInput(
                label="Enter a name for the NFT",
                placeholder="name",
                min_length=3,
                max_length=60,
            )
            description = discord.ui.TextInput(
                label="Description for the NFT",
                placeholder="description",
                min_length=5,
                max_length=200,
            )

            address = discord.ui.TextInput(
                label="The wallet address to send the NFT to",
                placeholder="wallet address",
                min_length=42,
                max_length=42,
            )

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.defer()
                self.stop()




        name = None
        description = None
        address = None
        #if only one favorable file, choose it
        if len(favourable_files) == 1:
            file_to_mint = favourable_files[0]
            view = discord.ui.View(timeout=60)
            button = discord.ui.Button(label="open form")
            modal = take_NFT_details()
            async def callback(interaction):
                await interaction.response.send_modal(modal)
                await modal.wait()
                view.stop()
            button.callback = callback
            view.add_item(button)
            user = self.bot.get_user(message.author.id)
            msg = await user.send(content="Enter the details for NFT!",view=view)
            await view.wait()
            name = modal.name.value
            if name == "" or name == None:
                await msg.edit(view=None, embed=None, content="Guess you didn't want to mint an NFT. Timed out.")
                return
            description = modal.description.value
            address = modal.address.value


        #give user a list of favorable files and then ask them to choose one.
        else:
            #adding embeds with a display of the image
            embeds = []
            for i in range(len(message.attachments)):
                embed = None
                if message.attachments[i].filename.split('.')[1] in ["png", "jpg", "jpeg"]:
                    embed = discord.Embed(title=str(i+1)+'.')
                    embed.set_thumbnail(url =message.attachments[i])
                else:
                    embed = discord.Embed(title=str(i+1)+". "+message.attachments[i].filename)
                embeds.append(embed)



            #adding a view with buttons for each file
            #class to define a view with a value parameter as well which will store which button was chosen by mapping the unique id
            class choose_buttons(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=60)
                    self.value = None
                    self.button_ids = []
                    self.modal = None

                async def callback_choose_button(self, interaction):
                    self.modal = take_NFT_details()
                    await interaction.response.send_modal(self.modal)
                    await self.modal.wait()
                    self.stop()
                    self.value = self.button_ids.index(interaction.data['custom_id'])


            view = choose_buttons()



            #we'll store the custom ids of all buttons and when callback function is invoked, we'll map the custom id with the position in the list to check which file was chosen
            for i in range(len(favourable_files)):
                x = discord.ui.Button(label=str(i+1), style=discord.ButtonStyle.blurple)
                x.callback = view.callback_choose_button
                view.button_ids.append(x.custom_id)
                view.add_item(x)

            user = self.bot.get_user(message.author.id)
            msg = await user.send(embeds=embeds, view=view)
            await view.wait()
            if view.value != None:
                file_to_mint = favourable_files[view.value]

            if file_to_mint == None:
                await msg.edit(view=None, content="Looks like you didn't respond in time. Try again if you want to mint the NFT.", embeds=[])
                return

            name = view.modal.name.value
            description = view.modal.description.value
            address = view.modal.address.value


        class choose_blockchain(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None

            @discord.ui.button(label='Polygon', style=discord.ButtonStyle.blurple)
            async def poly(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.value = 'polygon'
                await interaction.response.defer()
                self.stop()

            @discord.ui.button(label='Ethereum', style=discord.ButtonStyle.blurple)
            async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.value = 'eth'
                await interaction.response.defer()
                self.stop()

        view = choose_blockchain()
        await msg.edit(content="Choose your blockchain!!", view=view, embed=None)
        await view.wait()
        blockchain = None
        if view.value == None:
            await msg.edit(content="You didn't reply in time. Try again", view=None)
            return
        if view.value == 'polygon':
            blockchain="polygon"
        else:
            blockchain = "ethereum"
        embed = discord.Embed(title="We are minting your NFT!")
        embed.add_field(name="Name:", value=name)
        embed.add_field(name="description", value=description)
        embed.add_field(name="wallet address", value=address)
        embed.add_field(name="blockchain", value=blockchain)
        embed.add_field(name="file", value=file_to_mint.url)
        if file_to_mint.filename.split('.')[1] in ['png', 'gif', 'jpg', 'jpeg']:
            embed.set_thumbnail(url=file_to_mint.url)
        embed.set_footer(text="If your wallet address is wrong, minting process won't work")
        await msg.edit(view=None, embed=embed, content="")
        response = None
        if blockchain == 'polygon':
            response = mint_on_polygon(file_to_mint.url, file_to_mint.filename.split('.')[1], name, description, address)
        else:
            response = mint_on_eth(file_to_mint.url, file_to_mint.filename.split('.')[1], name, description, address)
        if "error" in response:
            embed.colour=discord.Colour.red()
            embed.title="We can't mint your NFT right now 😔"
            await msg.edit(content="The address that you entered is probably wrong or there was some error while minting. Please try again.", embed=embed)
            return
        else:
            x = json.loads(response)
            embed = discord.Embed(colour=discord.Colour.green(), title="Success!")
            embed.add_field(name="NFT name", value= x['name'])
            embed.add_field(name="NFT description", value=x['description'])
            embed.add_field(name="Blockchain", value= blockchain)
            embed.add_field(name="Contract address", value=x['contract_address'])
            embed.add_field(name="Transaction hash", value=x['transaction_hash'])
            embed.add_field(name="Transaction_external_url", value=x['transaction_external_url'])
            embed.add_field(name="Wallet address", value=x['mint_to_address'])
            embed.set_footer(text="Thanks for using our bot!")
            if file_to_mint.filename.split('.')[1] in ['png', 'gif', 'jpg', 'jpeg']:
                embed.set_thumbnail(url=file_to_mint.url)
            await msg.edit(content="Successfully minted on blockchain", embed = embed)

            x = None
            with open("NFTs_minted.json", "r+") as json_file:
                x = json.load(json_file)['minted']
                x+=1
            with open("NFTs_minted.json", "w+") as json_file:
                json.dump({'minted':x}, json_file)




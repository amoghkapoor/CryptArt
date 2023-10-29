import discord
from discord import app_commands
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="A help guide for CryptArt!")
    async def help(self, interaction):
        embed = discord.Embed(title=" ",
                              description="Hello there! I am CrypArt and I am here at your service to make it easier for you to upload your artistic creations as NFTs.",
                              color=0xcce5f5)
        embed.set_author(name="CryptArt Help Menu")
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1167533630541791306/1167951117062262784/Untitled_2.png?ex=654ffe3d&is=653d893d&hm=2247558082dbadbc7e712384dc63e0f46318611650f9815c90783b1f92e752d1&=&width=581&height=581")
        embed.add_field(name="How to convert your work into NFT?",
                        value="Your art work be it video or image can be converted into NFT by simply sending it on the same channel on which I, CryptArt, am present. From there onwards I will simply guide you.",
                        inline=False)
        embed.add_field(name="What if the files you are sending are not meant to be converted to NFTs?",
                        value="If the files that you are sending are not meant to be minted into NFTs, simply create a separate minting channel and give me read access only to that one :)",
                        inline=False)
        embed.add_field(name="What files are supported for minting?",
                        value="Your artwork can be as any of these file types: .png , .jpg, .jpeg , .gif and .mp4",
                        inline=False)
        embed.add_field(name="On which blockchain will your NFTs be minted?",
                        value="Don't worry I'll provide you the option of minting your NFTs onto either of the two popular blockchains Ethereum or Polygon.",
                        inline=False)
        embed.add_field(name="How to mint your NFTs to a specific block chain?",
                        value="For minting your NFTs onto any of the blockchains it is necessary for you to have a pre existing Crypto-Wallet. I KNOW! I KNOW! that you are worried about the security aspect of it but I will make this process secure by not asking about your private key and by continuing the minting process in you dms ;)",
                        inline=False)
        embed.add_field(name="What does the /list slash command do?",
                        value="It enables you to list out all the NFTs stored in any crypto wallet on polygon or ethereum blockchain with an interactive menu to navigate through it",
                        inline=False)
        embed.set_footer(text="- made with 💖 by our small team _H4CK3RS_")

        await interaction.response.send_message(embed=embed)
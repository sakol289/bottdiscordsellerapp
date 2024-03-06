import nextcord, json, requests, re
from nextcord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from Config import Config
from utils.Cybersafeapi import Cybersafeapi
from bs4 import BeautifulSoup

dtlike = Config("database/apps.json").Get()


class App(nextcord.ui.Modal):
    def __init__(self,bot,app,idapp,message: nextcord.Message):
        self.bot = bot
        self.app = app
        self.idapp = idapp
        self.message = message
        super().__init__(auto_defer=True, title="Verify")
        self.Input_amount = nextcord.ui.TextInput(
            label="amount",
            style=nextcord.TextInputStyle.short,
            required=True,
            placeholder="ใส่ amount",
        )
        self.add_item(self.Input_amount)
        
    
    def newurl(self,url1):
        url = "https://url.in.th/shorten"

        payload = {'url': url1}
        headers = {
        'authority': 'url.in.th',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': 'https://url.in.th',
        'pragma': 'no-cache',
        'referer': 'https://url.in.th/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 Edg/122.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return(response.json()["data"]["shorturl"])

    def newdt(self,text):
        plain_text = text.replace('<br>', '\n')
        # ใช้ BeautifulSoup เพื่อลบ HTML tags
        text = BeautifulSoup(plain_text, 'html.parser').text
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+\S+'
        urls = re.findall(url_pattern, text)

        # พิมพ์ลิ้งค์ URL ที่พบ
        for url in urls:
            new_url = self.newurl(url)
            text = re.sub(url, new_url, text)
        return text

            
    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send("send",delete_after=0)
        # await self.message.edit(f"{self.app} {self.idlike} {self.Input_link.value} {self.Input_amount.value}",embed=None,view=None)
        await self.message.edit(content='[SELECT] กำลังตรวจสอบ',embed=None,view=None)
        userdata = json.load(open('./database/users.json', 'r', encoding='utf-8'))
        embed = nextcord.Embed()
        if (self.Input_amount.value.isnumeric()):
            if (str(interaction.user.id) in userdata):
                price = float(self.app["new_price"]) * float(self.Input_amount.value)
                await self.message.edit(content=f"ซื้อ {self.app['name']} price {price}")
                Dtstoresocial_id = Cybersafeapi().Dtstoresocial_id(self.app["id"])
                print(Dtstoresocial_id.json()["result"][0]["amount"])
                if(Dtstoresocial_id.json()["result"][0]["amount"] != 0):
                    if (userdata[str(interaction.user.id)]['point'] >= price):
                        reponse = Cybersafeapi().Buystoresocial(Config().Get()['configweb']['token'],self.app["id"],self.Input_amount.value)
                        e = reponse.json()
                        print(e)
                        plain_text = e["result"]["t_detali"]
                        # ใช้ BeautifulSoup เพื่อลบ HTML tags
                        t_detali = self.newdt(plain_text)
                        # print(e)
                        if e["status"] == "succeed":

                            userdata[str(interaction.user.id)]['point'] -= price
                            userdata[str(interaction.user.id)]['spend'] += price
                            userdata[str(interaction.user.id)]['history'].append({
                                "type": "buyapp",
                                "item": f"idapp_{self.app['id']}",
                                "price": price,
                                "description": f"auto {self.app['name']} price {price} name {self.app['name']}",
                                "time": str(datetime.now()),
                            })
                            json.dump(userdata, open('./database/users.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
                                
                            embed.title = '``✅`` ซื้อสินค้าสำเร็จ'
                            embed.description = f'''บอทได้ส่งข้อมูลไปยังแชทส่วนตัวของคุณแล้ว\nยอดเงินคงเหลือ : `` {userdata[str(interaction.user.id)]["point"]} ``'''
                            embed.color = nextcord.Color.from_rgb(0, 255, 0)

                            embedDM = nextcord.Embed()
                            embedDM.title = f'''ซื้อ {self.app['name']} สำเร็จ'''
                            embedDM.color = nextcord.Color.from_rgb(0, 255, 0)
                            embedDM.set_image(url=Config().Get()["embed"]["imglogo"])
                            embedDM.description = f'''
            > `user`: <@{interaction.user.id}>
            > `app`: {self.app['name']}
            > `price`: {price} บาท
            > `amount`: {self.Input_amount.value}
            > `detali`: {t_detali}
            > `time`: {str(datetime.now())}
            '''
                            await interaction.user.send(embed=embedDM)
                            
                            
                            # ส่งงาน
                            embedSubmit = nextcord.Embed()
                            embedSubmit.title = f'''ซื้อ {self.app['name']} สำเร็จ'''
                            embedSubmit.description = f'''
            :mens: `ซื้อโดย` <@{interaction.user.id}>ㅤㅤ:money_with_wings:  `ราคา` : `{price} บาท`
            '''
                            embedSubmit.color = nextcord.Color.from_rgb(0, 255, 0)
                            embedSubmit.set_image(url=Config().Get()["embed"]["imglogo"])
                            try:
                                await self.bot.get_channel(int(Config().Get()['submitChannelId'])).send(embed=embedSubmit)
                            except Exception as error:
                                print('fail send message', str(error))
                            
                            embeAdmin = nextcord.Embed()
                            embeAdmin.title = f'''ซื้อ {self.app['name']} สำเร็จ'''
                            embeAdmin.color = nextcord.Color.from_rgb(0, 255, 0)
                            embeAdmin.description = f'''
            > `user`: <@{interaction.user.id}>
            > `status`: {self.app['name']}
            > `price`: {price} บาท
            > `amount`: {self.Input_amount.value}
            > `detali`: {t_detali}
            > `time`: {str(datetime.now())}
            '''
                        try:
                            await self.bot.get_channel(int(Config().Get()['channelAppLog'])).send(embed=embeAdmin)
                        except Exception as error:
                            print('fail send message', str(error))
                        else:
                            embed.title = '`❌﹕` สั่งซื้อไม่สำเร็จ'
                            embed.description = f'''
                คุณไม่สามารถสั่งซื้อสำเร็จได้
                หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า `{e['msg']}`
                '''
                            embed.color = nextcord.Color.from_rgb(255, 0, 0)
                        await self.message.edit(content=None,embed=embed)
                    else:
                        need = price - userdata[str(interaction.user.id)]['point']
                        embed.description = f'คุณมียอดคงเหลือ {userdata[str(interaction.user.id)]["point"]} บาท\nต้องการทั้งหมด {price} บาท (ขาดอีก {need} บาท)'
                        embed.color = nextcord.Color.from_rgb(255, 0, 0)
                        await self.message.edit(content=None,embed=embed)
                else:
                    embed.title = '`❌﹕` สินค้าหมดกรุณาติดต่อแอดมิน'
                    embed.description = f'''
            คุณไม่สามารถสั่งซื้อสำเร็จได้
            หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า
            '''
                    embed.color = nextcord.Color.from_rgb(255, 0, 0)
                    await self.message.edit(content=None,embed=embed)
            else:
                embed.title = '`❌﹕` ไม่พบบัญชีในระบบ'
                embed.description = f'''
                คุณสามารถเปิดบัญชีด้วยการเติมเงินเท่าไหร่ก็ได้โดยใช้คําสั่ง ``/topup``
                หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า
                '''
                embed.color = nextcord.Color.from_rgb(255, 0, 0)
                await self.message.edit(content=None,embed=embed)
        else:
            embed.title = '`❌﹕` กรุณากรอกตัวเลข'
            embed.description = f'''
            คุณสามารถใช้งานได้แค่ตัวเลขเท่านั้น
            '''
            embed.color = nextcord.Color.from_rgb(255, 0, 0)
            await self.message.edit(content=None,embed=embed)



class appPremiumSellView(nextcord.ui.View):

    def __init__(self,bot, app,idapp, message: nextcord.Message):

        self.bot = bot
        self.app = app
        self.idapp = idapp
        self.message = message
        
        super().__init__(timeout=None)
        self.is_persistent()
    @nextcord.ui.button(
        label='ซื้อสินค้า',
        custom_id='buyproduct',
        style=nextcord.ButtonStyle.green,
        emoji='🛒'
    )
    async def buyproduct(self,button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(App(self.bot,self.app,self.idapp,message=self.message))



    @nextcord.ui.button(
        label='ยกเลิก',
        custom_id='appcancel',
        style=nextcord.ButtonStyle.red,
        emoji='❌'
    )
    async def appcancel(self, button: nextcord.Button, interaction: nextcord.Interaction):
        return await self.message.edit(embed=None,view=None,content='ยกเลิกสำเร็จ')

class appPremiumSelect(nextcord.ui.Select):

    def __init__(self, bot):
        self.bot = bot

        options = []

        for app in dtlike:
            options.append(nextcord.SelectOption(
                label=dtlike[app]["name"],
                value=app,
                description=f'{dtlike[app]["name"]} ({dtlike[app]["new_price"]} บาท  ต่อ 1ชิ้น)',
            ))

        super().__init__(
            custom_id='select-app-premium',
            placeholder='เลือกสินค้าที่คุณต้องการจะซื้อ',
            min_values=1,
            max_values=1,
            options=options
        )
        
        
        
    async def callback(self, interaction: nextcord.Interaction):
        message = await interaction.response.send_message(content='[SELECT] กำลังตรวจสอบ',ephemeral=True)
        id = self.values[0]
        app = dtlike[(self.values[0])]
        embed = nextcord.Embed()
        embed.title = app['name']
        embed.description = f'''
ราคา : ``{app['new_price']} บาท ต่อ 1ชิ้น``
'''
        await interaction.message.edit(view=appPremiumView(bot=self.bot))
        embed.color = nextcord.Color.from_rgb(100, 255, 255)
        # print(app["img"])
        # embed.set_image(url=app["img"])
        await message.edit(embed=embed,view=appPremiumSellView(bot=self.bot,app=app,idapp=id,message=message), content=None)



class appPremiumView(nextcord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(appPremiumSelect(bot=bot))
        self.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.link, url="https://store.cyber-safe.pro/", label="Contect Me"))
        

class appPremiumCog(commands.Cog):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @nextcord.slash_command(
        name='setapppremium',
        description='📌 | ติดตั้งระบบซื้อแอปพรีเมี่ยม',
        guild_ids=[Config().Get()['serverId']]
    )
    async def apppremium(
        self,
        interaction: nextcord.Interaction
    ):
        if (interaction.user.id not in Config().Get()['ownerIds']):
            return await interaction.response.send_message(content='[ERROR] No Permission For Use This Command.', ephemeral=True)
        embed = nextcord.Embed()
        embed.title = 'BOT App PREMIUM'
        embed.description = '>  บริการขาย App PREMIUM ราคาถูกที่สุดในไทย\n> อ่านรายละเอียดเพิ่มเติมได้ที่ https://store.cyber-safe.pro/storesocial\n\n# กดเลือกสินค้าที่คุณต้องการได้เลย'
        embed.color = nextcord.Color.from_rgb(255, 0, 0)
        embed.set_image(url=Config().Get()["embed"]["imglogo"])
        try:
            await interaction.channel.send(embed=embed, view=appPremiumView(bot=self.bot))
            await interaction.response.send_message(content='[SUCCESS] Done.', ephemeral=True)
        except Exception as error:
            print(error)
            await interaction.response.send_message(content='[ERROR] Fail To Send Message.', ephemeral=True)
def setup(bot: commands.Bot):
    bot.add_cog(appPremiumCog(bot=bot))
    bot.add_view(appPremiumView(bot=bot))
# ส่วนสำคัญเกี่ยวกับบอท ขายแอปพรีเมี่ยม

## Installation
```bash
pip install -r requirements.txt
```
## สามารถสมัครเพื่อเอารหัสมาใส่ได้ที่ [https://store.cyber-safe.pro/](https://store.cyber-safe.pro/)
## ตั้งค่าส่วนต่างๆ
```json
{
    "botToken": "token โทเคนบอทของเราจากดิสคอร์ด",
    "commnadPrefix": "!",
    "serverId": "ไอดีเซิฟเวอร์ของเรา",
    "ownerIds": [
        "ไอดีแอดมินที่จะใช้บอทได้",
		"99999999999999"
    ],
    "channelTopupLog": "ไอดีห้องที่ไว้แจ้งเตือนเมื่อคนเติมเงิน",
    "channelAppLog": "ไอดีห้องที่ไว้แจ้งเตือนให้แอดมินรู้ว่าใครซื้ออะไร",
    "submitChannelId": "ไอดีห้องที่ไว้แจ้งเตือนให้คนอื่นรู้ว่าใครซื้ออะไร",
    "roleAddEnable": false or true ถ้าต้องการให้ยศเขาเมื่อซื้อใส่ให้้ใส่ true,
    "roleAddRoleId": ถ้าใส่trueส่วนนี้จะใส่ไอดียศ,
    "phoneNumber": "เบอร์ที่ไว้รับเงินอังเปา",
    "embed": {
        "imglogo": "โลโก้ไว้โชว์ตอนใช้คำสั่ง"
    },
    "configweb": {
        "username": "ชื่อในเว็บcybersafe",
        "password": "รหัสจากเว็บcybersafe",
        "token": "ส่วนนี้ไม่ต้องแก้ไข",
        "price_percentage": ใส่%ที่จะบวกกำไรเพื่อให้บอทเจนราคา
    }
}

```


## วิธีการตั้งค่าราคา

### ทางเราได้ใส่สินค้าขายดีไว้ให้แล้ว และ บวกกำไรให้ทุกชิ้นชิ้นละ10% ถ้าอยากเพิ่มเติมหรือแก้ไขสามารถทำได้ตามนี้เลย

1 ) ให้รันโปรแกรม getall.py และมันจะสร้างราคาใหม่มาให้
```bash
python getall.py
```
2 ) จะได้ราคาสินค้าที่ขายในเว็บมา ไปเป็นเก็บใน database/allapp.json
## แต่ดิสคอร์ดสามารถรับรองสินค้าเราได้แค่ 25 ชิ้นเท่านั้น

3 ) ให้เอาสินค้าที่จะขายคัดลอกมาใส่ใน database/apps.json ตัวอย่าง
```json
 "61": {
        "id": "61",
        "name": "Netflix 50 วัน <br>( ส่วนตัว TV ) ",
        "msg": "• สามารถดูบน TV ได้ ..  <br> \n• แอคเคาท์ไทย 100%  <br> \n• สามารถรับชมได้ 1 จอ <i class='fa fa-desktop' aria-hidden='true'></i><br> \n• ความละเอียดระดับ <span class='badge badge-dark'>UltraHD 4K</span> <br> \n• สามารถเปลี่ยนชื่อจอ และ PIN จอได้ <br> \n• หากจอชน กดแจ้งปัญหาเลือกหัวข้อจอชนได้เลย ( ระบบแก้ไขอัตโนมัติ ) <br> \n• หากบัญชีถูกปิดจาก Netflix ทางร้านไม่สามารถเคลมได้ <br><br>\n<b><i class='fas fa-info-circle text-danger how'></i> ข้อห้าม !!</b><br>\n❌ ห้ามเปลี่ยนรหัสและเมลเด็ดขาด ฝ่าฝืนปรับ 1,000บาท <br> \n❌ ห้ามดูพร้อมกันเกิน1เครื่อง หากพบเจอปรับ 300 บาท<br> ",
        "exp": 50,
        "price": "349",
        "new_price": 383.9
    },
```

ให้เอาส่วนนี้ไปใส่
### ราคาสามารถแก้ไขเพิ่มเติมจากส่วนนี้ได้


## วิธีการทำงาน
```bash
python main.py
```

# หากมีปัญหาติดต่อช่องทางได้ตามนี้

FB : [cybersafe](https://fb.me/cybersafe01)

DISCORD : [cybersafe](https://cyber-safe.pro/discord)

WEB : [cybersafe](https://cyber-safe.pro)


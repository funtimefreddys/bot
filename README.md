


<img width="1920" height="1080" alt="Screenshot (282)" src="https://github.com/user-attachments/assets/03e4fed4-8c4c-4850-a950-fbf99c4fadd9"/>






# 🤖 GuskungBot - Discord Bot

บอท Discord สำหรับความปลอดภัย พร้อมระบบตรวจจับ spam และตรวจสอบโปรไฟล์

## ✨ ฟีเจอร์

- ✅ **ระบบ Slash Commands** - คำสั่งแบบ `/` ที่ทันสมัย
- ✅ **ระบบตรวจจับ Spam** - ตรวจจับ spam แบบอัตโนมัติ
- ✅ **ระบบเตะอัตโนมัติ** - เตะผู้ใช้ที่ไม่ตั้งโปรไฟล์ออกอัตโนมัติ
- ✅ **ระบบ Rate Limiting** - ป้องกันการใช้งานคำสั่งมากเกินไป
- ✅ **ระบบ Permission Checks** - ตรวจสอบสิทธิ์ผู้ใช้
- ✅ **ระบบ Logging** - บันทึกการกระทำที่สำคัญ

## 📋 คำสั่ง

- `/hello [name]` - ทักทายบอท
- `/ping` - ตรวจสอบ latency
- `/clear [amount]` - ลบข้อความ
- `/help` - แสดงคำสั่งทั้งหมด
- `/sync` - Sync slash commands (ผู้ดูแลระบบ)
- `/autokick` - ตั้งค่าระบบเตะอัตโนมัติ (ผู้ดูแลระบบ)
- `/kickprofile [user]` - เตะผู้ใช้ที่ไม่ตั้งโปรไฟล์ (ผู้ดูแลระบบ)
- `/checkprofile [user]` - ตรวจสอบผู้ใช้ที่ไม่ตั้งโปรไฟล์

## 🚀 Installation

### 🪟 Windows

#### Option 1: All in One (Easiest) ⭐⭐⭐

**รันไฟล์เดียวได้ทุกอย่าง!**

1. Run `all_in_one.bat` - เปิดเมนูรวมทุกอย่าง
2. เลือก `[2] Setup` - ติดตั้ง dependencies
3. เลือก `[1] Run Bot` - รันบอท
4. ป้อน `DISCORD_TOKEN` เมื่อถูกถาม

**หรือเลือก `[3] Build EXE` เพื่อสร้างไฟล์ EXE**

#### Option 2: Command Line

```cmd
pip install -r requirements.txt
# Edit .env file and add DISCORD_TOKEN
python main.py
```

## 📦 สร้างไฟล์ EXE

### วิธีที่ 1: ใช้ all_in_one.bat (ง่ายที่สุด) ⭐
1. รัน `all_in_one.bat`
2. เลือก `[3] 🔨 Build EXE / สร้างไฟล์ EXE`
3. รอให้ build เสร็จ (ใช้เวลาประมาณ 2-5 นาที)
4. ไฟล์ EXE จะอยู่ที่ `dist\GuskungBot.exe`

### หลังจากสร้าง EXE แล้ว:
1. ไปที่โฟลเดอร์ `dist`
2. แก้ไข `.env` และเพิ่ม `DISCORD_TOKEN`
3. รัน `GuskungBot.exe`

**หมายเหตุ:** 
- EXE เป็น standalone **ไม่ต้องติดตั้ง Python**
- สามารถแจกจ่ายโฟลเดอร์ `dist` ให้ผู้อื่นได้เลย
- ไฟล์ `.env` จะถูกคัดลอกไปที่โฟลเดอร์ `dist` อัตโนมัติ

## ⚙️ การตั้งค่า

### ตั้งค่าระบบเตะอัตโนมัติ

```
/autokick enabled:True min_account_age:7 require_avatar:True log_channel:#channel
```

### ปิดการเตะอัตโนมัติ

```
/autokick enabled:False
```

## 🔒 ความปลอดภัย

- ไฟล์ `.env` ไม่ถูก commit ขึ้น Git (ตาม `.gitignore`)
- Token ไม่ถูก hardcode ในโค้ด
- ระบบ Rate Limiting ป้องกัน abuse
- ระบบ Permission Checks ตรวจสอบสิทธิ์

## 📝 หมายเหตุ

- บอทต้องมีสิทธิ์ "Kick Members" เพื่อใช้ฟีเจอร์เตะ
- Slash commands ต้อง sync ก่อนใช้งาน (ใช้เวลาประมาณ 1-5 นาที)
- ไฟล์ `.env` ต้องอยู่ในโฟลเดอร์เดียวกับไฟล์ที่รัน

## 🐛 การแก้ปัญหา

### บอทรันไม่ออก
- ตรวจสอบว่า Python ติดตั้งแล้ว
- ตรวจสอบว่าไฟล์ `.env` มี DISCORD_TOKEN
- ตรวจสอบว่า Token ถูกต้อง

### Slash commands ไม่ปรากฏ
- รอ 1-5 นาที ให้ Discord sync commands
- ใช้คำสั่ง `/sync` เพื่อ sync อีกครั้ง
- รีโหลด Discord (Ctrl+R)

### ไม่สามารถเตะสมาชิกได้
- ตรวจสอบว่าบอทมีสิทธิ์ "Kick Members"
- ตรวจสอบว่าผู้ใช้ไม่ใช่ admin หรือ owner

## 📄 License

MIT License

# อาจจะมีมาเรื่อยๆนะครับ มีบัคบ้างสามารถนำไปเเก้ไขรึดัด เเปลงได้ ให้เครคิตด้วยนะครับ 
## ห้ามนำไฟล์ไปขายเอากำไรเด็ดขาด 

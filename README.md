# 🦁☀️ پرچم شیر و خورشید برای ایموجی 🇮🇷

پیش‌نیازها

- فونت `Noto Color Emoji` نسخه‌ی **CBDT** (مثلاً `2.047` در Ubuntu 24.04)
- Python 3 به‌همراه `fonttools` و `pillow`
- فایل تصویر پرچم: `iran_flag_emoji.png` (PNG شفاف)

## نصب

### ۱. تولید `evdev.xml` با پرچم‌ها (gnome-language-flags)

```bash
python3 glyphs2flags.py
```

از فایل اصلی بکاپ بگیر:

```bash
sudo cp /usr/share/X11/xkb/rules/evdev.xml \
        /usr/share/X11/xkb/rules/evdev.xml.bak
```

فایل ساخته‌شده را جایگزین کن:

```bash
sudo cp evdev.xml /usr/share/X11/xkb/rules/evdev.xml
```

### ۲. ساخت و نصب فونت پچ‌شده

```bash
pip install -r requirements.txt  
python3 patch_iran_flag.py iran_flag_emoji.png

mkdir -p ~/.local/share/fonts
cp NotoColorEmojiLionSun.ttf ~/.local/share/fonts/
```

### ۳. اولویت دادن به فونت جدید

این محتوا را در `~/.config/fontconfig/fonts.conf` قرار بده:

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <alias binding="same">
    <family>emoji</family>
    <prefer><family>Noto Color Emoji LionSun</family></prefer>
  </alias>
</fontconfig>
```

سپس:

```bash
fc-cache -f
```

### ۴. اعمال تغییرات

GNOME Shell را ری‌استارت کن:

```bash
killall -SIGQUIT gnome-shell
```

یا ساده‌تر سیستم را ریبوت کن:

```bash
sudo reboot
```

> ⚠️ `killall -SIGQUIT gnome-shell` روی **Wayland** احتمالاً کل سشن را می‌بندد، پس قبلش کارهایت را ذخیره کن. روی Wayland لاگ‌اوت/لاگین یا ریبوت مطمئن‌تر است. روی **X11** می‌توانی از `Alt+F2` سپس `r` هم استفاده کنی.

## بررسی و عیب‌یابی

- **فونت در مسیر دیگری است (مثلاً Arch):** مقدار `SRC` بالای `patch_iran_flag.py` را عوض کن، مثلاً `/usr/share/fonts/noto/NotoColorEmoji.ttf`.
- **فونت CBDT نیست (COLRv1 است):** اسکریپت کار نمی‌کند. بررسی:

  ```bash
  python3 -c "from fontTools.ttLib import TTFont; print(TTFont('/path/to/NotoColorEmoji.ttf').keys())"
  ```

  باید `CBDT` و `CBLC` در خروجی باشند.
- **هنوز پرچم قدیمی نمایش داده می‌شود:**

  ```bash
  fc-match "emoji"
  ```

  باید `Noto Color Emoji LionSun` را نشان بدهد.
- **بعد از آپدیت پکیج فونت:** فونت اصلی تغییر می‌کند ولی نسخه‌ی پچ‌شده نه. اسکریپت را دوباره اجرا کن.

## برگرداندن به حالت اول

```bash
rm ~/.local/share/fonts/NotoColorEmojiLionSun.ttf
rm ~/.config/fontconfig/fonts.conf   # اگر فایل دیگری در آن نداری
sudo cp /usr/share/X11/xkb/rules/evdev.xml.bak /usr/share/X11/xkb/rules/evdev.xml
fc-cache -f
```

و GNOME را ریستارت کن (مطابق مرحله‌ی ۴).

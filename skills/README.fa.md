# مهارت‌های عامل NetBox

مهارت‌های وظیفه‌محور دوزبانه (انگلیسی/فارسی) برای Brain Bot (NanoCortex) جهت پرس‌وجو از NetBox از طریق netbox-mcp.

## مهارت‌ها

| مهارت | انگلیسی | فارسی | توضیحات |
|-------|---------|---------|----------|
| جستجوی دستگاه | [SKILL.md](netbox-device-lookup/SKILL.md) | [SKILL.fa.md](netbox-device-lookup/SKILL.fa.md) | یافتن دستگاه بر اساس نام، سریال یا IP |
| موجودی رک | [SKILL.md](netbox-rack-inventory/SKILL.md) | [SKILL.fa.md](netbox-rack-inventory/SKILL.fa.md) | فهرست دستگاه‌های یک رک همراه با موقعیت U |
| جستجوی IP | [SKILL.md](netbox-ip-lookup/SKILL.md) | [SKILL.fa.md](netbox-ip-lookup/SKILL.fa.md) | تطبیق IP با دستگاه، اینترفیس و prefix |
| جزئیات اینترفیس | [SKILL.md](netbox-interface-details/SKILL.md) | [SKILL.fa.md](netbox-interface-details/SKILL.fa.md) | نمایش اینترفیس‌ها و IPهای یک دستگاه |
| بررسی توان | [SKILL.md](netbox-power-check/SKILL.md) | [SKILL.fa.md](netbox-power-check/SKILL.fa.md) | مصرف برق دستگاه یا ظرفیت توان رک |
| جستجوی دستگاه‌ها | [SKILL.md](netbox-search-devices/SKILL.md) | [SKILL.fa.md](netbox-search-devices/SKILL.fa.md) | جستجوی دستگاه‌ها بر اساس زیررشته |
| عیب‌یابی کابل‌کشی | [SKILL.md](netbox-troubleshoot-cabling/SKILL.md) | [SKILL.fa.md](netbox-troubleshoot-cabling/SKILL.fa.md) | ردیابی کابل‌کشی بین دستگاه‌ها |

## نحوه استفاده

- **عامل‌های Superpowers:** فایل `SKILL.md` مربوط به وظیفه را بارگذاری کنید.
- **Brain Bot (NanoCortex):** از پرامپت کامپایل‌شده در `nanocortex/netbox-prompt.md` (انگلیسی) یا `nanocortex/netbox-prompt.fa.md` (فارسی) استفاده کنید.

## قاعده زبان

Brain Bot به زبان کاربر پاسخ می‌دهد: پرسش فارسی ← پاسخ فارسی، پرسش انگلیسی ← پاسخ انگلیسی.

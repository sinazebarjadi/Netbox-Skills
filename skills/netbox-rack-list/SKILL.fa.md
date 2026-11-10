---
name: netbox-rack-list
description: List all racks, optionally filtered by site
tools: [netbox_list_racks]
---

## ابزارهای ترکیبی را ترجیح دهید

برای پرسش‌های پیچیده، به‌جای زنجیره‌کردن ابزارها، از ابزار ترکیبی استفاده کنید:
- "همه اطلاعات رک" → `netbox_rack_full` (نه `netbox_rack_inventory` + `netbox_list_cables`)
- "همه اطلاعات سایت همراه با رک‌ها" → `netbox_site_full` (نه `netbox_site_detail` + `netbox_list_racks`)

از ابزار ساده زیر فقط برای جست‌وجوی سریع یک نکته مشخص استفاده کنید.

# فهرست رک‌ها در NetBox

## زمان استفاده

- "List all racks"
- "What racks are in DC-Primary?"
- "Show me all racks at SiteA"
- "همه رک‌ها رو لیست کن"
- "رک‌های سایت تهران رو نشون بده"

## نحوه حل

۱. ابزار `netbox_list_racks` را با فیلتر اختیاری سایت فراخوانی کنید.
۲. نتیجه را به صورت جدول نمایش دهید.

## نحوه نمایش

```
| Name | Site | U Height | Devices |
|------|------|----------|---------|
| R16 | DC-Primary | 42U | 12 |
| R17 | DC-Primary | 42U | 8 |
| R01 | DC-Secondary | 48U | 20 |
```

## موارد خاص

- **هیچ رکی وجود ندارد:** «هیچ رکی مطابق با معیارهای شما یافت نشد.»
- **سایت یافت نشد:** «سایت 'X' یافت نشد.»

## مثال‌ها

**ورودی:** "List all racks"
**فراخوانی ابزار:** `netbox_list_racks()`
**خروجی:** جدول رک‌ها.

**ورودی:** "Racks in DC-Primary"
**فراخوانی ابزار:** `netbox_list_racks(site="DC-Primary")`
**خروجی:** جدول رک‌های فیلترشده بر اساس سایت.

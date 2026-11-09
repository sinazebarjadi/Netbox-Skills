---
name: netbox-rack-list
description: List all racks, optionally filtered by site
tools: [netbox_list_racks]
---

# فهرست رک‌ها در NetBox

## زمان استفاده

- "List all racks"
- "What racks are in Tehran-DC1?"
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
| R16 | Tehran-DC1 | 42U | 12 |
| R17 | Tehran-DC1 | 42U | 8 |
| R01 | Isfahan-DC1 | 48U | 20 |
```

## موارد خاص

- **هیچ رکی وجود ندارد:** «هیچ رکی مطابق با معیارهای شما یافت نشد.»
- **سایت یافت نشد:** «سایت 'X' یافت نشد.»

## مثال‌ها

**ورودی:** "List all racks"
**فراخوانی ابزار:** `netbox_list_racks()`
**خروجی:** جدول رک‌ها.

**ورودی:** "Racks in Tehran-DC1"
**فراخوانی ابزار:** `netbox_list_racks(site="Tehran-DC1")`
**خروجی:** جدول رک‌های فیلترشده بر اساس سایت.

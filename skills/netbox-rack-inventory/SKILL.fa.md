---
name: netbox-rack-inventory
description: List all devices in a rack with U positions and power feed information
tools: [netbox_rack_inventory, netbox_get_device]
---

# موجودی رک در NetBox

## چه زمانی استفاده شود

- "What's in rack R16?"
- "Show me rack R16 at SiteA"
- "List devices in rack R16"
- "رک R16 چی توشه؟"
- "دستگاه‌های رک R16 رو لیست کن"

## نحوه شناسایی

۱. ابزار `netbox_rack_inventory` را با نام رک و در صورت نیاز سایت فراخوانی کن.
۲. اگر رک یافت نشد، به کاربر پیشنهاد بده نام رک یا سایت را بررسی کند.
۳. فهرست دستگاه‌ها را بر اساس موقعیت U مرتب‌شده نمایش بده.

## نحوه نمایش

```
**Rack:** R16 (Site: DC-Primary, Height: 42U)
**Power Feed:** PDU-A (240V, 30A, max 80% utilization)

| U | Device | Model | Serial | Role |
|---|--------|-------|--------|------|
| 10 | SRV-01 | R750 | ABC123 | Server |
| 12 | SW-01 | C3850 | DEF456 | Switch |
```

## موارد خاص

- **رک یافت نشد:** «رک 'X' یافت نشد. نام و سایت را بررسی کنید.»
- **رک خالی:** «رک 'X' خالی است.»
- **خطای ابزار:** «خطا در پرس‌وجوی NetBox: [error].»

## مثال‌ها

**ورودی:** "What's in rack R16?"
**فراخوانی ابزار:** `netbox_rack_inventory("R16")`
**خروجی:** خلاصه رک + جدول دستگاه‌ها.

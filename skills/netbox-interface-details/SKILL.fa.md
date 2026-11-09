---
name: netbox-interface-details
description: Show all interfaces of a device with their assigned IP addresses
tools: [netbox_interface_info]
---

# جزئیات اینترفیس‌ها در NetBox

## چه زمانی استفاده شود

- "Show interfaces on SW-01"
- "What interfaces does SRV-01 have?"
- "IPs on Gi1/0/1"
- "اینترفیس‌های SW-01 رو نشون بده"
- "اینترفیس Gi1/0/1 چه IP هایی داره؟"

## نحوه دریافت اطلاعات

۱. ابزار `netbox_interface_info` را با نام دستگاه فراخوانی کن.
۲. اگر کاربر یک اینترفیس مشخص خواسته بود، آن را فیلتر یا برجسته کن.
۳. نتیجه را به‌صورت جدول نمایش بده.

## نحوه نمایش

```
**Device:** SW-01

| Interface | Type | Mode | MAC | IPs |
|-----------|------|------|-----|-----|
| Gi1/0/1 | 1000BASE-T | access | aa:bb:cc:dd:ee:ff | 10.0.1.1/24 |
| Gi1/0/2 | 1000BASE-T | trunk | aa:bb:cc:dd:ee:ff | — |
```

## موارد خاص

- **دستگاه یافت نشد:** «دستگاه 'X' یافت نشد.»
- **بدون اینترفیس:** «دستگاه 'X' هیچ اینترفیسی در NetBox ندارد.»
- **اینترفیس یافت نشد:** «اینترفیس 'Y' روی دستگاه 'X' یافت نشد.»

## مثال‌ها

**ورودی:** "Show interfaces on SW-01"
**فراخوانی ابزار:** `netbox_interface_info("SW-01")`
**خروجی:** جدول اینترفیس‌ها.

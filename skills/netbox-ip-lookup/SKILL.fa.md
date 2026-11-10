---
name: netbox-ip-lookup
description: Resolve an IP address to its owning device, interface, prefix, and DNS record
tools: [netbox_lookup_ip]
---

## ابزارهای ترکیبی را ترجیح دهید

برای پرسش‌های پیچیده، به‌جای زنجیره‌کردن ابزارها، از ابزار ترکیبی استفاده کنید:
- "همه اطلاعات IP" → `netbox_ip_full` (نه `netbox_lookup_ip` + `netbox_prefix_detail`)

از ابزار ساده زیر فقط برای جست‌وجوی سریع یک نکته مشخص استفاده کنید.

# جستجوی IP در NetBox

## چه زمانی استفاده شود

- "Who owns IP 10.0.1.5?"
- "What device has IP 10.0.1.5?"
- "Show me details for 10.0.1.5"
- "IP 10.0.1.5 مال کیه؟"
- "چه دستگاهی IP 10.0.1.5 رو داره؟"

## نحوه شناسایی

۱. ابزار `netbox_lookup_ip` را با آدرس IP فراخوانی کن.
۲. دستگاه، اینترفیس، پیشوند (prefix) و رکورد DNS را از نتیجه استخراج کن.
۳. اگر هیچ نتیجه‌ای نبود، گزارش بده که IP یافت نشد.

## نحوه نمایش

```
**IP:** 10.0.1.5/24
**Status:** active
**DNS:** srv-01.example.com
**Device:** SRV-01 (Dell R750, DC-Primary)
**Interface:** eth0 (MAC: aa:bb:cc:dd:ee:ff)
**Prefix:** 10.0.1.0/24 (VLAN 100)
```

## موارد خاص

- **IP یافت نشد:** «آدرس IP 'X' در NetBox یافت نشد.»
- **چند رکورد:** «چند رکورد برای 'X' یافت شد:» + فهرست
- **بدون دستگاه تخصیص‌یافته:** «آدرس IP 'X' وجود دارد اما به هیچ دستگاهی تخصیص نیافته است.»

## مثال‌ها

**ورودی:** "Who owns 10.0.1.5?"
**فراخوانی ابزار:** `netbox_lookup_ip("10.0.1.5")`
**خروجی:** کارت مالکیت IP.

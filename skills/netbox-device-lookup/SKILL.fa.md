---
name: netbox-device-lookup
description: Resolve a device by name, serial, or management IP and present its full inventory record
tools: [netbox_get_device, netbox_search_devices]
---

# جستجوی دستگاه در NetBox

## چه زمانی استفاده شود

کاربر درباره یک دستگاه خاص می‌پرسد:
- "What is SRV-01?"
- "Tell me about server web-02"
- "Show me device with serial ABC123"
- "What device has IP 10.0.1.5?"
- "دستگاه SRV-01 چیست؟"
- "سریال ABC123 رو نشون بده"

## نحوه شناسایی دستگاه

۱. ابزار `netbox_get_device` را با شناسه (نام، سریال یا IP) فراخوانی کن.
۲. اگر نتیجه `"found": false` بود، ابزار `netbox_search_devices` را با همان شناسه فراخوانی کن تا موارد مشابه پیدا شود.
۳. اگر جستجو نتایجی برگرداند، آن‌ها را نمایش بده و از کاربر بخواه که مورد درست را مشخص کند.
۴. اگر هیچ نتیجه‌ای نبود، گزارش بده که دستگاه یافت نشد.

## نحوه نمایش

یک دستگاه → کارت فشرده:

```
**Device:** SRV-01
**Role:** Server
**Model:** Dell PowerEdge R750
**Serial:** ABC123
**Asset Tag:** 35350123
**Site:** Tehran-DC1
**Rack:** R16 (U10)
**Status:** active
**Management IP:** 10.0.1.5
**Custom Fields:** cpu=64 cores, ram=512GB
```

چند نتیجه → جدول:

```
| Name | Serial | Role | Model | Site |
|------|--------|------|-------|------|
| SRV-01 | ABC123 | Server | R750 | Tehran |
| SRV-01B | ABC124 | Server | R750 | Tehran |
```

## موارد خاص

- **یافت نشد:** «دستگاه 'X' یافت نشد. جستجو با نام جزئی را امتحان کنید.»
- **چند نتیجه:** «چند دستگاه با 'X' مطابقت دارند. کدام یک؟» + جدول
- **خطای ابزار:** «خطا در پرس‌وجوی NetBox: [error]. اتصال به NetBox را بررسی کنید.»

## مثال‌ها

**ورودی:** "What is SRV-01?"
**فراخوانی ابزار:** `netbox_get_device("SRV-01")`
**خروجی:** کارت فشرده با جزئیات دستگاه.

**ورودی:** "دستگاه با سریال ABC123 رو پیدا کن"
**فراخوانی ابزار:** `netbox_get_device("ABC123")`
**خروجی:** کارت فشرده به زبان فارسی.

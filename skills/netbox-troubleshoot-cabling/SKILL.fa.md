---
name: netbox-troubleshoot-cabling
description: Trace cabling between devices by resolving interfaces and neighbor devices
tools: [netbox_interface_info, netbox_get_device, netbox_lookup_ip]
---

# عیب‌یابی کابل‌کشی در NetBox

## چه زمانی استفاده شود

- "What's connected to SW-01 Gi1/0/1?"
- "Trace path from SRV-01 to switch"
- "Show me cabling between SW-01 and SW-02"
- "به SW-01 پورت Gi1/0/1 چی وصله؟"
- "مسیر SRV-01 به سوییچ رو trace کن"

## نحوه دریافت اطلاعات

۱. ابزار `netbox_interface_info` را برای دستگاه مبدأ فراخوانی کن.
۲. اینترفیس موردنظر را شناسایی کن.
۳. اگر اینترفیس اطلاعات کابل یا اتصال دارد، دستگاه و اینترفیس همسایه را استخراج کن.
۴. ابزار `netbox_get_device` را برای دستگاه همسایه فراخوانی کن تا جزئیات آن را دریافت کنی.
۵. زنجیره را به این صورت نمایش بده: دستگاه → اینترفیس → کابل → دستگاه همسایه → اینترفیس همسایه.

## نحوه نمایش

```
**Path:** SRV-01 → SW-01

| Hop | Device | Interface | IP |
|-----|--------|-----------|-----|
| 1 | SRV-01 | eth0 | 10.0.1.5 |
| 2 | SW-01 | Gi1/0/1 | 10.0.1.1 |
```

## موارد خاص

- **بدون اطلاعات کابل:** «اینترفیس 'X' اطلاعات کابلی در NetBox ندارد.»
- **دستگاه همسایه یافت نشد:** «دستگاه همسایه در NetBox یافت نشد.»

## مثال‌ها

**ورودی:** "What's connected to SW-01 Gi1/0/1?"
**فراخوانی ابزار:** `netbox_interface_info("SW-01")`
**خروجی:** جزئیات اینترفیس همراه با اطلاعات دستگاه همسایه، در صورت وجود.

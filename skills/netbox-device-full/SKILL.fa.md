---
name: netbox-device-full
description: دریافت اطلاعات کامل دستگاه شامل اینترفیس‌ها، کابل‌ها و برق در یک فراخوانی
tools: [netbox_device_full]
---

# اطلاعات کامل دستگاه NetBox

## زمان استفاده

کاربر اطلاعات کامل یک دستگاه را درخواست می‌کند:
- "Tell me everything about SRV-01"
- "Full details of device X"
- "Show me all information about server Y"
- "همه اطلاعات SRV-01 رو بده"
- "جزئیات کامل دستگاه X رو نشون بده"

## نحوه اجرا

1. ابزار `netbox_device_full` را با شناسه دستگاه فراخوانی کنید.
2. کارت دستگاه + جدول اینترفیس‌ها + فهرست کابل‌ها + خلاصه برق را نمایش دهید.

## نحوه نمایش

```
**Device:** SRV-01
**Role:** Server
**Model:** Dell R750
**Serial:** ABC123
**Site:** DC-Primary
**Rack:** R16 (U10)
**Status:** active
**Management IP:** 10.0.1.5

**Interfaces (3):**
| Name | Type | Mode | MAC | IPs |
|------|------|------|-----|-----|
| eth0 | 1000BASE-T | access | aa:bb:cc:dd:ee:ff | 10.0.1.5/24 |
| eth1 | 1000BASE-T | trunk | aa:bb:cc:dd:ee:00 | — |

**Cables (2):**
| Local | Remote | Type |
|-------|--------|------|
| eth0 | SW-01:Gi1/0/1 | Cat6 |
| eth1 | SW-01:Gi1/0/2 | Cat6 |

**Power:**
| PSU | Allocated | Max |
|-----|-----------|-----|
| PSU1 | 450W | 750W |
| Feed: PDU-A (240V, 30A, max 80%) |
```

## موارد خاص

- **پیدا نشد:** "دستگاه 'X' پیدا نشد. برای جستجوی جزئی از netbox_search_devices استفاده کنید."
- **بدون کابل:** "اطلاعات کابلی برای دستگاه 'X' وجود ندارد."
- **بدون اطلاعات برق:** "اطلاعات برقی برای دستگاه 'X' وجود ندارد."

## مثال‌ها

**ورودی:** "همه اطلاعات SRV-01 رو بده"
**فراخوانی ابزار:** `netbox_device_full("SRV-01")`
**خروجی:** کارت کامل دستگاه + اینترفیس‌ها + کابل‌ها + برق.

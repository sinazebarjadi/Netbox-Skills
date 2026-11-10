---
name: netbox-site-full
description: دریافت اطلاعات کامل سایت شامل رک‌ها، دستگاه‌ها، پیشوندها و VLANها در یک فراخوانی
tools: [netbox_site_full]
---

# اطلاعات کامل سایت در NetBox

## زمان استفاده

- "Everything about site X"
- "Full site overview for DC-Primary"
- "Show me complete information about this site"
- "همه اطلاعات سایت X رو بده"
- "نمای کامل سایت X رو نشون بده"

## نحوه اجرا

1. ابزار `netbox_site_full` را با نام سایت فراخوانی کنید.
2. کارت سایت + لیست رک‌ها + تعداد دستگاه‌ها + جدول پیشوندها + جدول VLANها را نمایش دهید.

## نحوه نمایش

```
**Site:** DC-Primary
**Status:** active
**Region:** City-A

**Racks (5):**
| Name | U Height | Devices |
|------|----------|---------|
| R16 | 42U | 12 |
| R17 | 42U | 8 |

**Total Devices:** 42

**Prefixes (10):**
| Prefix | VRF | VLAN | Description |
|--------|-----|------|-------------|
| 10.0.1.0/24 | default | 100 | Servers |
| 10.0.2.0/24 | default | 200 | Management |

**VLANs (5):**
| VID | Name | Status |
|-----|------|--------|
| 100 | Servers | active |
| 200 | Management | active |
```

## موارد خاص

- **سایت پیدا نشد:** "سایت 'X' پیدا نشد."
- **بدون رک:** "سایت 'X' هیچ رکی ندارد."

## مثال‌ها

**ورودی:** "همه اطلاعات DC-Primary رو بده"
**فراخوانی ابزار:** `netbox_site_full("DC-Primary")`
**خروجی:** اطلاعات کامل سایت.

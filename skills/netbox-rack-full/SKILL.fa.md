---
name: netbox-rack-full
description: دریافت اطلاعات کامل رک شامل دستگاه‌ها، فیدهای برق و کابل‌ها در یک فراخوانی
tools: [netbox_rack_full]
---

# اطلاعات کامل رک NetBox

## زمان استفاده

- "Everything in rack R16"
- "Full rack inventory for R16"
- "Show me all devices and cables in rack R16"
- "همه چیز رک R16 رو بده"
- "موجودی کامل رک R16 رو نشون بده"

## نحوه اجرا

1. ابزار `netbox_rack_full` را با نام رک و سایت اختیاری فراخوانی کنید.
2. خلاصه رک + جدول دستگاه‌ها + فیدهای برق + فهرست کابل‌ها را نمایش دهید.

## نحوه نمایش

```
**Rack:** R16 (Site: DC-Primary, Height: 42U)

**Power Feeds:**
| Name | Voltage | Amperage | Max Utilization |
|------|---------|----------|-----------------|
| PDU-A | 240V | 30A | 80% |

**Devices (12):**
| U | Device | Model | Serial | Role |
|---|--------|-------|--------|------|
| 10 | SRV-01 | R750 | ABC123 | Server |
| 12 | SW-01 | C3850 | DEF456 | Switch |

**Cables (8):**
| A-End | B-End | Type | Status |
|-------|-------|------|--------|
| SRV-01:eth0 | SW-01:Gi1/0/1 | Cat6 | connected |
```

## موارد خاص

- **رک پیدا نشد:** "رک 'X' پیدا نشد. نام و سایت را بررسی کنید."
- **رک خالی:** "رک 'X' خالی است."

## مثال‌ها

**ورودی:** "همه چیز رک R16 رو بده"
**فراخوانی ابزار:** `netbox_rack_full("R16")`
**خروجی:** خلاصه رک + دستگاه‌ها + برق + کابل‌ها.

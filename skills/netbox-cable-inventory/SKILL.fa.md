---
name: netbox-cable-inventory
description: List cables and trace connections between device interfaces
tools: [netbox_list_cables, netbox_trace_cable]
---

# فهرست کابل‌های NetBox

## چه زمانی استفاده شود

- "Show me all cables in rack R16"
- "List cables for device SW-01"
- "Trace cable from SW-01 Gi1/0/1"
- "What's connected to SW-01 Gi1/0/1?"
- "کابل‌های رک R16 رو نشون بده"
- "کابل از SW-01 پورت Gi1/0/1 رو trace کن"

## نحوه دریافت اطلاعات

برای فهرست کردن کابل‌ها:
۱. ابزار `netbox_list_cables` را با فیلترهای اختیاری رک، دستگاه یا سایت فراخوانی کن.
۲. نتیجه را به‌صورت جدول نمایش بده.

برای ردیابی یک کابل:
۱. ابزار `netbox_trace_cable` را با دستگاه و اینترفیس فراخوانی کن.
۲. زنجیره اینترفیس → کابل → همسایه را نمایش بده.

## نحوه نمایش

فهرست کابل‌ها:
```
| Cable | A-End | B-End | Type | Status |
|-------|-------|-------|------|--------|
| #101 | SW-01:Gi1/0/1 | SRV-01:eth0 | Cat6 | connected |
| #102 | SW-01:Gi1/0/2 | SRV-02:eth0 | Cat6 | connected |
```

ردیابی کابل:
```
**Source:** SW-01 Gi1/0/1
**Cable:** #101 (Cat6)
**Neighbor:** SRV-01 eth0
```

## موارد خاص

- **بدون کابل:** «هیچ کابلی مطابق با معیارهای شما یافت نشد.»
- **اینترفیس یافت نشد:** «اینترفیس 'X' روی دستگاه 'Y' یافت نشد.»
- **بدون کابل روی اینترفیس:** «هیچ کابلی به 'X' روی 'Y' متصل نیست.»

## مثال‌ها

**ورودی:** "Cables in rack R16"
**فراخوانی ابزار:** `netbox_list_cables(rack="R16")`
**خروجی:** جدول کابل‌ها.

**ورودی:** "Trace cable from SW-01 Gi1/0/1"
**فراخوانی ابزار:** `netbox_trace_cable("SW-01", "Gi1/0/1")`
**خروجی:** زنجیره ردیابی کابل.

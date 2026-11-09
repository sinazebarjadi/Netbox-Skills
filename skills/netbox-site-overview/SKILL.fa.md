---
name: netbox-site-overview
description: List all sites and show detailed site information including racks and devices
tools: [netbox_list_sites, netbox_site_detail]
---

# نمای کلی سایت در NetBox

## زمان استفاده

- "List all sites"
- "What sites do we have?"
- "Show me details for Tehran-DC1"
- "How many racks in SiteA?"
- "همه سایت‌ها رو لیست کن"
- "خلاصه سایت تهران رو نشون بده"

## نحوه حل

برای فهرست‌کردن سایت‌ها:
۱. ابزار `netbox_list_sites` را فراخوانی کنید.
۲. نتیجه را به صورت جدول نمایش دهید.

برای جزئیات سایت:
۱. ابزار `netbox_site_detail` را با نام سایت فراخوانی کنید.
۲. اطلاعات سایت + تعداد رک‌ها + تعداد دستگاه‌ها + فهرست رک‌ها را نمایش دهید.

## نحوه نمایش

فهرست سایت‌ها:
```
| Name | Status | Region |
|------|--------|--------|
| Tehran-DC1 | active | Tehran |
| Isfahan-DC1 | active | Isfahan |
```

جزئیات سایت:
```
**Site:** Tehran-DC1
**Status:** active
**Region:** Tehran
**Racks:** 5
**Devices:** 42

**Racks:**
| Name | U Height | Devices |
|------|----------|---------|
| R16 | 42U | 12 |
| R17 | 42U | 8 |
```

## موارد خاص

- **سایت یافت نشد:** «سایت 'X' یافت نشد.»
- **هیچ سایتی موجود نیست:** «هیچ سایتی در NetBox یافت نشد.»

## مثال‌ها

**ورودی:** "List all sites"
**فراخوانی ابزار:** `netbox_list_sites()`
**خروجی:** جدول سایت‌ها.

**ورودی:** "Summary of Tehran-DC1"
**فراخوانی ابزار:** `netbox_site_detail("Tehran-DC1")`
**خروجی:** جزئیات سایت + رک‌ها.

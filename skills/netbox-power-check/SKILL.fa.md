---
name: netbox-power-check
description: Check power draw of a device or power capacity of a rack
tools: [netbox_device_power, netbox_rack_inventory]
---

## ابزارهای ترکیبی را ترجیح دهید

برای پرسش‌های پیچیده، به‌جای زنجیره‌کردن ابزارها، از ابزار ترکیبی استفاده کنید:
- "جزئیات کامل دستگاه همراه با توان" → `netbox_device_full` (نه `netbox_get_device` + `netbox_device_power`)
- "همه اطلاعات رک همراه با فیدهای برق" → `netbox_rack_full` (نه `netbox_rack_inventory` + `netbox_list_cables`)

از ابزار ساده زیر فقط برای جست‌وجوی سریع یک نکته مشخص استفاده کنید.

# بررسی توان در NetBox

## چه زمانی استفاده شود

- "Power draw of SRV-01"
- "How much power does SRV-01 use?"
- "Rack R16 power capacity"
- "مصرف برق SRV-01 چقدره؟"
- "ظرفیت برق رک R16 چقدره؟"

## نحوه دریافت اطلاعات

برای مصرف برق دستگاه:
۱. ابزار `netbox_device_power` را با نام دستگاه فراخوانی کن.
۲. مصرف برق PSU و اطلاعات فید رک را نمایش بده.

برای توان رک:
۱. ابزار `netbox_rack_inventory` را با نام رک فراخوانی کن.
۲. اطلاعات فید برق را استخراج کن.
۳. مشخصات فید و میزان استفاده را نمایش بده.

## نحوه نمایش

توان دستگاه:
```
**Device:** SRV-01
**PSU1:** 450W allocated / 750W max
**Rack Feed:** PDU-A (240V, 30A, max 80% = 5.76kW)
```

توان رک:
```
**Rack R16 Power**
**Feed:** PDU-A
**Spec:** 240V, 30A
**Max Utilization:** 80% (5.76kW)
```

## موارد خاص

- **بدون اطلاعات برق:** «اطلاعات برقی برای دستگاه 'X' موجود نیست.»
- **رک یافت نشد:** «رک 'X' یافت نشد.»

## مثال‌ها

**ورودی:** "Power draw of SRV-01"
**فراخوانی ابزار:** `netbox_device_power("SRV-01")`
**خروجی:** مصرف برق PSU + اطلاعات فید.

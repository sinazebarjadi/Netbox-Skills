---
name: netbox-ip-full
description: دریافت اطلاعات کامل IP شامل دستگاه، اینترفیس، پیشوند، VLAN و VRF در یک فراخوانی
tools: [netbox_ip_full]
---

# اطلاعات کامل IP در NetBox

## زمان استفاده

- "Everything about IP 10.0.1.5"
- "Full details for 10.0.1.5"
- "Show me complete information about this IP"
- "همه اطلاعات IP 10.0.1.5 رو بده"
- "جزئیات کامل IP 10.0.1.5 رو نشون بده"

## نحوه اجرا

1. ابزار `netbox_ip_full` را با آدرس IP فراخوانی کنید.
2. کارت IP + دستگاه + اینترفیس + پیشوند + VLAN + VRF را نمایش دهید.

## نحوه نمایش

```
**IP:** 10.0.1.5/24
**Status:** active
**DNS:** srv-01.example.com

**Device:** SRV-01 (Dell R750, DC-Primary)
**Interface:** eth0 (MAC: aa:bb:cc:dd:ee:ff)

**Prefix:** 10.0.1.0/24
**VLAN:** 100 (Servers)
**VRF:** default
**Site:** DC-Primary
```

## موارد خاص

- **IP پیدا نشد:** "آدرس IP 'X' در NetBox پیدا نشد."
- **دستگاهی اختصاص داده نشده:** "آدرس IP 'X' وجود دارد اما به دستگاهی اختصاص داده نشده است."
- **بدون پیشوند:** "آدرس IP 'X' در هیچ پیشوندی در NetBox قرار ندارد."

## مثال‌ها

**ورودی:** "همه اطلاعات IP 10.0.1.5 رو بده"
**فراخوانی ابزار:** `netbox_ip_full("10.0.1.5")`
**خروجی:** اطلاعات کامل IP.

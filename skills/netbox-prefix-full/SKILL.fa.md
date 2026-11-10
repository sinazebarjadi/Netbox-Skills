---
name: netbox-prefix-full
description: دریافت اطلاعات کامل پیشوند شامل VLAN، VRF، IPهای آزاد و پیشوندهای فرزند در یک فراخوانی
tools: [netbox_prefix_full]
---

# اطلاعات کامل پیشوند در NetBox

## زمان استفاده

- "Everything about 10.0.1.0/24"
- "Full prefix details for 10.0.1.0/24"
- "Show me complete information about this subnet"
- "همه اطلاعات 10.0.1.0/24 رو بده"
- "جزئیات کامل ساب‌نت 10.0.1.0/24 رو نشون بده"

## نحوه اجرا

1. ابزار `netbox_prefix_full` را با CIDR فراخوانی کنید.
2. کارت پیشوند + VLAN + VRF + IPهای آزاد + پیشوندهای فرزند را نمایش دهید.

## نحوه نمایش

```
**Prefix:** 10.0.1.0/24
**Status:** active
**Description:** Server subnet

**VLAN:** 100 (Servers)
**VRF:** default
**Site:** DC-Primary

**Available IPs (sample):**
| IP | Status |
|----|--------|
| 10.0.1.50 | available |
| 10.0.1.51 | available |

**Child Prefixes:**
| Prefix | Description |
|--------|-------------|
| 10.0.1.0/26 | Servers-A |
| 10.0.1.64/26 | Servers-B |
```

## موارد خاص

- **پیشوند پیدا نشد:** "پیشوند 'X' در NetBox پیدا نشد."
- **بدون IP آزاد:** "هیچ IP آزادی در پیشوند 'X' وجود ندارد."
- **بدون فرزند:** "هیچ پیشوند فرزندی برای 'X' وجود ندارد."

## مثال‌ها

**ورودی:** "همه اطلاعات 10.0.1.0/24 رو بده"
**فراخوانی ابزار:** `netbox_prefix_full("10.0.1.0/24")`
**خروجی:** اطلاعات کامل پیشوند.

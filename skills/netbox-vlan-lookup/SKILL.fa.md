---
name: netbox-vlan-lookup
description: Look up VLANs by ID or name and show associated prefixes
tools: [netbox_list_vlans, netbox_vlan_detail]
---

# جستجوی VLAN در NetBox

## زمان استفاده

- "VLAN 100 رو نشون بده"
- "چه VLAN هایی در سایت A وجود دارند؟"
- "همه VLAN ها رو لیست کن"
- "VLAN 100 چیست؟"
- "VLAN های سایت A رو نشون بده"

## نحوه حل

برای لیست کردن VLAN ها:
1. ابزار `netbox_list_vlans` را با فیلترهای اختیاری site/vid/q فراخوانی کنید.
2. نتیجه را به صورت جدول نمایش دهید.

برای جزئیات VLAN:
1. ابزار `netbox_vlan_detail` را با VID یا نام فراخوانی کنید.
2. اطلاعات VLAN + پیشوندها را نمایش دهید.

## نحوه نمایش

لیست VLAN ها:
```
| VID | Name | Site | Status |
|-----|------|------|--------|
| 100 | Servers | City-A | active |
| 200 | Management | City-A | active |
```

جزئیات VLAN:
```
**VLAN:** 100 (Servers)
**Site:** DC-Primary
**Status:** active

**Prefixes in this VLAN:**
| Prefix | VRF | Description |
|--------|-----|-------------|
| 10.0.1.0/24 | default | Server subnet |
```

## موارد خاص

- **VLAN یافت نشد:** "VLAN 'X' یافت نشد."
- **هیچ VLAN ای یافت نشد:** "هیچ VLAN ای با معیارهای شما یافت نشد."

## مثال‌ها

**ورودی:** "VLAN 100 رو نشون بده"
**فراخوانی ابزار:** `netbox_vlan_detail("100")`
**خروجی:** جزئیات VLAN + پیشوندها.

---
name: netbox-ipam-prefixes
description: List IPAM prefixes and find available IPs within a prefix
tools: [netbox_list_prefixes, netbox_prefix_detail]
---

## ابزارهای ترکیبی را ترجیح دهید

برای پرسش‌های پیچیده، به‌جای زنجیره‌کردن ابزارها، از ابزار ترکیبی استفاده کنید:
- "همه اطلاعات پیشوند" → `netbox_prefix_full` (نه `netbox_prefix_detail` + `netbox_vlan_detail`)
- "IP‌های خالی در پیشوندها" → `netbox_find_free_ips` (نه `netbox_list_prefixes` + `netbox_prefix_detail`)

از ابزار ساده زیر فقط برای جست‌وجوی سریع یک نکته مشخص استفاده کنید.

# پیشوندهای IPAM در NetBox

## زمان استفاده

- "چه ساب‌نت‌هایی تو سایت A داریم؟"
- "همه پیشوندها رو نشون بده"
- "IP های خالی تو 10.0.1.0/24 رو پیدا کن"
- "پیشوند 10.0.1.0/24 تو کدوم VRF هست؟"
- "What subnets exist at SiteA?"
- "Find free IPs in 10.0.1.0/24"

## نحوه حل

برای لیست کردن پیشوندها:
1. ابزار `netbox_list_prefixes` را با فیلترهای اختیاری site/family/q فراخوانی کنید.
2. نتیجه را به صورت جدول نمایش دهید.

برای جزئیات پیشوند + IP های خالی:
1. ابزار `netbox_prefix_detail` را با CIDR فراخوانی کنید.
2. اطلاعات پیشوند + نمونه IP های خالی را نمایش دهید.

## نحوه نمایش

لیست پیشوندها:
```
| Prefix | VRF | Site | VLAN | Status | Description |
|--------|-----|------|------|--------|-------------|
| 10.0.1.0/24 | default | City-A | 100 | active | Servers |
| 10.0.2.0/24 | default | City-A | 200 | active | Management |
```

جزئیات پیشوند:
```
**Prefix:** 10.0.1.0/24
**VRF:** default
**Site:** DC-Primary
**VLAN:** 100
**Status:** active
**Description:** Server subnet

**Available IPs (sample):**
| IP | Status |
|----|--------|
| 10.0.1.50 | available |
| 10.0.1.51 | available |
```

## موارد خاص

- **هیچ پیشوندی یافت نشد:** "هیچ پیشوندی با معیارهای شما یافت نشد."
- **پیشوند یافت نشد:** "پیشوند 'X' در NetBox یافت نشد."
- **هیچ IP خالی وجود ندارد:** "هیچ IP خالی در پیشوند 'X' وجود ندارد."

## مثال‌ها

**ورودی:** "چه ساب‌نت‌هایی تو سایت A داریم؟"
**فراخوانی ابزار:** `netbox_list_prefixes(site="SiteA")`
**خروجی:** جدول پیشوندها.

**ورودی:** "IP های خالی تو 10.0.1.0/24 رو پیدا کن"
**فراخوانی ابزار:** `netbox_prefix_detail("10.0.1.0/24")`
**خروجی:** جزئیات پیشوند + IP های خالی.

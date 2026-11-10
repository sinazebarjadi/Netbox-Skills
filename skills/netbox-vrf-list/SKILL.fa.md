---
name: netbox-vrf-list
description: List VRFs (Virtual Routing and Forwarding instances) in NetBox
tools: [netbox_list_vrfs]
---

## ابزارهای ترکیبی را ترجیح دهید

برای پرسش‌های پیچیده، به‌جای زنجیره‌کردن ابزارها، از ابزار ترکیبی استفاده کنید:
- "همه اطلاعات IP همراه با VRF" → `netbox_ip_full` (نه `netbox_lookup_ip` + `netbox_prefix_detail`)
- "همه اطلاعات پیشوند همراه با VRF" → `netbox_prefix_full` (نه `netbox_prefix_detail` + `netbox_vlan_detail`)

از ابزار ساده زیر فقط برای جست‌وجوی سریع یک نکته مشخص استفاده کنید.

# فهرست VRF در NetBox

## زمان استفاده

- "List all VRFs"
- "What VRFs exist?"
- "Show me VRF information"
- "VRF ها رو لیست کن"
- "چه VRF هایی داریم؟"

## نحوه حل

۱. ابزار `netbox_list_vrfs` را فراخوانی کنید.
۲. نتیجه را به صورت جدول نمایش دهید.

## نحوه نمایش

```
| Name | RD | Description |
|------|----|-------------|
| default | — | Default VRF |
| management | 65000:100 | Management network |
| production | 65000:200 | Production network |
```

## موارد خاص

- **هیچ VRF موجود نیست:** «هیچ VRF در NetBox یافت نشد.»

## مثال‌ها

**ورودی:** "List all VRFs"
**فراخوانی ابزار:** `netbox_list_vrfs()`
**خروجی:** جدول VRF.

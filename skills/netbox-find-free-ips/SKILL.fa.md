---
name: netbox-find-free-ips
description: یافتن سریع آدرس‌های IP آزاد در پیشوندها
tools: [netbox_find_free_ips]
---

# یافتن IP آزاد در NetBox

## زمان استفاده

- "IP های خالی تو سایت X رو پیدا کن"
- "آدرس‌های آزاد در 10.0.1.0/24 رو نشون بده"
- "۵ تا IP خالی برای سرورهای جدید می‌خوام"
- "Find free IPs at site X"
- "Show me available addresses in 10.0.1.0/24"

## نحوه اجرا

1. ابزار `netbox_find_free_ips` را با پارامترهای اختیاری site/family/count فراخوانی کنید.
2. جدول آدرس‌های IP آزاد را نمایش دهید.

## نحوه نمایش

```
**Available IPs (5):**

| Address | Prefix | Site | VLAN |
|---------|--------|------|------|
| 10.0.1.50 | 10.0.1.0/24 | DC-Primary | Servers |
| 10.0.1.51 | 10.0.1.0/24 | DC-Primary | Servers |
| 10.0.2.10 | 10.0.2.0/24 | DC-Primary | Management |
```

## موارد خاص

- **بدون IP آزاد:** "هیچ آدرس IP آزادی مطابق معیارهای شما یافت نشد."
- **سایت پیدا نشد:** "سایت 'X' پیدا نشد."

## مثال‌ها

**ورودی:** "۵ تا IP خالی تو DC-Primary پیدا کن"
**فراخوانی ابزار:** `netbox_find_free_ips(site="DC-Primary", count=5)`
**خروجی:** جدول آدرس‌های IP آزاد.

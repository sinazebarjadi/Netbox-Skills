---
name: netbox-search-devices
description: Search NetBox devices by name, serial, role, or model substring
tools: [netbox_search_devices]
---

# جستجوی دستگاه‌ها در NetBox

## چه زمانی استفاده شود

- "Find all Cisco switches"
- "List servers at SiteA"
- "Search for Dell devices"
- "Find devices with serial starting ABC"
- "همه سوییچ‌های سیسکو رو پیدا کن"
- "سرورهای سایت A رو لیست کن"

## نحوه جستجو

۱. ابزار `netbox_search_devices` را با رشته جستجو فراخوانی کن.
۲. اگر کاربر سایت، نقش یا مدل را مشخص کرده است، نتایج را پس از دریافت، سمت کلاینت فیلتر کن.
۳. نتایج را به‌صورت جدول نمایش بده.

## نحوه نمایش

```
**Found 3 devices:**

| Name | Serial | Role | Model | Site |
|------|--------|------|-------|------|
| SW-01 | ABC123 | Switch | C3850 | City-A |
| SW-02 | ABC124 | Switch | C3850 | City-A |
| SW-03 | ABC125 | Switch | C9300 | City-B |
```

## موارد خاص

- **بدون نتیجه:** «هیچ دستگاهی مطابق با 'X' یافت نشد.»
- **نتایج بیش از حد:** «N دستگاه یافت شد. ۱۰ مورد اول نمایش داده می‌شود. جستجوی خود را محدودتر کنید.»

## مثال‌ها

**ورودی:** "Find all Cisco switches"
**فراخوانی ابزار:** `netbox_search_devices("Cisco")`
**خروجی:** جدول فیلترشده دستگاه‌ها.

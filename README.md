# AI-Powered URL Slug Matcher for SEO Migration

> **For Persian/Farsi documentation, please scroll down** | **برای مشاهده مستندات فارسی، به پایین صفحه بروید** ⬇️

---

## Overview

A powerful AI-driven tool for matching old and new URLs in websites undergoing URL structure changes. 

Perfect for scenarios where webpage slugs have changed (especially in SEO projects or site migrations) but you can establish a topical/semantic relationship between old and new slugs – **with full support for Persian/Farsi slugs**.

---

## ✨ Features

- 📊 **Read old URLs from Excel file**
- 🗺️ **Read new URLs from sitemap.xml** (single or multiple files)
- 🤖 **Use various AI models** (OpenAI, Azure OpenAI, Anthropic, or local models)
- 🧪 **Test mode** (first 50 rows) and **full execution mode**
- 📤 **Excel output** with source and destination URLs side-by-side
- 🌐 **Full support for Persian/Farsi URLs and slugs** without encoding
- 🎯 **Duplicate detection** with color-coded warnings (red/yellow/orange)
- ⚙️ **Configurable via config.yaml**
- 💬 **Interactive mode** for ease of use
- 🔄 **Automatic retry** for sitemap downloads (up to 10 attempts)

---

## 👥 Ideal For

- 🔍 **SEO Specialists**
- 💻 **Web Developers**
- 🌐 **Site Managers** planning URL migration or redesign
- 🏢 **Digital Marketing Agencies**
- 📈 **Businesses** migrating from old to new platforms

---

## 🚀 Why Use This Tool?

With this tool, your URL redirect and matching process becomes more accurate, faster, and with minimal human error. Instead of manually matching hundreds or thousands of URLs, leverage AI's power for semantic analysis to find the best matches.

---

## 📋 Requirements

- Python 3.9+
- Internet access for model API calls
- API key for one provider: OpenAI, Azure OpenAI, Anthropic, or OpenAI-compatible/local (e.g., Liara)

---

## 🛠️ Installation

1) **Create virtual environment** (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2) **Install dependencies**:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

1) **Create your config from the sample**:
```bash
cp config.sample.yaml config.yaml
```

2) **Set the `ai` section for your provider**. Example (OpenAI-compatible, Liara):
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  temperature: 0.0
  response_json: true
  timeout_seconds: 60
  max_retries: 3
  retry_base_delay: 1.5
  qps: 1.0

  compatible_base_url: "https://ai.liara.ir/api/YOUR_PROJECT_ID/v1"
  compatible_api_key: "env:LIARA_API_KEY"
```

3) **Export your API key(s)**:
```bash
export LIARA_API_KEY="YOUR_KEY"
# or for OpenAI:
export OPENAI_API_KEY="YOUR_KEY"
```

---

## 🏃 Running the Tool

### Non-Interactive Mode

**Test mode** (first 50 rows - adjustable in code):
```bash
python url_matcher.py \
  --excel old_urls.xlsx \
  --config config.yaml \
  --out matched_urls.xlsx \
  --mode test \
  --min_confidence 0.6 \
  --sitemap sitemap1.xml \
  --sitemap_url https://example.com/sitemap.xml \
  --sitemaps_dir sitemaps \
  --verbose
```

**Full mode** (all rows):
```bash
python url_matcher.py \
  --excel old_urls.xlsx \
  --config config.yaml \
  --out matched_urls.xlsx \
  --mode full \
  --min_confidence 0.7 \
  --sitemap_url https://example.com/sitemap.xml
```

### Fully Interactive Mode

Start a guided flow that prompts for Excel file, then sitemap URLs one-by-one. Type `finishsitemaps` when done to start matching.

```bash
python url_matcher.py --config config.yaml --interactive --mode test --min_confidence 0.6 --sitemaps_dir sitemaps
```

**What you'll see:**
- Short guidance message (3–4 lines)
- Prompt: Enter path to Excel file (e.g., `old_urls.xlsx`)
- Prompt: Enter sitemap URLs one-by-one (type `finishsitemaps` to proceed)
- Each sitemap is downloaded with up to 10 attempts; on failure, you'll be asked if you want to try 10 more
- When finished, matching begins automatically and results are saved to the output Excel

---

## 📊 Output

The tool generates an **Excel file** containing:

| Column | Description |
|--------|-------------|
| `old_url` | Legacy URL |
| `best_new_url` | Selected new URL |
| `confidence` | 0..1 confidence score |
| `low_confidence` | Flag if below threshold |
| `rationale` | AI's reasoning |
| `candidates` | JSON list of considered URLs |
| `source_dup_of` | First row number if old URL duplicates |
| `dest_dup_of` | First row number if new URL duplicates |

### Row Highlights:
- 🔴 **Red**: Duplicate source URL - **Error**
- 🟡 **Light yellow**: Duplicate destination URL - **Warning**
- 🟠 **Orange**: Below minimum confidence threshold - **Low Confidence**

---

## 🔧 How It Works

1. **Read** old URLs from Excel and new URLs from all provided sitemaps
2. **Preserve** human-readable text (including Persian) using `unquote`
3. **Prune** candidates using heuristic (token-based Jaccard + prefix matching)
4. **Ask AI** to pick the best match and return JSON with `best_new_url`, `confidence`, and `rationale`
5. **Annotate** duplicate sources/destinations
6. **Write** styled Excel output with color-coded warnings

---

## ❗ Troubleshooting

- **Authentication errors**: Verify environment variables and `provider/model` in `config.yaml`
- **Sitemap download failures**: In interactive mode, you'll be prompted to retry another 10 attempts
- **Timeouts or rate limits**: Increase `timeout_seconds`, `max_retries`, or adjust `qps`
- **Invalid JSON from model**: The script attempts to extract JSON; try a different model or set `temperature: 0.0`

---

## 📄 License

MIT License - feel free to use and modify for your projects.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for SEO professionals and web developers**

---
---

# 🇮🇷 مستندات فارسی

## معرفی

ابزاری قدرتمند مبتنی بر هوش مصنوعی برای مطابقت آدرس‌های قدیمی و جدید در سایت‌هایی که ساختار URL آن‌ها تغییر کرده است.

مناسب برای زمانی که اسلاگ صفحات وب (خصوصاً در پروژه‌های سئو یا مهاجرت سایت) تغییر کرده ولی می‌توان ارتباط موضوعی بین اسلاگ‌های قدیم و جدید برقرار کرد – **حتی با پشتیبانی کامل از اسلاگ‌های فارسی**.

---

## ✨ ویژگی‌ها

- 📊 **خواندن آدرس‌های قدیمی از فایل Excel**
- 🗺️ **خواندن آدرس‌های جدید از sitemap.xml** (تک یا چند فایل)
- 🤖 **استفاده از مدل‌های مختلف AI** (OpenAI، Azure OpenAI، Anthropic، یا مدل‌های محلی)
- 🧪 **حالت تست** (۵۰ ردیف اول) و **حالت اجرا کامل**
- 📤 **خروجی در فایل Excel** با آدرس‌های مبدا و مقصد کنار هم
- 🌐 **پشتیبانی کامل از URLها و اسلاگ‌های فارسی** بدون کدگذاری
- 🎯 **تشخیص تکراری‌ها** با رنگ‌بندی هشدار (قرمز/زرد/نارنجی)
- ⚙️ **قابل تنظیم با فایل config.yaml**
- 💬 **حالت تعاملی** (Interactive) برای سهولت استفاده
- 🔄 **تلاش مجدد خودکار** برای دانلود سایت‌مپ‌ها (تا ۱۰ بار)

---

## 👥 مناسب برای

- 🔍 **متخصصان سئو** (SEO Specialists)
- 💻 **توسعه‌دهندگان وب** (Web Developers)
- 🌐 **مدیران سایت** که قصد مهاجرت یا بازطراحی آدرس‌های سایت را دارند
- 🏢 **آژانس‌های دیجیتال مارکتینگ**
- 📈 **کسب‌وکارهایی** که در حال انتقال از پلتفرم قدیمی به جدید هستند

---

## 🚀 چرا از این ابزار استفاده کنیم؟

با این ابزار، فرآیند ریدایرکت و تطبیق URL شما دقیق‌تر، سریع‌تر و با حداقل خطای انسانی انجام می‌شود. به‌جای مطابقت دستی صدها یا هزاران URL، از قدرت هوش مصنوعی برای تحلیل معنایی و پیدا کردن بهترین تطابق استفاده کنید.

---

## 📋 پیش‌نیازها

- Python 3.9 یا بالاتر
- دسترسی اینترنت (برای استفاده از APIهای مدل‌ها)
- کلید دسترسی به یکی از ارائه‌دهندگان: OpenAI، Azure OpenAI، Anthropic یا سرویس سازگار با OpenAI (مثل لیارا)

---

## 🛠️ نصب

1) **ایجاد محیط مجازی** (اختیاری اما توصیه‌شده):
```bash
python -m venv .venv
source .venv/bin/activate  # در Windows: .venv\Scripts\activate
```

2) **نصب وابستگی‌ها**:
```bash
pip install -r requirements.txt
```

---

## ⚙️ پیکربندی

1) **ایجاد فایل تنظیمات از نمونه**:
```bash
cp config.sample.yaml config.yaml
```

2) **تنظیم بخش `ai` برای ارائه‌دهنده خود**. مثال (سازگار با OpenAI، لیارا):
```yaml
ai:
  provider: openai_compatible
  model: openai/gpt-4o-mini
  temperature: 0.0
  response_json: true
  timeout_seconds: 60
  max_retries: 3
  retry_base_delay: 1.5
  qps: 1.0

  compatible_base_url: "https://ai.liara.ir/api/YOUR_PROJECT_ID/v1"
  compatible_api_key: "env:LIARA_API_KEY"
```

3) **تنظیم متغیر محیطی برای کلید API**:
```bash
export LIARA_API_KEY="YOUR_KEY"
# یا برای OpenAI:
export OPENAI_API_KEY="YOUR_KEY"
```

---

## 🏃 اجرای ابزار

### حالت غیر تعاملی

**حالت تست** (۵۰ ردیف اول - قابل تنظیم در کد):
```bash
python url_matcher.py \
  --excel old_urls.xlsx \
  --config config.yaml \
  --out matched_urls.xlsx \
  --mode test \
  --min_confidence 0.6 \
  --sitemap sitemap1.xml \
  --sitemap_url https://example.com/sitemap.xml \
  --sitemaps_dir sitemaps \
  --verbose
```

**حالت کامل** (تمام ردیف‌ها):
```bash
python url_matcher.py \
  --excel old_urls.xlsx \
  --config config.yaml \
  --out matched_urls.xlsx \
  --mode full \
  --min_confidence 0.7 \
  --sitemap_url https://example.com/sitemap.xml
```

### حالت کاملاً تعاملی

یک جریان راهنما که فایل Excel و سپس آدرس‌های sitemap را یکی‌یکی می‌پرسد. برای پایان، `finishsitemaps` را تایپ کنید.

```bash
python url_matcher.py --config config.yaml --interactive --mode test --min_confidence 0.6 --sitemaps_dir sitemaps
```

**آنچه خواهید دید:**
- پیام راهنمای کوتاه (۳-۴ خط)
- درخواست: مسیر فایل Excel را وارد کنید (مثلاً `old_urls.xlsx`)
- درخواست: آدرس‌های sitemap را یکی‌یکی وارد کنید (برای پایان `finishsitemaps` تایپ کنید)
- هر sitemap با حداکثر ۱۰ تلاش دانلود می‌شود؛ در صورت شکست، از شما پرسیده می‌شود آیا ۱۰ تلاش دیگر انجام شود
- پس از اتمام، مطابقت به‌طور خودکار شروع و نتایج در Excel ذخیره می‌شود

---

## 📊 خروجی

ابزار یک فایل **Excel** با ستون‌های زیر تولید می‌کند:

| ستون | توضیحات |
|------|---------|
| `old_url` | آدرس قدیمی |
| `best_new_url` | بهترین آدرس جدید پیشنهادی |
| `confidence` | درجه اطمینان (۰ تا ۱) |
| `low_confidence` | پرچم اطمینان پایین |
| `rationale` | توضیح منطقی مدل |
| `candidates` | لیست JSON کاندیداهای بررسی‌شده |
| `source_dup_of` | شماره ردیف اول در صورت تکراری بودن آدرس قدیمی |
| `dest_dup_of` | شماره ردیف اول در صورت تکراری بودن آدرس جدید |

### رنگ‌بندی ردیف‌ها:
- 🔴 **قرمز**: آدرس مبدا تکراری - **خطا**
- 🟡 **زرد کمرنگ**: آدرس مقصد تکراری - **هشدار**
- 🟠 **نارنجی**: زیر حد اطمینان - **اطمینان پایین**

---

## 🔧 نحوه کار

1. **خواندن** آدرس‌های قدیمی از Excel و آدرس‌های جدید از تمام سایت‌مپ‌ها
2. **حفظ** متن خوانا (شامل فارسی) با استفاده از `unquote`
3. **هرس** کاندیدها با استفاده از الگوریتم ابتکاری (Jaccard مبتنی بر توکن + تطابق پیشوند)
4. **پرسش از AI** برای انتخاب بهترین تطابق و دریافت JSON شامل `best_new_url`، `confidence` و `rationale`
5. **یادداشت** موارد تکراری مبدا/مقصد
6. **نوشتن** خروجی Excel با رنگ‌بندی هشدارها

---

## ❗ رفع مشکلات

- **خطاهای احراز هویت**: متغیرهای محیطی و `provider/model` در `config.yaml` را بررسی کنید
- **شکست در دانلود sitemap**: در حالت تعاملی، از شما پرسیده می‌شود آیا ۱۰ تلاش دیگر انجام شود
- **تایم‌اوت یا محدودیت نرخ**: `timeout_seconds`، `max_retries` را افزایش یا `qps` را تنظیم کنید
- **JSON نامعتبر از مدل**: اسکریپت سعی در استخراج JSON دارد؛ مدل دیگری امتحان کنید یا `temperature: 0.0` تنظیم کنید

---

## 📄 مجوز

مجوز MIT - برای پروژه‌های خود آزادانه استفاده و تغییر دهید.

---

## 🤝 مشارکت

مشارکت‌ها، گزارش مشکلات و درخواست‌های ویژگی جدید خوش‌آمد است!

---

## 📧 پشتیبانی

برای سؤالات یا پشتیبانی، لطفاً یک issue در GitHub ایجاد کنید.

---

**ساخته شده با ❤️ برای متخصصان سئو و توسعه‌دهندگان وب**

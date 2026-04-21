# 🛡️ ai-act-guardian - Simple AI Act Compliance Checks

[![Download and use ai-act-guardian](https://img.shields.io/badge/Download-ai--act--guardian-blue?style=for-the-badge&logo=github)](https://github.com/Jozithe3019/ai-act-guardian)

## 🚀 What this app does

ai-act-guardian helps you check files for EU AI Act and GDPR issues on Windows. It looks for common compliance risks in your project and flags them in plain terms. It is made for end users who want a clear check before they share, ship, or review a project.

It can help you spot:

- AI Act article risks in project files
- personal data that may count as PII
- missing checks around high-risk use cases
- cross-file data flow that may spread risk across a project
- common compliance issues in text, code, and config files

## 💻 What you need

Use a Windows PC with:

- Windows 10 or Windows 11
- At least 4 GB of RAM
- 200 MB of free disk space
- Internet access to open the download page
- A modern browser like Edge, Chrome, or Firefox

For best results, close large apps before you run the scan.

## 📥 Download

Visit this page to download:

https://github.com/Jozithe3019/ai-act-guardian

Open the page, look for the latest release or main project page, and download the Windows version if one is listed. If the page offers a ZIP file or installer, save it to your computer before you open it.

## 🧭 How to install on Windows

1. Open the download page in your browser.
2. Find the latest release or download option.
3. Download the Windows file to your Downloads folder.
4. If the file is in a ZIP folder, right-click it and choose Extract All.
5. Open the extracted folder.
6. Double-click the app file or launcher.
7. If Windows shows a security prompt, choose Run or More info, then Run anyway if you trust the file source.
8. Wait for the app to open.

If the app comes with a setup file, follow the on-screen steps and keep the default choices unless you want a different install location.

## 🧪 How to run a scan

1. Open ai-act-guardian.
2. Choose the folder or file you want to check.
3. Start the scan.
4. Wait for the result list to load.
5. Review each item that gets flagged.
6. Open the file it points to if you want to inspect the line or section.
7. Fix the issue and run the scan again.

For a first scan, use a small folder so you can see how the results look.

## 📂 What it checks

ai-act-guardian is built to inspect project files for signs of legal and privacy risk. It focuses on:

- **EU AI Act rules**  
  It checks for patterns tied to Articles 5, 14, and 52.

- **PII detection**  
  It looks for personal data such as names, email addresses, phone numbers, IDs, and other user details.

- **Cross-file taint tracking**  
  It follows data as it moves from one file to another so hidden risk is easier to spot.

- **Static analysis**  
  It reads files without running them, which keeps the check simple and safe.

- **Compliance review**  
  It helps you catch issues before they turn into a larger review problem.

## 🛠️ Common file types

You can use it on files such as:

- Python files
- config files
- text files
- project folders
- source code trees
- support files that store user data or model settings

If you are unsure what to scan, start with the main project folder.

## 🧩 How the results work

The app may show results in a list with:

- file name
- line number
- rule name
- severity
- short reason for the flag

Read the reason first. It should tell you why the item was marked. If a result points to personal data, check whether that data should be removed, masked, or stored in a safer way. If it points to a policy or AI Act rule, review the related code or text and make the wording or flow clearer.

## ✅ Good uses

Use ai-act-guardian when you want to:

- review a new AI project before sharing it
- check for user data in code or notes
- scan project folders for compliance issues
- look for risks tied to model behavior or output text
- get a first pass before a manual review

## 🔍 Example workflow

A simple way to use the app:

1. Download it from the project page.
2. Open the app on Windows.
3. Scan your project folder.
4. Review the flagged items.
5. Fix the items that look risky.
6. Scan again to confirm the result list is smaller.

This workflow works well for school work, internal tools, demos, and early-stage AI projects.

## 📌 Tips for better scans

- Scan the full project folder, not just one file.
- Check files that store prompts, logs, or user input.
- Review config files, sample data, and notes.
- Remove test data that contains real personal details.
- Keep file names clear so you can find issues faster.
- Run the scan again after each round of fixes.

## 🧠 Why this tool helps

EU AI Act and GDPR checks can be hard to track by hand. This app gives you a clear first look at common risk areas. It helps you find problems early, while the project is still easy to change.

It is useful when you want a plain report instead of reading every file one by one.

## 🗂️ Project topics

This project is linked to:

- ast
- compliance
- eu-ai-act
- gdpr
- linter
- python
- regulatory-compliance
- security
- static-analysis
- taint-analysis

## 📞 If something does not work

If the app does not open:

- check that the file finished downloading
- make sure Windows did not block the file
- try extracting the ZIP again
- move the app to a simple folder like `C:\Apps`
- open the download page again and check for a newer file

If the scan shows no results, try a larger folder or confirm that the folder has supported file types.

## 🔐 Privacy and compliance use

Use this app as part of a review process, not as your only check. It helps you spot likely issues, but you should still read the flagged files yourself. For projects with user data, keep data handling clear and limit what you store in the first place
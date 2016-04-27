# app-stores-toolkit
Soft, quick, useful layer built on Fastlane tool, Google Publishing API, Apple iTransporter

**Usage:**

1. Use Google Spreadsheet at link [here](https://docs.google.com/spreadsheets/d/1gvd1y6YNyPNxqCYm324svAP2a3JFQnX9m9AtbIi2ZQQ/edit?usp=sharing) to translate your app stores metadata strings.
2. Download (or just copy content) to your computer as xlsx file (notice to check the downloaded file so that it still remains all translated strings).
3. You should init your fastlane Apple Appstore/Google Play project first.
3. Run the script populate.py to populate data from xlsx file to your Apple Appstore/Google Play metadata.
4. Resubmit your data by fastlane command.
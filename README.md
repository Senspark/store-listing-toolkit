# app-stores-toolkit
Soft, quick, useful layer built on Fastlane tool, Google Publishing API, Apple iTransporter

**Usage:**

1. Use Google Spreadsheet at link [here](https://docs.google.com/spreadsheets/d/1gvd1y6YNyPNxqCYm324svAP2a3JFQnX9m9AtbIi2ZQQ/edit?usp=sharing) to translate your app stores metadata strings.
2. Download (or just copy content) to your computer as xlsx file (notice to check the downloaded file so that it still remains all translated strings).
3. You should init your fastlane Apple Appstore/Google Play project first.
3. Run the script populate.py to populate data from xlsx file to your Apple Appstore/Google Play metadata.

	./populate.py metadata -platform PLATFORM -src_data_path SRC_DATA_PATH -prj_path FASTLANE_PRJ_PATH -manual_src_meta_path MANUAL_SRC_PATH
  
  	Sample: ./populate.py metadata -platform iOS -src_data_path data.xlsx -prj_path . -src_screenshots_path ./src/screenshots

	./populate.py screenshots -platform PLATFORM -src_screenshots_path SRC_SCREENSHOTS_PATH -prj_path FASTLANE_PRJ_PATH 
	
	Sample: ./populate.py screenshots -platform android -src_screenshots_path ./src/screenshots -prj_path .
	
4. Resubmit your data by fastlane command.
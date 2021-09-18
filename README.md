# download_chrome_extensions

## STEP1: get all the ids from google sitemap
**get_all_ids.py**  
**config.py**  
This code is mostly copied from https://github.com/logicalhacking/ExtensionCrawler  
store the discovered ids in known_ids.txt  


## STEP2: download the extensions from Google CDN
**extension_crawler.py**  
With the url:  
url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=31.0.1609.0&acceptformat=crx2,crx3&x=id%3D{id}%26uc"  
NOTE that the parameter: acceptformat=crx2,crx3 must be added to let the download succeed.   
Refer to:   
https://stackoverflow.com/questions/7184793/how-to-download-a-crx-file-from-the-chrome-web-store-for-a-given-id  
The downloaded extensions are stored in extensions/  

## STEP3: extract code from CRX files
**crx2unzip.py**  
extract zip file from crx file, then unzip  
By default:  
The extension directory is extensions/  
The temporary zip files will be stored in zipped_extensions/  
The zip files that are broken will be left in zipped_extensions/, the ones that are successfully unzipped will then be deleted.  
The successfully unzipped files will be stored in unzipped_extensions/  
The crx files' names with file size 0 will be stored in zero_file.txt (filesize 0 indicated they are no longer available on Chrome Web Store)  


With the code in this repository, we  
got 187,667 ids on 2021.09.08  
downloaded 185,076 crx files on 2021.09.17  
Among them, 20,622 crx file size 0 (no longer available)  
1 zip file not able to unzip (a theme)  
164,453 successfully unzipped extensions (including themes and extensions)  

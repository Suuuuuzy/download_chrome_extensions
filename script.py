# STEP 1:
from get_all_ids import get_ids
# get_ids() 219245 2023/3/5
# STEP 2:
from extension_crawler import crawl
# crawl()
# STEP 3:
from crx2unzip import run_with_threads
# run_with_threads(crxdir='extensions', zipdir='/media/data4/jianjia_data4/new_extension/zipped_extensions', unzipdir='/media/data4/jianjia_data4/new_extension/unzipped_extensions')
# STEP 4:
# 133549 2023/3/5, in filtered_file.txt
from filter_no_theme import filter_run_with_threads
filter_run_with_threads(unzipdir='/media/data4/jianjia_data4/new_extension/unzipped_extensions') 

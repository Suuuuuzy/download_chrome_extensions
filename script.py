from get_all_ids import get_ids
get_ids()
from extension_crawler import crawl
crawl()
from crx2unzip import run_with_threads
run_with_threads(crxdir='extensions', zipdir='/media/data4/jianjia_data4/new_extension/zipped_extensions', unzipdir='/media/data4/jianjia_data4/new_extension/unzipped_extensions')
from filter_no_theme import filter_run_with_threads
filter_run_with_threads(crxdir='extensions', unzipdir='/media/data4/jianjia_data4/new_extension/unzipped_extensions')

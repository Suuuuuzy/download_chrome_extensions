import os
import json
import threading, time, sys, getopt
from tqdm import tqdm


def filter_no_theme(flag, crxs, unzipdir):
    count =0
    filtered_files = []
    theme = []
    error_json = []
    for crx in crxs:
        files = os.listdir(os.path.join(unzipdir, crx))
        if 'manifest.json' not in files:
            continue        
        with open(os.path.join(unzipdir, crx, 'manifest.json'), encoding='ascii', errors='ignore') as f:
            try:
                manifest = json.load(f)
                if 'theme' in manifest:
                    theme.append(crx)
                    continue
                else:
                    count+=1
                    filtered_files.append(crx)
            except:
                error_json.append(crx)
                # print('json load error: ', crx)
        
    print('successfully filtered ', count, 'extension (not theme) files')
    with open(str(flag) + 'filtered_file.txt', 'w') as f:
        json.dump(filtered_files, f)
    with open(str(flag) + 'theme.txt', 'w') as f:
        json.dump(theme, f)
    with open(str(flag) + 'error_json.txt', 'w') as f:
        json.dump(error_json, f)
    print('Thread No.' + str(flag) + ' end.')

def sum_all_files(prefix):
    zero_list = []
    thread_num = 200
    with open(prefix+'.txt', 'w') as f:
        for i in range(0, thread_num):
            with open(str(i) + prefix+'.txt') as fr:
                c = json.load(fr)
                zero_list.extend(c)
        json.dump(zero_list, f)
    for i in range(0, thread_num):
        os.remove(str(i) + prefix+'.txt')


def filter_run_with_threads(unzipdir, func=filter_no_theme, ):
    thread_num = 200
    threads = []
    flag = 0
    crxs = os.listdir(unzipdir)
    crxs = [i for i in crxs if not i.startswith('.')]
    step = len(crxs) // thread_num
    print('Filter task started with %d threads.'%thread_num)
    for i in range(thread_num - 1):
        t = threading.Thread(target=func, args=(i, crxs[flag:flag+step], unzipdir))
        t.start()
        threads.append(t)
        flag += step
    t = threading.Thread(target=func, args=(thread_num - 1, crxs[flag:], unzipdir))
    t.start()
    threads.append(t)
    for t in threads:
        t.join()
    
    sum_all_files('filtered_file')
    sum_all_files('theme')
    sum_all_files('error_json')

    print('Task finished.')

if __name__ == "__main__":
    filter_run_with_threads(unzipdir = '/media/data4/jianjia_data4/new_extension/unzipped_extensions')


import json
import os
import threading, time, sys, getopt
from tqdm import tqdm
thread_num = 200
def filter_mv3(flag, crxs, unzipdir):
    count =0
    mv3Ids = []
    for crx in crxs:
        files = os.listdir(os.path.join(unzipdir, crx))
        if 'manifest.json' not in files:
            continue        
        with open(os.path.join(unzipdir, crx, 'manifest.json'), encoding='ascii', errors='ignore') as f:
            try:
                manifest = json.load(f)
                if 'manifest_version' in manifest and manifest['manifest_version']==3:
                    mv3Ids.append(crx)
                    count+=1
            except:
                pass
        
    print('successfully filtered ', count, 'extensions are mv3')
    with open(str(flag) + 'mv3Ids.txt', 'w') as f:
        json.dump(mv3Ids, f)
    print('Thread No.' + str(flag) + ' end.')

def sum_all_files(prefix):
    zero_list = []
    global thread_num
    with open(prefix+'.txt', 'w') as f:
        for i in range(0, thread_num):
            with open(str(i) + prefix+'.txt') as fr:
                c = json.load(fr)
                zero_list.extend(c)
        json.dump(zero_list, f)
    for i in range(0, thread_num):
        os.remove(str(i) + prefix+'.txt')


def run_with_threads(func, unzipdir, idFile):
    global thread_num
    threads = []
    flag = 0
    with open(idFile) as f:
        crxs = json.load(f)
    step = len(crxs) // thread_num
    print('Task started with %d threads.'%thread_num)
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
    
    sum_all_files('mv3Ids')

    print('Task finished.')

# run_with_threads(args.crxdir, crx2zip, args.crxdir, args.zipdir)
run_with_threads(func = filter_mv3, unzipdir = '../unzipped_extensions', idFile = '../filtered_file.txt')
# run_with_threads(func = filter_mv3, unzipdir = '/Users/jia/Desktop/tmp/EOPG/run_JSCPG_merge/demos', idFile = '/Users/jia/Desktop/tmp/EOPG/run_JSCPG_merge/crx_lists/test.txt')
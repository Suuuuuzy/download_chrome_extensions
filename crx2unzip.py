import os
import zipfile
import argparse
import threading
import json

parser = argparse.ArgumentParser()
parser.add_argument('--crxdir', help='the directory of crx files', default='extensions')
parser.add_argument('--zipdir', help='the directory of zipped files', default='zipped_extensions')
parser.add_argument('--unzipdir', help='the directory of unzipped files', default='unzipped_extensions')
args = parser.parse_args()
print(args)

os.makedirs(args.zipdir, exist_ok = True)
os.makedirs(args.unzipdir, exist_ok = True)

# convert to zip file
def crx2zip(flag, files, crxdir, zipdir):
    zipped_files = os.listdir(zipdir)
    # print('zipped_files: ')
    # print(zipped_files)
    count = 0
    for file in files:
        id = file[:-4]
        # print('id: ', id)
        if file.startswith('.') or (id+'.zip') in zipped_files:
            continue
        if os.stat(os.path.join(crxdir, file)).st_size==0:
            print('file size is 0: ', file)
            continue
        with open(os.path.join(crxdir, file), 'rb') as f:
            content = f.read()
        with open(os.path.join(zipdir, file.split('.crx')[0]+'.zip'), 'wb') as f:
            f.write(content[307:])
            count += 1
            print(file)
    print('successfully zipped ', count, 'crx files')
    print('Thread No.' + str(flag) + ' end.')

def zip2unzip(flag, files, zipdir, unzipdir):
    unzipped_files = os.listdir(unzipdir)
    # print('unzipped_files: ')
    # print(unzipped_files)
    # then convert to unzipped file
    count = 0
    for file in files:
        id = file[:-4]
        if file.startswith('.') or id in unzipped_files:
            continue
        if os.stat(os.path.join(zipdir, file)).st_size==0:
            print('file size is 0: ', file)
            continue
        with zipfile.ZipFile(os.path.join(zipdir, file), 'r') as zip_ref:
            try:
                zip_ref.extractall(os.path.join(unzipdir, file.split('.zip')[0]))
                count += 1
                print(file)
            except:
                print('failed to unzip', file)
    print('successfully unzipped ', count, 'zipped files')
    print('Thread No.' + str(flag) + ' end.')


def crx2unzip(flag, files, crxdir, zipdir, unzipdir, zipped_files, unzipped_files):
    count = 0
    zero_file = []
    for file in files:
        id = file[:-4]
        if file.startswith('.') or id in unzipped_files:
            continue
        if os.stat(os.path.join(crxdir, file)).st_size==0:
            zero_file.append(file)
            continue

        id = file[:-4]
        # print('id: ', id)
        tmp_zip = os.path.join(zipdir, id+'.zip')
        if (id+'.zip') in zipped_files:
            pass
        else:
            with open(os.path.join(crxdir, file), 'rb') as f:
                content = f.read()
            with open(tmp_zip, 'wb') as f:
                f.write(content[307:])
        try:
            with zipfile.ZipFile(tmp_zip, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(unzipdir, id))
                count += 1
            os.remove(tmp_zip)
        except:
            print('failed to unzip', tmp_zip)
            
    print('successfully unzipped ', count, 'zipped files')
    with open(str(flag) + '_zero_file.txt', 'w') as f:
        json.dump(zero_file, f)
    print('Thread No.' + str(flag) + ' end.')



def run_with_threads(func, crxdir, zipdir, unzipdir):
    zipped_files = os.listdir(zipdir)
    unzipped_files = os.listdir(unzipdir)
    thread_num = 200
    threads = []
    flag = 0
    files = os.listdir(crxdir)
    step = len(files) // thread_num
    print('Task started with %d threads.'%thread_num)
    for i in range(thread_num - 1):
        t = threading.Thread(target=func, args=(i, files[flag:flag+step], crxdir, zipdir, unzipdir, zipped_files, unzipped_files))
        t.start()
        threads.append(t)
        flag += step
    t = threading.Thread(target=func, args=(thread_num - 1, files[flag:], crxdir, zipdir, unzipdir, zipped_files, unzipped_files))
    t.start()
    threads.append(t)
    for t in threads:
        t.join()
    zero_list = []
    with open('zero_file.txt', 'w') as f:
        for i in range(0, thread_num):
            with open(str(i) + '_zero_file.txt') as fr:
                c = json.load(fr)
                zero_list.extend(c)
        json.dump(zero_list, f)
    for i in range(0, thread_num):
        os.remove(str(i) + '_zero_file.txt')

    print('Task finished.')

# run_with_threads(args.crxdir, crx2zip, args.crxdir, args.zipdir)
run_with_threads(crx2unzip, args.crxdir, args.zipdir, args.unzipdir)




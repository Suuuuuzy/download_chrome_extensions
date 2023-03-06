import os
import zipfile
import argparse
import threading
import json

parser = argparse.ArgumentParser()
parser.add_argument('--crxdir', help='the directory of crx files', default='extensions')
parser.add_argument('--zipdir', help='the directory of zipped files', default='/media/data4/jianjia_data4/new_extension/zipped_extensions')
parser.add_argument('--unzipdir', help='the directory of unzipped files', default='/media/data4/jianjia_data4/new_extension/unzipped_extensions')
args = parser.parse_args()
print(args)

os.makedirs(args.zipdir, exist_ok = True)
os.makedirs(args.unzipdir, exist_ok = True)


def crx2unzip(flag, files, crxdir, zipdir, unzipdir):
    count = 0
    for file in files:
        id = file[:-4]
        # print('id: ', id)
        tmp_zip = os.path.join(zipdir, id+'.zip')
        if not os.path.isfile(tmp_zip):
            with open(os.path.join(crxdir, file), 'rb') as f:
                content = f.read()
            with open(tmp_zip, 'wb') as f:
                f.write(content[307:])
        try:
            with zipfile.ZipFile(tmp_zip, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(unzipdir, id))
                count += 1
            os.remove(tmp_zip)
            print('successfully unzipped', tmp_zip)
        except:
            print('failed to unzip', tmp_zip)
            
    print('successfully unzipped ', count, 'zipped files')
    print('Thread No.' + str(flag) + ' end.')
    

def run_with_threads(crxdir, zipdir, unzipdir, func = crx2unzip):
    thread_num = 200
    threads = []
    flag = 0
    files = os.listdir(crxdir)
    files = [i for i in files if not i.startswith(".")]
    unzips = os.listdir(unzipdir)
    files = [i for i in files if i[:-4] not in unzips]         
    print(len(files), " crx files to extract")   
    step = len(files) // thread_num
    print('Task started with %d threads.'%thread_num)
    for i in range(thread_num - 1):
        t = threading.Thread(target=func, args=(i, files[flag:flag+step], crxdir, zipdir, unzipdir))
        t.start()
        threads.append(t)
        flag += step
    t = threading.Thread(target=func, args=(thread_num - 1, files[flag:], crxdir, zipdir, unzipdir))
    t.start()
    threads.append(t)
    for t in threads:
        t.join()

    print('Task finished.')


if __name__ == "__main__":
    run_with_threads(args.crxdir, args.zipdir, args.unzipdir)




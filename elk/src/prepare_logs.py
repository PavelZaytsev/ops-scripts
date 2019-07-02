#! /usr/bin/env python

import os
import sys
import tarfile
import glob
import gzip
import shutil
import json
import fnmatch
from pathlib import Path

arguments = sys.argv

ignored_patterns = ['*esx*']

def unarchive_tar(path, data_path):
    processed = []
    unarchived = []
    unarchive_tar_rec(path, data_path, processed, unarchived)
    if not unarchived:
        raise ValueError(f'Nothing has been processed for {path}')
    else:
        return unarchived


def unarchive_tar_rec(path, data_path, processed, unarchived):
    for pattern in ignored_patterns:
        if fnmatch.fnmatch(path, pattern):
            print(f'Skipping {path}...')
            return None

    if os.path.isfile(path) and tarfile.is_tarfile(path):
        processed.append(path)
        with tarfile.open(path) as archive:
            print(f'Extracting {path}...')
            archive.extractall(path=data_path)
            members = archive.getmembers()
            for member in members:
                member_path = '/'.join([data_path, member.name])
                if '/' not in member.name and member.name not in unarchived and os.path.isdir(
                        member_path):
                    unarchived.append(member.name)
                try:
                    if member_path not in processed \
                            and os.path.isfile(member_path) \
                            and tarfile.is_tarfile(member_path) \
                            and os.path.splitext(member_path)[1] in ['.tgz', '.tar', '.gzip', '.gz']:
                        unarchive_tar_rec(member_path, data_path, processed, unarchived)
                except Exception as ex:
                    print(f'There was an issue processing path {member_path}')
                    print(f'The exception was {ex}.')


def unarchive_gzip(path, data_path):
    with gzip.open(path) as decompressed_archive:
        print(f'Extracting {path}')
        archive_name = path.split('/')[-1]
        archive_name = archive_name.split('.')
        archive_name.pop()
        file_name = '.'.join(archive_name)
        new_file_path = '/'.join([data_path, file_name])
        with open(new_file_path, 'wb') as output_file:
            output_file.write(decompressed_archive.read())


def get_bundles_ip(ifconfig_path):
    with open(ifconfig_path) as ifconfig_file:
        ifconfig_file.readline()
        line = ifconfig_file.readline().strip()
        addr = line.split(' ')[1]
        ip = addr.split(':')[1]
        return ip


def unzip_logs(path, pattern):
    match_path = '/'.join([path, pattern])
    matched_files = glob.glob(match_path)
    if not matched_files:
        print(f'No {pattern} archive logs found')
        return
    matched_str = '\n'.join(matched_files)
    print(f'Found the following zipped log files:\n{matched_str}')

    for file in matched_files:
        unarchive_gzip(file, path)


def prepare_log_directory(data_path, ip, path, pattern):
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    dir_name = '/'.join([data_path, ip])
    try:
        if not os.path.isdir(dir_name): os.mkdir(dir_name)
        match_path = '/'.join([path, pattern])
        log_files = glob.glob(match_path)
        if not log_files:
            raise FileNotFoundError('No matched log files')
        for old_file_name in log_files:
            file_name = old_file_name.split('/')[-1]
            new_file_name = '/'.join([dir_name, file_name])
            print(f'Moving to {new_file_name}')
            shutil.move(old_file_name, new_file_name)
    except FileNotFoundError as fnfe:
        print(str(fnfe))
        raise


def prepare_layout(data_path, layout_path):
    pattern = 'LAYOUTS_*.ds'
    all_layouts = glob.glob('/'.join([layout_path, pattern]))
    if not all_layouts:
        print('No layouts in dir')
        return
    for f in all_layouts:
        buffer = []
        with open(f, 'rb') as file:
            content = file.read(4)
            while content != b'':
                content = file.read(1)
                buffer.append(content)
            string = str(b''.join(buffer), 'utf-8')
            json_string = json.loads(string)
        file_name = f.split('/')[-1]
        with open('/'.join([data_path, '{}.json'.format(os.path.splitext(file_name)[0])]),
                  'w') as file:
            json.dump(json_string, file, indent=4)


if len(arguments) < 2:
    raise ValueError('support bundle archive is required')

else:
    # TODO: remove dirs when done
    support_bundle = arguments[1]
    data_path = '/'.join([os.getcwd(), 'data'])
    path = '/'.join([data_path, support_bundle])
    path_exists = os.path.isfile(path)

    if not path_exists:
        raise FileNotFoundError(f'support bundle {path} does not exists')

    if not tarfile.is_tarfile(path):
        raise tarfile.TarError(f'support bundle {path} should be a tar archive')

    unarchived_dirs = unarchive_tar(path, data_path)

    for archive_name in unarchived_dirs:
        if 'nsx_manager' in archive_name:
            print(f'Found: {archive_name}')

            archive_path = '/'.join([data_path, archive_name])
            system_path = '/'.join([archive_path, 'system'])

            if not os.path.isdir(system_path):
                raise FileNotFoundError('System directory is not found in the bundle')

            ifconfig = '/'.join([system_path, 'ifconfig_-a'])

            if not os.path.isfile(ifconfig):
                raise FileNotFoundError('ifconfig file not found in the system directory')

            print('Extracting this bundles ip')

            ip = get_bundles_ip(ifconfig)
            print(f'Found ip: {ip}')

            corfu_log_dir = '/'.join([archive_path, 'var', 'log', 'corfu'])
            proton_log_dir = '/'.join([archive_path, 'var', 'log', 'proton'])
            ccp_log_dir = '/'.join([archive_path, 'var', 'log', 'cloudnet'])

            if not os.path.isdir(corfu_log_dir):
                raise FileNotFoundError('Corfu log directory does not exist')

            print('Unzipping logs if any')

            unzip_logs(corfu_log_dir, 'corfu.9000.*log.gz')
            unzip_logs(proton_log_dir, 'nsxapi.*log.gz')
            unzip_logs(ccp_log_dir, 'nsx-ccp.*log.gz')

            print('Moving logs to a separate directory')

            top_dir = '/'.join(['/output', 'data', os.path.splitext(support_bundle)[0]])

            prepare_log_directory(top_dir, ip, corfu_log_dir, "corfu.9000*.log")
            prepare_log_directory(top_dir, ip, proton_log_dir, "nsxapi*.log")
            prepare_log_directory(top_dir, ip, ccp_log_dir, "nsx-ccp.*log")

    print('Logs are ready for stashing.')

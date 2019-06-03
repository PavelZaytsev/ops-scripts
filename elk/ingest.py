#! /usr/bin/env python

import os
import sys
import tarfile
import glob
import gzip
import shutil

arguments = sys.argv


def unarchive_tar(path, data_path):
    with tarfile.open(path) as archive:
        print(f'Extracting {path}...')
        members = archive.getmembers()
        if not members:
            raise tarfile.TarError('Archive is empty')
        archive.extractall(path=data_path)
        archive_name = members[0].name.split('/')[0]
        return archive_name


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


def unzip_corfu_logs(corfu_path):
    match_path = '/'.join([corfu_path, 'corfu.9000.*log.gz'])
    matched_files = glob.glob(match_path)
    if not matched_files:
        print('No corfu archive logs found')
        return
    matched_str = '\n'.join(matched_files)
    print(f'Found the following zipped corfu log files:\n{matched_str}')

    for corfu_file in matched_files:
        unarchive_gzip(corfu_file, corfu_path)


def prepare_log_directory(data_path, ip, corfu_path):
    dir_name = '/'.join([data_path, ip])
    if not os.path.isdir(dir_name):
        try:
            os.mkdir(dir_name)
            match_path = '/'.join([corfu_path, 'corfu.9000.*log'])
            corfu_log_files = glob.glob(match_path)
            if not corfu_log_files:
                raise FileNotFoundError('No matched corfu log files')
            for old_file_name in corfu_log_files:
                file_name = old_file_name.split('/')[-1]
                new_file_name = '/'.join([dir_name, file_name])
                print(f'Moving to {new_file_name}')
                shutil.move(old_file_name, new_file_name)
        except FileNotFoundError as fnfe:
            print(str(fnfe))
            raise


if len(arguments) < 2:
    raise ValueError('support bundle archive is required')

else:
    support_bundle = arguments[1]
    data_path = '/'.join([os.getcwd(), 'data'])
    path = '/'.join([data_path, support_bundle])
    path_exists = os.path.isfile(path)

    if not path_exists:
        raise FileNotFoundError(f'support bundle {support_bundle} does not exists')

    if not tarfile.is_tarfile(path):
        raise tarfile.TarError(f'support bundle {support_bundle} should be a tar archive')

    archive_name = unarchive_tar(path, data_path)
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

    if not os.path.isdir(corfu_log_dir):
        raise FileNotFoundError('Corfu log directory does not exist')

    print('Unzipping corfu logs if any')

    unzip_corfu_logs(corfu_log_dir)

    print('Moving corfu logs to a separate directory')

    prepare_log_directory(data_path, ip, corfu_log_dir)

import os
import argparse
import sys
import xml.etree.ElementTree as ET
from base64 import b64decode
import shlex

def list_cookies_flag_each(cookies, flag):
    result = ""
    for cookie in cookies:
       result = result + flag + " '" + cookie + "' "
    return result


def list_cookies_single_flag(cookies, flag, postfix=''):
    result = flag
    for cookie in cookies:
       result = result + " '" + cookie + "' " + postfix
    return result


def list_cookies_long(cookies, flag, postfix='; '):
    result = flag + " '"
    for cookie in cookies:
       result = result + cookie + postfix
    return result.rstrip() + "'"


def read_cookies(fname):
    # I should check more than the extension
    if fname.split('.')[-1] == 'xml':
        try:
            tree = ET.parse(fname)
            root = tree.getroot()

            for item in root.iter('request'):
                if item.attrib['base64']:
                    x = b64decode(item.text)
                req = x.decode('utf-8')
        except FileNotFoundError:
            sys.exit('File not found.')
        except:
            sys.exit('Failed to parse xml. I only parse xml from Burpsuite.')
    else:
        with open(fname) as fin:
            req = fin.read()

    cookies = [x for x in req.split('\n')
                if 'cookie' in x.lower()][0].split(':', 1)[1].strip().split(';')
    cookies = [x.strip() for x in cookies]
    return cookies


if __name__ == '__main__':
    names = ['dalfox', 'tplmap', 'seesurf', 'arjun', 'blackwidow', 'dirsearch', 'noxss', 'xsstrike', 'x8']
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set-posix',
                        dest='set_posix',
                        default=False,
                        action='store_true')
    parser.add_argument('-df', '--dalfox',
                        dest='dalfox',
                        default=False,
                        action='store_true')
    parser.add_argument('-tpl', '--tplmap',
                        dest='tplmap',
                        default=False,
                        action='store_true')
    parser.add_argument('-ss', '--seesurf',
                        dest='seesurf',
                        default=False,
                        action='store_true')
    parser.add_argument('-aj', '--arjun',
                        dest='arjun',
                        default=False,
                        action='store_true')
    parser.add_argument('-bw', '--blackwidow',
                        dest='blackwidow',
                        default=False,
                        action='store_true')
    parser.add_argument('-ds', '--dirsearch',
                        dest='dirsearch',
                        default=False,
                        action='store_true')
    parser.add_argument('-nx', '--noxss',
                        dest='noxss',
                        default=False,
                        action='store_true')
    parser.add_argument('-xs', '--xsstrike',
                        dest='xsstrike',
                        default=False,
                        action='store_true')
    parser.add_argument('-x8', '--x8',
                        dest='x8',
                        default=False,
                        action='store_true')

    parser.add_argument('-f', '--file',
                        dest='file',
                        type=str,
                        required=True)

    args = parser.parse_args()


    cookies = read_cookies(args.file)
    do_all = True if args.set_posix or not (args.dalfox or args.tplmap or args.seesurf or args.arjun or args.blackwidow or args.dirsearch or args.noxss or args.xsstrike or args.x8) else False


    c = '_COOKIE'
    results = {}
    if do_all or args.dalfox:
        results[('dalfox'+c).upper()] = list_cookies_flag_each(cookies, '-C')
    if do_all or args.tplmap:
        results[('tplmap'+c).upper()] = list_cookies_flag_each(cookies, '--cookie')
    if do_all or args.seesurf:
        results[('seesurf'+c).upper()] = list_cookies_single_flag(cookies, '-c')
    if do_all or args.arjun:
        results[('arjun'+c).upper()] = list_cookies_long(cookies, '--headers', '; ')
    if do_all or args.blackwidow:
        results[('blackwidow'+c).upper()] = list_cookies_long(cookies, '-c')
    if do_all or args.dirsearch:
        results[('dirsearch'+c).upper()] = list_cookies_long(cookies, '--cookie')
    if do_all or args.noxss:
        results[('noxss'+c).upper()] = list_cookies_long(cookies, '--cookie')
    if do_all or args.xsstrike:
        results[('xsstrike'+c).upper()] = list_cookies_long(cookies, '--headers', '; ')
    if do_all or args.x8:
        results[('x8'+c).upper()] = list_cookies_single_flag(cookies, '-H')

    # just doing posix right now then I'll do pwsh
    if args.set_posix or True:
        for name, value in results.items():
            # Escape symbols commonly used by Bash.
            value = shlex.quote(value)
            print('export {}={}'.format(
                name,
                value
            ))

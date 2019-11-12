#!/usr/bin/env python3
"""jc - JSON CLI output utility

JC cli module
"""
import sys
import textwrap
import signal
import json
import jc.utils
import jc.parsers.arp
import jc.parsers.df
import jc.parsers.dig
import jc.parsers.env
import jc.parsers.free
import jc.parsers.history
import jc.parsers.ifconfig
import jc.parsers.iptables
import jc.parsers.jobs
import jc.parsers.ls
import jc.parsers.lsblk
import jc.parsers.lsmod
import jc.parsers.lsof
import jc.parsers.mount
import jc.parsers.netstat
import jc.parsers.ps
import jc.parsers.route
import jc.parsers.uname
import jc.parsers.uptime
import jc.parsers.w


def ctrlc(signum, frame):
    exit()


def helptext(message):
    helptext_string = f'''
    jc:     {message}

    Usage:  jc PARSER [OPTIONS]

    Parsers:
            --arp        arp parser
            --df         df parser
            --dig        dig parser
            --env        env parser
            --free       free parser
            --history    history parser
            --ifconfig   iconfig parser
            --iptables   iptables parser
            --jobs       jobs parser
            --ls         ls parser
            --lsblk      lsblk parser
            --lsmod      lsmod parser
            --lsof       lsof parser
            --mount      mount parser
            --netstat    netstat parser
            --ps         ps parser
            --route      route parser
            --uname      uname -a parser
            --uptime     uptime parser
            --w          w parser

    Options:
            -d           debug - show trace messages
            -p           pretty print output
            -q           quiet - suppress warnings
            -r           raw JSON output

    Example:
            ls -al | jc --ls -p
    '''
    print(textwrap.dedent(helptext_string), file=sys.stderr)


def main():
    signal.signal(signal.SIGINT, ctrlc)

    if sys.stdin.isatty():
        helptext('missing piped data')
        exit()

    data = sys.stdin.read()
    debug = False
    pretty = False
    quiet = False
    raw = False

    # options
    if '-d' in sys.argv:
        debug = True

    if '-p' in sys.argv:
        pretty = True

    if '-q' in sys.argv:
        quiet = True

    if '-r' in sys.argv:
        raw = True

    # parsers
    parser_map = {
        '--arp': jc.parsers.arp.parse,
        '--df': jc.parsers.df.parse,
        '--dig': jc.parsers.dig.parse,
        '--env': jc.parsers.env.parse,
        '--free': jc.parsers.free.parse,
        '--history': jc.parsers.history.parse,
        '--ifconfig': jc.parsers.ifconfig.parse,
        '--iptables': jc.parsers.iptables.parse,
        '--jobs': jc.parsers.jobs.parse,
        '--ls': jc.parsers.ls.parse,
        '--lsblk': jc.parsers.lsblk.parse,
        '--lsmod': jc.parsers.lsmod.parse,
        '--lsof': jc.parsers.lsof.parse,
        '--mount': jc.parsers.mount.parse,
        '--netstat': jc.parsers.netstat.parse,
        '--ps': jc.parsers.ps.parse,
        '--route': jc.parsers.route.parse,
        '--uname': jc.parsers.uname.parse,
        '--uptime': jc.parsers.uptime.parse,
        '--w': jc.parsers.w.parse
    }

    found = False

    if debug:
        for arg in sys.argv:
            if arg in parser_map:
                result = parser_map[arg](data, raw=raw, quiet=quiet)
                found = True
                break
    else:
        for arg in sys.argv:
            if arg in parser_map:
                try:
                    result = parser_map[arg](data, raw=raw, quiet=quiet)
                    found = True
                    break
                except:
                    parser_name = arg.lstrip('--')
                    jc.utils.error_message(f'{parser_name} parser could not parse the input data. Did you use the correct parser?\n         For details use the -d option.')
                    exit(1)

    if not found:
        helptext('missing or incorrect arguments')
        exit()

    # output resulting dictionary as json
    if pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == '__main__':
    main()

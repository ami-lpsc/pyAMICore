import sys, pyAMI.parser

print('# ' + pyAMI.parser.parse(['GetUserInfo', '-amiLogin=bar', '--foo']))

pyAMI.parser.shell_barrier = True

print('# ' + pyAMI.parser.parse(sys.argv[1: ]))

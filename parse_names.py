
fin = open('names.txt', 'r')
fout = open('url_extensions.txt', 'w')
num = '-1'
for line in fin.readlines():
    line = line.split('    \t\t')
    print(line)
    if len(line) > 1:
        fout.write(line[0].lower().replace(' ', '-').replace('(', '').replace(')', '').replace("'", '').replace('%', '').replace('&-', '').replace('?', '').replace('/', '').replace(',', '').replace('`', '').replace('---', '-').replace('--', '-') + '\n')
    else:
        num = line[0].replace('\t\n', '')
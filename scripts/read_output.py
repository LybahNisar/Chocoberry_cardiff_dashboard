with open('verify_output.txt', 'rb') as f:
    raw = f.read()

for enc in ['utf-16-le', 'utf-16', 'utf-8-sig', 'utf-8']:
    try:
        text = raw.decode(enc)
        break
    except:
        continue

lines = text.split('\n')
# Print in small chunks
for i in range(0, len(lines), 10):
    chunk = lines[i:i+10]
    for line in chunk:
        print(line.rstrip())
    print('---')

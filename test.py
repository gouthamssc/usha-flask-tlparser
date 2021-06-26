import subprocess
cmd = 'python3 website_generator.py'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, err = p.communicate() 
result = out.split(b'\n')
for lin in result:
    # if not lin.startswith('#'):
    print(lin.decode("utf-8"))
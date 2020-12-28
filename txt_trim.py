import os

dir=os.path.dirname(__file__)
with open((os.path.join(dir, 'bpchars.txt')), 'r+', newline='\n') as file:
    with open((os.path.join(dir, 'bpchars2.txt')), 'w', newline='\n') as file2:
        for line in file:
            print(line)
            if "Enemies" in line:
                print('good')
                file2.write(line)
            
           
                
                
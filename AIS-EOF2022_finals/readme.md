# Thoughts

### Summary

This particular CTF was a 2-day offline competition that featured Attack and Defense as well as King of the Hill modes. A total of 24 teams participated in this event.

### My thoughts

This is my first time participating in an offline CTF competition, which also happens to be my first time playing the Attack and Defense/King of the Hill mode in CTF. The first challenge of the competition was to find the location, which was at the 中華電信學院板橋所會館. Before the starting time, I had to figure out the transportation and the path to the destination XD.\
\
There is total 2 problems of Attack and Defense, and 2 other problems of King of the Hill. 

#### Attack and Defense -- NAS

This problem belongs to the Reverse/Pwn category. We were provided with the binary executable file of the service and the dockerfile used to build the service environment. The service is a NAS (Network Attached Storage) service that includes account management, upload and download functionality, and a debug feature. The points awarded in each round were divided into three parts: successful attacks, defense, and availability (ensuring the service remains operational).\
\
We didn't focus much on this problem as I believed that reversing the entire binary and finding the exploit would take up a lot of time, and we might miss other solvable problems. However, I discovered an exploit caused by the debug feature and managed to write a script to attack all the teams, thereby gaining partial score. Initially, I thought that everyone would patch this bug and it would be impossible to attack after some time. But surprisingly, nobody paid much attention to defense in this problem XD. As a result, we continued to score points on this problem without bothering to search for another exploit XDDD.

#### Attack and Defense -- Pyjail

This is my favourite problem among these challenges. This problem belongs to the Misc category. Basically, our service will receive the code from other team, and we must **examine** the code to protect our flag, but maintain the availability at the same time. In other words, we only can ban those invalid code (steal our flag) and must allow the valid code, otherwise we won't passed the test case and unable to update our patches.\
\
Our defense strategy is to filter all the invalid function call or the strings at the opcode levels.
```python
import dis
    for inst in dis.get_instructions(code):
        if inst.opcode == 100:
            if 'flag.txt' in str(inst.argval) or 'system' in str(inst.argval) or 'io' in str(inst.argval) or 'spawn' in str(inst.argval) or 'subprocess' in str(inst.argval) or 'pickle' in str(inst.argval) or 'getattr' in str(inst.argval) or 'base64' in str(inst.argval) or 'rot' in str(inst.argval) or 'open' in str(inst.argval) or 'read' in str(inst.argval) or 'write' in str(inst.argval) or 'sys' in str(inst.argval) or 'eval' in str(inst.argval) or 'exec' in str(inst.argval) or 'cat' in str(inst.argval) or 'builtins' in str(inst.argval):
                return False, "f2"
```
The attack strategy has customized to each team. Some team doesn't ban the library or function call such as base64, so we can bypass the jail by using base64 encode our exploit and decode it when using it (e.g. call exec or eval). Some team also doesn't ban about builtins property or the element, so that we can bypass the ban list of the function call by using builtins.

#### King of the Hill -- World of words

We abandoned this problem because it was too difficult for us to solve, which was categorized under Web. The task involved a web game about tank battles and scoring depended on securing a spot in the top 10 ranking for each round. To succeed in this problem, we needed to uncover a web exploit or a cryptography exploit that allowed us to obtain a powerful ability and gain an unfair advantage in the game to secure top ranking.

#### King of the Hill -- Jeopardy

My other two teammates focused on this problem since I am not very proficient in cryptography. The problem was structured like a jeopardy, but with a twist; it leaked some information, specifically the algorithm index of each round (not the details). To obtain points, we had to deduce the algorithm details based on the results of each round and predict the results of the next round before it began, allowing us to guess correctly and score points.

#### Picture
![](3.jpg)
![](2.jpg)\
I am the one who wearing the black shirt and black mask XD
![](1.jpg)


#### Results

We get 12th rank!
![](final_result.png)
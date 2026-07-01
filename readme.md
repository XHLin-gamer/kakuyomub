# Kakuyomub
<p align="center">
  <img src="icon.png" style="width:30%;" />
</p>
Usage:

Make sure python is available, then
```bash
git clone https://github.com/XHLin-gamer/kakuyomub.git
pip install -r requirement.txt
python -m kakuyomub.main WORK_ID 
```
or if you want to point the downloaded file to a folder:
```bash
python -m kakuyomub.main WORK_ID --path C:\Users\xhaug\OneDrive\Desktop
```

```bash
pip install kakuyomub
>>> kakuyomub.download(16817330650993330082, "./")
```
replace the ```WORK_ID``` with the カクヨム work id


## EXAMPLE
the url of 「クーデレなセフレと小悪魔な後輩が義妹になったので距離を置きたい。」 is https://kakuyomu.jp/works/16817330668128729529

The id of the work is the last trunk of the url, which is 16817330668128729529
```bash
# use the id to download work
python -m kakuyomub.main 16817330668128729529
```

and the result is as:
![alt text](image.png)

## 学習指導要領コード整形ツール

学習指導要領をコード体系に沿ってツリー構造に展開した上で、ツリー上で連鎖する親項目の記述内容を引き継いで、コードとそれが意味する教科・指導要領の内容を1:1で表現します。

### 解説 

[blog](https://hommalab.io/posts/python/mext-guide-code-organizer/)

### Install

On local computer

```
$ python -m venv env
$ source env/bin/activate
$ (env) pip install -r requirements.txt --index-url="https://pypi.python.org/simple"
$ deactivate
```

### Run

On the virtual environment, run `python ./mext_guide_code_tree.py <csv file path>`

```
$ source env/bin/activate
$ (env) python ./mext_guide_code_tree.py ./data/000102025_JH_83V11.cv
```

- Input(文科省のサイトからダウンロードしたCSVファイル): 
  - (Sample) ./data/000102025_83V11_JH.csv

- Output:
  - (Sample) ./data/000102025_83V11_JH_out.csv


### Requirement

- python3
- For python libraries, see `requirements.txt`

### Links

- [学習指導要領コードのコード表（全体版）について](https://www.mext.go.jp/a_menu/other/data_00002.htm)
# 公式からpython3.7 linuxイメージをpull
FROM python:3.7

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

# ホストのrequirementsをコンテナの作業ディレクトリにコピー
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt


# ホストのカレントディレクトリ（現在はappディレクトリ）を作業ディレクトリにコピー
COPY . /usr/src/app/

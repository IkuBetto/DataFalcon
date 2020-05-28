# 競馬 x データファルコン
# ディレクトリ説明
基本的にソースコードはsrc配下の物を編集する。 ※ 他ファイルはDockerのコンテナを立ち上げるに必要なものになるので、基本的に編集は行わない
# Django-Docker
DockerでDjangoを作る時に使うレポジトリです。
# Docker起動方法
コマンドはdockerコマンドを使う。 ファーストステップとして、dockerファイルからコンテナを立ち上げる。 Docker起動は、作業中のディレクトリにはいり、下記を実行致します。
'''
$ docker-compose up -d --build
'''
今回はdockerの設定上、下記のローカルIP, portでサーバーが立ち上がるようになっている。
'''
127.0.0.1:8000
'''
アクセスすると、初期画面からlogin機能のついたページへリダイレクトされる
# コンテナ内でのコマンド実行方法
コンテナ内でのコマンド実行は下記で行うことができます。
'''
$ docker-compose run python 実行したいコマンド
'''
一つ目の引数である"python"は、docker-cimpose.ymlファイルのサービス名である"python"内での実行を意味しています。 下記が具体例です。

例：make migrations方法
'''
$ docker-compose run python python manage.py makemigrations
'''
例：migrate方法
'''
$ docker-compose run python python manage.py migrate
'''
# モデルに初期値を入れる方法
モデルに初期値を入れるには、下記の手順をふみます

1. アプリケーションフォルダの中にfixturesフォルダを作る
2. fixturesフォルダの中に"{テーブル名}.json"を作成する
3. 下記コマンドを実行する
'''
$ docker-compose run python python manage.py loaddata {テーブル名ファイル}.json
'''
# 初期データを入れるファイルを作成したため、開発前にこちちらのコマンドを実行
'''
$ docker-compose run python python manage.py loaddata users.json
'''
このコマンドを実行することで、テストデータが入る
# テストデータを入れた後
テストデータ挿入後 ログイン画面にて（/auth/login)
'''
メールアドレス: test@gmail.com
パスワード: 12345
'''
こちらを入力して、ログインする。
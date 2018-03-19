Github のプルリクエスト取得スクリプト

# 動作環境

OS: Mac OS 10.11.6
Python 3系
percol

## 事前インストール

```
> pip install requests
```

## アクセストークン

1. Github のアクセストークンを取得する。

1. .netrc ファイルにトークン情報を記述する。

```
machine api.github.com
    login your_account
    password your_token
```

## 実行

review.sh を実行する








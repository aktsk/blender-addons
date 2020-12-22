# blender-addons

## 利用方法（利用者向け）

`scripts/addons` フォルダの中にそれぞれのアドオンのためのフォルダがあります。
さらにその中の `README.md` というファイルに、使い方やインストール方法が書いてあります。

## 開発者向け

利用時には気にしなくても大丈夫です！
開発時には、以下のようにすると Addon を開発しやすいです。

## セットアップ時

```sh
# コマンドラインから起動をするとログ等の出力が見れます
$ /Applications/Blender.app/Contents/MacOS/Blender
```

`Prefarence > Fole Paths > Data > Scripts` に `/path-to-this-repo/scripts/` をセットする.

## 開発時

```sh
# コマンドラインから起動をするとログ等の出力が見れます
$ /Applications/Blender.app/Contents/MacOS/Blender
```

1. コードを編集する
2. `Prefarence > Addons > Testing` 内で `Object: <アドオン名>` を無効化して再度有効にする.
3. 検証したら1に戻る

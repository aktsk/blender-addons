# Size Presets

Select grease pencil brush size from presets.
グリースペンシルのブラシサイズをプリセットから選べるようにするアドオン

## インストール方法

1. このREADMEが設置されている `size_presets` フォルダを丸ごとzipファイルに圧縮してください
2. Blender の `Preference > Addons` で `Install` から作成したzipファイルを選択し、インストールします

## 使い方

グリースペンシル使用時に `Properties > Active Tool and Workspace Settigns > Size Presets` から `Size Presets` パネルでプリセットを選択できます。

キーボードショートカットを使用して、現在のブラシサイズをプリセットにしたがい増減させることができます。
デフォルトの設定では以下の通りです。

- `[` キーで `ブラシサイズアップ`
- `]` キーで `ブラシサイズダウン`

この設定は変更することができます。`Prefrerennces > Keymap` から、以下のidを任意のキーマップに設定してください。

- `brush.increase_brush_size` で `ブラシサイズアップ`
- `brush.decrease_brush_size` で `ブラシサイズダウン`

## プリセットの内容を変更したい場合

`size_presets/presets` フォルダの `presets.json` を編集してください。

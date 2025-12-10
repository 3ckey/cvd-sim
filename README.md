# 色覚シミュレーション（Machado 2009 ベース）

画像の「色の見え方の違い」をブラウザ上でシミュレートする、静的な Web アプリケーションです。  
Protan / Deutan / Tritan（1型 / 2型 / 3型）の色覚タイプを、Machado 2009 のモデルを元に近似的に再現します。

> ⚠️ このツールは医療・診断用途ではありません。  
> 実際の見え方には個人差があり、「だいたいの傾向を知るための一例」として利用してください。

---

## 特長

- ブラウザだけで動作（バックエンド不要、静的ホスティングで OK）
- クリップボードから画像を貼り付け（対応ブラウザのみ）／ローカルファイルから画像を読み込み
- Protan / Deutan / Tritan の 3 種類の色覚タイプを並べて表示
- severity スライダーで「見え方の変化の度合い」を 0.00〜1.00 の範囲で調整
- PC / スマートフォン双方に対応したシンプルな UI
- Machado 2009 / Colour ライブラリに基づく行列を JSON で外出しして利用

---

## デモ

GitHub Pages などの静的ホスティングにデプロイすることで、ブラウザから直接利用できます。

例（デプロイ後に置き換えてください）:

- <https://3ckey.github.io/cvd-sim/>

ローカルで試したい場合は、下記の「ローカルでの動作確認」を参照してください。

---

## 自分の環境でホストするには

このプロジェクトは、静的ファイルとしてホスティングするだけで動作します。  
GitHub Pages や社内の静的ファイルサーバーなどにアップロードして利用できます。

GitHub Pages にデプロイする場合の一例:

1. このリポジトリをフォークするか、クローンして自分のリポジトリとして作成します。
2. `public/` ディレクトリ以下のファイルを GitHub Pages の公開ブランチ（例: `gh-pages`）のルートに配置します。
3. リポジトリ設定で GitHub Pages の公開ブランチを `gh-pages` に設定します。
4. 数分待つと、`https://{your-account}.github.io/{your-repo}/` のような URL からアクセスできるようになります。

---

## 想定する用途

- グラフ・チャート・UI のスクリーンショットを読み込んで、  
  「色に頼りすぎていないか」「情報が伝わりにくくなっていないか」をざっくり確認する
- カラーユニバーサルデザインを説明する際の補助ツールとして、  
  スライドやハンズオンと組み合わせて使う
- 自分の作った Web ページやアプリの配色を検討する際の参考として使う

---

## 動作環境

### ブラウザ側

- クリップボード API から画像を読み取るには、比較的モダンなブラウザが必要です
  - 例: 最新の Chrome / Edge / Firefox など
  - 対応していない環境でも、「ファイルを選択」から画像を読み込めば利用可能です
- HTTPS もしくは `http://localhost` からのアクセスを想定しています

### Python / 開発環境側（任意）

行列 JSON（`machado_matrices.json`）を自分で再生成したい場合に必要になります。  
アプリを「使うだけ」であれば、JSON がリポジトリに含まれていれば必須ではありません。

- Python 3.11〜3.14（`colour-science==0.4.7` のサポート範囲に合わせています）
- pip でインストール可能な環境

---

## ディレクトリ構成（例）

```text
.
├── public/
│   ├── index.html              # メインの UI
│   ├── js/
│   │   ├── main.js             # 画面操作・キャンバス描画・イベント処理
│   │   └── color-sim.js        # 色覚シミュレーション処理（Machado 行列の適用）
│   └── data/
│       └── machado_matrices.json  # Machado 2009 ベースの CVD 行列プリセット
├── scripts/
│   ├── export_machado_matrices.py # Colour から JSON を生成するスクリプト
│   └── requirements.txt           # 開発用 Python 依存関係
├── .devcontainer/ ...             # （任意）Dev Container 設定
├── LICENSE
└── README.md
```

---

## インストールとセットアップ

### 1. リポジトリを取得

```bash
git clone https://github.com/3ckey/cvd-sim.git
cd cvd-sim
```

### 2. （任意）行列 JSON の再生成

すでに `public/data/machado_matrices.json` がコミットされている場合、  
Web アプリとして利用するだけならこのステップは不要です。

行列を自分で生成し直したい場合は、仮想環境を作成して `scripts/export_machado_matrices.py` を実行します。

```bash
cd scripts

python -m venv .venv
source .venv/bin/activate  # Windows の場合: .venv\Scripts\activate

pip install -r requirements.txt

python export_machado_matrices.py
```

成功すると、`public/data/machado_matrices.json` が生成（または更新）されます。

> `scripts/requirements.txt` には、以下のような依存関係が含まれています：
> - `colour-science==0.4.7`
> - `numpy==2.3.5`

---

## ローカルでの動作確認

`public` ディレクトリを静的ファイルとして配信できれば動作します。  
簡単な方法として、Python の簡易 HTTP サーバーが利用できます。

```bash
cd public

# Python 3 系
python -m http.server 8080
```

ブラウザで <http://localhost:8080> を開くと、アプリを試すことができます。

---

## 使い方

### 1. 画像の読み込み

画面上部に以下の操作があります：

- **📋 クリップボードから画像を貼り付け**
  - 対応ブラウザでは、スクリーンショットや画像をクリップボードにコピーしてから
    このボタンを押すことで、クリップボード上の画像を読み込めます。
- **ファイルを選択**
  - ローカルの画像ファイル（PNG / JPEG など）を選択して読み込みます。

読み込みに成功すると、画面左上の「オリジナル」パネルに元画像が表示されます。

> ブラウザや環境によっては、クリップボードからの貼り付けが動作しない場合があります。  
> その場合は「ファイルを選択」から読み込んでください。

### 2. 色覚シミュレーションの確認

- 「Protan（1型）」「Deutan（2型）」「Tritan（3型）」の各パネルには、  
  それぞれの色覚タイプをシミュレーションした画像が表示されます。
- これらは Machado 2009 のモデルを元にした 3×3 行列と、
  sRGB / 線形 RGB の変換を組み合わせて計算しています。

### 3. severity スライダー

画面上部の `severity` スライダーで、シミュレーションの「度合い」を調整できます。

- `0.00` に近いほど、元の画像に近い色
- `1.00` に近いほど、各タイプの色の特徴を強くシミュレート

実際の見え方は人によって異なるため、

- 「特定の人の見え方そのもの」を再現するものではなく
- 「こういう傾向の違いがありうる」という目安として使うツールです

---

## 実装メモ（技術的な補足）

- 画像は `<canvas>` 上に描画し、`getImageData` / `putImageData` を用いてピクセル単位で変換しています。
- 変換時には sRGB → 線形 RGB 変換を行い、Machado 2009 ベースの 3×3 行列を適用した後、線形 RGB → sRGB に戻しています。
- severity は 0.0〜1.0 の連続値として扱い、`machado_matrices.json` に含まれる  
  離散的な行列プリセットの間を線形補間して利用しています。
- 画面幅が狭い（主にスマートフォン）場合は、1 列レイアウトに自動的に切り替わるよう CSS で制御しています。

---

## ライセンス

- このリポジトリ全体のライセンスは **MIT License** です。  
  詳細は [`LICENSE`](./LICENSE) を参照してください。
- このプロジェクトでは、以下の第三者ソフトウェアに依存しています：
  - **Colour (Colour Science for Python)**  
    - Machado 2009 ベースの色覚シミュレーション行列  
      `CVD_MATRICES_MACHADO2010` を使用しています。
    - Colour は **BSD-3-Clause ライセンス** で公開されています。
    - 詳細なライセンス条文は `LICENSE` の「Third-party licenses」セクションを参照してください。

---

## 参考文献

- Gustavo M. Machado, Manuel M. Oliveira, and Leandro A. F. Fernandes,  
  *“A Physiologically-based Model for Simulation of Color Vision Deficiency”*,  
  IEEE Transactions on Visualization and Computer Graphics (TVCG), 2009.
- [Colour – Colour Science for Python](https://www.colour-science.org/)

---

### 備考

将来的に、ドラッグ＆ドロップでの画像読み込みや、多言語対応・ダークテーマ対応なども検討していますが、現時点ではシンプルな画像シミュレーターとしての基本機能に絞っています。

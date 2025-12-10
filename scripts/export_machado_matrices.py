import json
from pathlib import Path

import colour  # pip install colour-science

def main():
    # 1. CVD_MATRICES_MACHADO2010 を取得
    #   典型的には:
    #   colour.CVD_MATRICES_MACHADO2010["Protanomaly"][severity] -> 3x3行列
    cvd_matrices = colour.CVD_MATRICES_MACHADO2010

    # 2. ライブラリ側のキー名 -> JSON側のキー名 のマッピング
    mode_map = {
      "Protanomaly":  "protan",
      "Deuteranomaly":"deutan",
      "Tritanomaly":  "tritan",
    }

    # 3. JSON用の dict を組み立てる
    json_root: dict[str, dict[str, list[list[float]]]] = {}

    for lib_mode_name, json_mode_name in mode_map.items():
        if lib_mode_name not in cvd_matrices:
            print(f"Warning: {lib_mode_name} not found in CVD_MATRICES_MACHADO2010")
            continue

        table = cvd_matrices[lib_mode_name]
        mode_dict: dict[str, list[list[float]]] = {}

        # severityキーが float の場合と str の場合があるので、一旦floatにしてソートする
        severity_values = []
        for sev_key in table.keys():
            try:
                sev = float(sev_key)
            except (TypeError, ValueError):
                # もし"0"や"1"などの文字列でなければスキップor警告
                print(f"Warning: cannot parse severity key {sev_key!r} for {lib_mode_name}")
                continue
            severity_values.append(sev)

        severity_values = sorted(set(severity_values))

        for sev in severity_values:
            # ライブラリ側のキーは文字列のこともあるので str(sev) と sev 両方試す
            mats = None
            if sev in table:
                mats = table[sev]
            else:
                key_str = str(sev)
                if key_str in table:
                    mats = table[key_str]
                else:
                    # "0.0" vs "0" の食い違いに備えて少し工夫
                    key_str_alt = f"{sev:.1f}"
                    mats = table.get(key_str_alt)

            if mats is None:
                print(f"Warning: matrix not found for {lib_mode_name} severity {sev}")
                continue

            # Pythonオブジェクト -> JSON friendly (リストのリスト) に変換しておく
            # colour の行列型がnumpy配列の可能性もあるので list() 化しておく
            mat_3x3 = [list(row) for row in mats]

            # JSONのキーは文字列にしておく（スライダーとのマッチを考えて小数1桁など）
            sev_key = f"{sev:.1f}"
            mode_dict[sev_key] = mat_3x3

        json_root[json_mode_name] = mode_dict

    # 4. ファイルに書き出す
    project_root = Path(__file__).resolve().parent.parent
    out_path = project_root / "public" / "data" / "machado_matrices.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(json_root, f, ensure_ascii=False, indent=2)

    print(f"Exported JSON to {out_path.resolve()}")

if __name__ == "__main__":
    main()

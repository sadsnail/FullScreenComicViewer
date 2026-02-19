# 多语言文案 / Localization

本目录存放各语言的 UI 文案，按「语言代码 + `.json`」命名（如 `zh.json`、`en.json`）。

## 切换语言

在 **`kantu_config.txt`** 第二行写入语言代码即可：

- `zh` — 简体中文（默认）
- `en` — English

示例：

```
D:\Comics
en
```

## 新增语言（配置化添加）

1. **复制现有 JSON**  
   复制 `en.json` 或 `zh.json`，重命名为 `语言代码.json`（如 `ja.json`）。

2. **翻译文案**  
   只改 JSON 中的值，不要改键名。键名与代码中的 `i18n.t("key")` 对应。

3. **登记语言代码**  
   在 **`i18n.py`** 中，将新代码加入元组：

   ```python
   SUPPORTED = ("zh", "en", "ja")  # 添加 ja
   ```

4. **（可选）配置读写**  
   - `config.load_language()` 会读取配置第二行，无需改 config 即可支持新代码。  
   - 若希望「仅允许部分代码写入配置」，可在 `config.save_language()` 中增加校验。

完成后，用户在 `kantu_config.txt` 第二行填写 `ja` 即可使用日文界面。

---

This folder holds per-language UI strings as `lang_code.json`. Set the second line of `kantu_config.txt` to `en` or `zh` to switch language. To add a new language: copy an existing JSON, translate the values, and add the code to `SUPPORTED` in `i18n.py`.

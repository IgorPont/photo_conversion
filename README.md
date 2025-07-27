# 🖼️ Photo Conversion CLI

Утилита на Python для рекурсивной обработки фотографий из директории `DCIM`:

- удаление `.NEF` файлов
- преобразование `.HEIC` в `.JPG` (с удалением оригинала)
- переименование `.JPG` файлов с объединением в одну директорию
- CLI-интерфейс на базе [Typer](https://typer.tiangolo.com/)
- поддержка `--dry-run`, логирование, подробный вывод

## 📦 Установка зависимостей

```bash
poetry install
```

## 🚀 Команды CLI

### 🔧 Обработка изображений (`process`)

Удаление `.NEF` и преобразование `.HEIC` → `.JPG` с возможностью dry-run и логирования:

```bash
# Базовая обработка
poetry run python -m photo_converter.cli process objects_to_convert/DCIM

# Режим dry-run (только логирование, без изменений)
poetry run python -m photo_converter.cli process objects_to_convert/DCIM --dry-run

# Подробный вывод
poetry run python -m photo_converter.cli process objects_to_convert/DCIM -v

# Лог в файл
poetry run python -m photo_converter.cli process objects_to_convert/DCIM --log-file=log.txt
```

### 🔄 Переименование и объединение (`rename`)

Сортировка `.JPG` файлов по подпапкам, переименование в `1.jpg`, `2.jpg`, … и копирование в новую общую папку:

```bash
# Сбор и переименование файлов
poetry run python -m photo_converter.cli rename objects_to_convert/DCIM output

# Режим dry-run
poetry run python -m photo_converter.cli rename objects_to_convert/DCIM output --dry-run
```

> 💡 Папка `output` будет содержать результат с именем вроде `2025-07-26_renamed_images`.

## 🧪 Тестирование

```bash
poetry run pytest -v
```

## 📝 Лицензия

MIT (см. `LICENSE.md`)

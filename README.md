# 🖼️ Photo Conversion CLI

Утилита на Python для рекурсивной обработки фотографий:

- удаление `.NEF` файлов
- преобразование `.HEIC` в `.JPG` (с удалением оригинала)
- CLI-интерфейс на [Typer](https://typer.tiangolo.com/)
- поддержка `--dry-run`, логирование, подробный вывод

## 📦 Установка зависимостей

```bash
poetry install
```

## 🚀 Запуск

```bash
# Базовая обработка
poetry run python -m photo_converter.cli objects_to_convert/DCIM

# Режим dry-run (только логирование, без изменений)
poetry run python -m photo_converter.cli objects_to_convert/DCIM --dry-run

# Подробный вывод
poetry run python -m photo_converter.cli objects_to_convert/DCIM -v

# Лог в файл
poetry run python -m photo_converter.cli objects_to_convert/DCIM --log-file=log.txt
```

## 🧪 Тестирование

```bash
poetry run pytest -v
```

## 📝 Лицензия

MIT (см. `LICENSE.md`)

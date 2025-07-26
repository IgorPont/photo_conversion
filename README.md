# 🖼️ Photo Conversion CLI

Утилита на Python для рекурсивной обработки фотографий:
- удаление `.NEF` файлов
- преобразование `.HEIC` в `.JPG`
- CLI-интерфейс на Typer
- логирование и поддержка `--dry-run`

## 📦 Установка зависимостей

```bash
poetry install
```

## 🚀 Запуск

```bash
# Базовая обработка
poetry run python photo_converter/cli.py process objects_to_convert/DCIM

# Режим dry-run (только вывод без удаления/конверсии)
poetry run python photo_converter/cli.py process objects_to_convert/DCIM --dry-run

# Подробный вывод
poetry run python photo_converter/cli.py process objects_to_convert/DCIM -v

# Логирование в файл
poetry run python photo_converter/cli.py process objects_to_convert/DCIM --log-file=log.txt
```

## 🧪 Тестирование

```bash
poetry run pytest -v
```

## 📝 Лицензия

MIT (см. `LICENSE.md`)

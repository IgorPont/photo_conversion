# 📸 Photo Conversion CLI

Утилита на Python для обработки RAW и HEIC изображений в структуре папки `DCIM`.

Позволяет:
- удалять `.NEF` файлы (Nikon RAW)
- конвертировать `.HEIC` в `.JPG` с удалением исходников
- запускать в dry-run режиме
- логировать в файл

---

## 📦 Установка

Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями.

### 1. Клонируй репозиторий

```bash
git clone https://example.com/your/project.git
cd photo_conversion
```

### 2. Установи зависимости

```bash
poetry install
```

---

## 🚀 Запуск

### 🛠 Обычная обработка

```bash
poetry run python photo_converter/cli.py process objects_to_convert/DCIM
```

### 🔍 Dry-run (ничего не изменяет)

```bash
poetry run python photo_converter/cli.py process objects_to_convert/DCIM --dry-run
```

### 📋 Подробный вывод

```bash
poetry run python photo_converter/cli.py process objects_to_convert/DCIM -v
```

### 📝 С выводом в лог-файл

```bash
poetry run python photo_converter/cli.py process objects_to_convert/DCIM --log-file=log.txt
```

Можно комбинировать:

```bash
poetry run python photo_converter/cli.py process objects_to_convert/DCIM --dry-run -v --log-file=run.log
```

---

## 🧪 Тестирование

Тесты написаны на `pytest`, находятся в `test/`.

Запуск:

```bash
poetry run pytest -v
```

---

## 📁 Структура проекта

```
photo_conversion/
├── objects_to_convert/         # Исходные данные (DCIM)
├── photo_converter/            # Основной код
│   ├── cli.py                  # CLI-утилита
│   └── del_nef_and_covert_heic.py
├── test/                       # Тесты
├── pyproject.toml              # Poetry-конфигурация
├── poetry.lock
└── README.md                   # 📘 Этот файл
```

---

## 🛠 Зависимости

- [Pillow](https://pillow.readthedocs.io/)
- [pillow-heif](https://github.com/strukturag/libheif)
- [typer](https://typer.tiangolo.com/)
- [pytest](https://pytest.org/) — для тестов
- [black](https://github.com/psf/black) — для автоформатирования

---

## 🧑‍💻 Автор

igor_pont (pontigor11@gmail.com)

---

## 📜 Лицензия

MIT

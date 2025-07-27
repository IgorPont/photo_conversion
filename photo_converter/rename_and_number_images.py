"""
Модуль для объединения и переименования JPEG-изображений из подпапок директории DCIM.

Основной сценарий:
    - Рекурсивный проход по подпапкам DCIM в отсортированном порядке
    - В каждой папке сортировка файлов по имени
    - Копирование всех файлов с расширением `.jpg` и `.jpeg` в новую директорию
    - Переименование файлов в формате 1.jpg, 2.jpg, ... (сквозная нумерация)
    - Название итоговой папки содержит текущую дату (например, 2025-07-26_renamed_images)

Поддерживает режим dry-run, в котором выполняется только логирование без копирования файлов.

Используется как часть CLI-команды `rename` (см. photo_converter.cli).
"""

import logging
from datetime import datetime
from pathlib import Path


def rename_and_collect_images(dcim_path: Path, output_root: Path, dry_run: bool = False) -> None:
    """
    Поочерёдно обходит отсортированные подпапки DCIM и:
      - сортирует изображения внутри каждой папки по имени
      - копирует и переименовывает все JPEG-файлы (jpg, jpeg) в формат 1.jpg, 2.jpg, ...
      - сохраняет их в общую новую папку, названную по дате выполнения

    :param dcim_path: Путь к директории DCIM
    :param output_root: Корневая папка, где будет создана итоговая папка
    :param dry_run: Если True — только логирует действия, не копируя файлы
    """
    if not dcim_path.exists() or not dcim_path.is_dir():
        logging.warning(f"Путь {dcim_path} не существует или не является директорией.")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = output_root / f"{date_str}_renamed_images"

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"📁 Чтение из: {dcim_path.resolve()}")
    logging.info(f"📦 Итоговая папка: {output_dir.resolve()}")

    counter = 1
    folders = sorted([f for f in dcim_path.iterdir() if f.is_dir()])
    total_images = 0

    for folder in folders:
        # Учитываем все возможные расширения JPEG
        jpeg_files = sorted(
            f for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg"}
        )

        for file in jpeg_files:
            new_filename = f"{counter}.jpg"
            destination = output_dir / new_filename

            if dry_run:
                logging.info(f"[dry-run] {file.name} → {destination.name}")
            else:
                try:
                    destination.write_bytes(file.read_bytes())
                    logging.info(f"📷 {file.name} → {destination.name}")
                except Exception as e:
                    logging.error(f"❌ Ошибка при копировании {file}: {e}")

            counter += 1
            total_images += 1

    logging.info("📊 Завершено.")
    logging.info(f"  Обработано папок          : {len(folders)}")
    logging.info(f"  Всего найдено изображений : {total_images}")
    logging.info(f"  Скопировано и переименовано: {counter - 1}")

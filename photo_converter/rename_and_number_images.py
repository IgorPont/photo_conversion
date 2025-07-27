"""
Модуль для объединения и переименования .JPG изображений из вложенных папок DCIM.

Функция `rename_and_collect_images`:
    - поочерёдно обходит отсортированные папки внутри DCIM
    - внутри каждой папки сортирует .JPG-файлы по имени
    - копирует изображения в новую папку с переименованием (1.jpg, 2.jpg, ...)
    - имя новой папки формируется по текущей дате и добавке `_renamed_images`
    - поддерживает режим dry-run
"""

import logging
from datetime import datetime
from pathlib import Path


def rename_and_collect_images(dcim_path: Path, output_root: Path, dry_run: bool = False) -> None:
    """
    Поочерёдно обходит отсортированные подпапки DCIM и:
      - сортирует изображения внутри папки по имени
      - копирует и переименовывает изображения в формат 1.jpg, 2.jpg, ...
      - сохраняет в общую новую папку, названную по дате выполнения

    :param dcim_path: Путь к директории DCIM
    :param output_root: Корневая папка, где будет создана итоговая папка
    :param dry_run: Если True — выводит действия без изменения файлов
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
    total_found = 0
    folders = sorted([f for f in dcim_path.iterdir() if f.is_dir()])

    for folder in folders:
        jpg_files = sorted(f for f in folder.iterdir() if f.suffix.lower() == ".jpg")
        total_found += len(jpg_files)

        for file in jpg_files:
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

    logging.info("📊 Завершено.")
    logging.info(f"  Обработано папок         : {len(folders)}")
    logging.info(f"  Всего изображений найдено: {total_found}")
    logging.info(f"  Скопировано и переименовано: {counter - 1}")

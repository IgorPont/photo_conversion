"""
Модуль бизнес-логики для обработки изображений в директории DCIM.

Выполняет:
    - рекурсивный обход всех поддиректорий
    - удаление файлов с расширением `.NEF`
    - конвертацию файлов `.HEIC` в `.JPG` (с удалением исходников)
    - поддержку dry-run режима
    - возврат статистики обработки

Предназначен для использования из CLI или в качестве импортируемого модуля.
"""

import logging
from pathlib import Path
from PIL import Image
import pillow_heif

# Регистрируем поддержку формата HEIC для Pillow
pillow_heif.register_heif_opener()


def process_dcim(dcim_path: Path, dry_run: bool = False) -> dict | None:
    """
    Рекурсивно обрабатывает файлы в указанной директории DCIM:
        - удаляет `.NEF` файлы
        - конвертирует `.HEIC` в `.JPG` и удаляет исходники

    :param dcim_path: путь к директории DCIM
    :param dry_run: если True, действия не выполняются, только логируются
    :return: словарь со статистикой обработки или None, если путь недоступен
    """
    if not dcim_path.exists() or not dcim_path.is_dir():
        logging.warning(f"Путь {dcim_path} не существует или не является директорией.")
        return None

    logging.info(f"📁 Обработка директории: {dcim_path.resolve()}")

    # Статистика
    total_before = sum(1 for _ in dcim_path.rglob("*") if _.is_file())
    nef_deleted = 0
    heic_converted = 0

    for file in dcim_path.rglob("*"):
        if not file.is_file():
            continue

        suffix = file.suffix.lower()

        if suffix == ".nef":
            if dry_run:
                logging.info(f"[dry-run] 🗑️  Будет удалён: {file}")
            else:
                try:
                    file.unlink()
                    nef_deleted += 1
                    logging.info(f"🗑️  Удалён .NEF файл: {file}")
                except Exception as e:
                    logging.error(f"❌ Ошибка при удалении {file}: {e}")

        elif suffix == ".heic":
            jpg_path = file.with_suffix(".jpg")
            if dry_run:
                logging.info(f"[dry-run] ✅ Будет конвертирован: {file} → {jpg_path}")
            else:
                try:
                    with Image.open(file) as img:
                        rgb_img = img.convert("RGB")
                        rgb_img.save(jpg_path, "JPEG", quality=95)
                    file.unlink()
                    heic_converted += 1
                    logging.info(f"✅ Конвертирован и удалён: {file} → {jpg_path}")
                except Exception as e:
                    logging.error(f"❌ Ошибка при конвертации {file}: {e}")

    total_after = sum(1 for _ in dcim_path.rglob("*") if _.is_file())

    return {
        "total_before": total_before,
        "nef_deleted": nef_deleted,
        "heic_converted": heic_converted,
        "total_after": total_after if not dry_run else total_before,
    }


if __name__ == "__main__":
    # Запуск для ручной проверки
    dcim_dir = Path("objects_to_convert/DCIM")
    stats = process_dcim(dcim_dir)
    if stats:
        logging.info("📊 Статистика обработки:")
        logging.info(f"  Всего файлов ДО обработки: {stats['total_before']}")
        logging.info(f"  Удалено .NEF файлов      : {stats['nef_deleted']}")
        logging.info(f"  Конвертировано .HEIC     : {stats['heic_converted']}")
        logging.info(f"  Всего файлов ПОСЛЕ       : {stats['total_after']}")

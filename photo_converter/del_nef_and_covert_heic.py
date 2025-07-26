import logging
from pathlib import Path
from PIL import Image
import pillow_heif

# Регистрируем поддержку формата HEIC для Pillow
pillow_heif.register_heif_opener()

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(message)s")


def process_dcim(dcim_path: Path) -> None:
    """
    Обрабатывает все подкаталоги папки DCIM:
        - удаляет файлы с расширением `.NEF`
        - конвертирует `.HEIC` в `.JPG` и удаляет исходник

    Также ведёт подсчёт количества обработанных файлов.
    """
    if not dcim_path.exists() or not dcim_path.is_dir():
        logging.warning(f"Путь {dcim_path} не существует или не является директорией.")
        return

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
            try:
                file.unlink()
                nef_deleted += 1
                logging.info(f"🗑️  Удалён .NEF файл: {file}")
            except Exception as e:
                logging.error(f"❌ Ошибка при удалении {file}: {e}")

        elif suffix == ".heic":
            jpg_path = file.with_suffix(".jpg")
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

    # Финальный отчёт
    logging.info("📊 Статистика обработки:")
    logging.info(f"  Всего файлов ДО обработки: {total_before}")
    logging.info(f"  Удалено .NEF файлов      : {nef_deleted}")
    logging.info(f"  Конвертировано .HEIC     : {heic_converted}")
    logging.info(f"  Всего файлов ПОСЛЕ       : {total_after}")


if __name__ == "__main__":
    dcim_dir = Path("objects_to_convert/DCIM")
    process_dcim(dcim_dir)

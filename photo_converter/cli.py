import logging
from pathlib import Path
from PIL import Image
import pillow_heif
import typer

# Регистрируем поддержку HEIC для Pillow
pillow_heif.register_heif_opener()


def configure_logging(verbose: bool, log_file: Path | None):
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(str(log_file), encoding="utf-8"))
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=handlers,
    )


def main(
        dcim_path: Path = typer.Argument(..., help="Путь к директории DCIM"),
        dry_run: bool = typer.Option(False, "--dry-run", help="Только логировать действия, ничего не менять"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Подробный вывод"),
        log_file: Path = typer.Option(None, "--log-file", help="Путь к лог-файлу"),
):
    """
    Удаляет .NEF и конвертирует .HEIC → .JPG с удалением исходников.
    """
    configure_logging(verbose, log_file)

    if not dcim_path.exists() or not dcim_path.is_dir():
        logging.error(f"Путь {dcim_path} не существует или не является директорией.")
        raise typer.Exit(code=1)

    logging.info(f"📁 Обработка: {dcim_path.resolve()}")

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
                    logging.info(f"🗑️  Удалён: {file}")
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

    logging.info("📊 Статистика:")
    logging.info(f"  Всего ДО     : {total_before}")
    logging.info(f"  Удалено .NEF : {nef_deleted}")
    logging.info(f"  HEIC → JPG   : {heic_converted}")
    logging.info(f"  Всего ПОСЛЕ  : {total_after if not dry_run else total_before}")


if __name__ == "__main__":
    typer.run(main)

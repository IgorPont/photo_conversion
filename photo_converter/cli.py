"""
CLI-интерфейс для обработки изображений в директории DCIM.

Поддерживает:
    - удаление файлов .NEF
    - конвертацию .HEIC → .JPG с удалением исходников
    - объединение всех .JPG файлов в одну папку с переименованием (1.jpg, 2.jpg, ...)
    - dry-run режим, логгирование и подробный вывод

Примеры:
    poetry run python -m photo_converter.cli process objects_to_convert/DCIM
    poetry run python -m photo_converter.cli rename objects_to_convert/DCIM output
"""

import logging
from pathlib import Path
import typer
from photo_converter.del_nef_and_covert_heic import process_dcim
from photo_converter.rename_and_number_images import rename_and_collect_images

# Создаём CLI-приложение
app = typer.Typer(help="Утилита для обработки изображений: удаление .NEF, конвертация .HEIC, переименование .JPG")


def configure_logging(verbose: bool, log_file: Path | None):
    """
    Настраивает логирование в консоль и (опционально) в файл.

    :param verbose: если True — устанавливается уровень DEBUG, иначе INFO
    :param log_file: путь к лог-файлу, если указан — лог сохраняется и туда
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(str(log_file), encoding="utf-8"))
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=handlers,
    )


@app.command("process")
def process_images(
        dcim_path: Path = typer.Argument(..., help="Путь к директории DCIM"),
        dry_run: bool = typer.Option(False, "--dry-run", help="Только логировать действия, ничего не менять"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Подробный вывод"),
        log_file: Path = typer.Option(None, "--log-file", help="Путь к лог-файлу"),
):
    """
    Удаляет файлы .NEF и конвертирует .HEIC → .JPG в указанной директории.
    """
    configure_logging(verbose, log_file)
    stats = process_dcim(dcim_path, dry_run=dry_run)

    if stats:
        logging.info("📊 Статистика:")
        logging.info(f"  Всего ДО     : {stats['total_before']}")
        logging.info(f"  Удалено .NEF : {stats['nef_deleted']}")
        logging.info(f"  HEIC → JPG   : {stats['heic_converted']}")
        logging.info(f"  Всего ПОСЛЕ  : {stats['total_after']}")
    else:
        logging.warning("Ничего не было обработано.")


@app.command("rename")
def rename_images(
        dcim_path: Path = typer.Argument(..., help="Путь к директории DCIM"),
        output_dir: Path = typer.Argument(..., help="Папка, куда сохранить итоговые изображения"),
        dry_run: bool = typer.Option(False, "--dry-run", help="Только логировать действия, не копировать файлы"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Подробный вывод"),
        log_file: Path = typer.Option(None, "--log-file", help="Путь к лог-файлу"),
):
    """
    Обходит подпапки DCIM, сортирует изображения и копирует их в новую папку с последовательной нумерацией.
    """

    configure_logging(verbose, log_file)
    rename_and_collect_images(dcim_path, output_dir, dry_run=dry_run)


if __name__ == "__main__":
    app()

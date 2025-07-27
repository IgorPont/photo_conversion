"""
CLI-интерфейс для обработки изображений в директории DCIM.

Выполняет:
- удаление файлов с расширением `.NEF`
- конвертацию файлов `.HEIC` в `.JPG` с удалением исходников
- логирование действий (с возможностью логгирования в файл)
- поддержку режима dry-run
- подробный вывод по ключу `--verbose`

Запуск:
    poetry run python -m photo_converter.cli process objects_to_convert/DCIM
"""

import logging
from pathlib import Path
import typer
from photo_converter.del_nef_and_covert_heic import process_dcim

# Создаём CLI-приложение
app = typer.Typer(help="Утилита для удаления .NEF и конвертации .HEIC → .JPG")


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


@app.command()
def process(
        dcim_path: Path = typer.Argument(..., help="Путь к директории DCIM"),
        dry_run: bool = typer.Option(False, "--dry-run", help="Только логировать действия, "
                                                              "ничего не менять"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Подробный вывод"),
        log_file: Path = typer.Option(None, "--log-file", help="Путь к лог-файлу"),
):
    """
    Обрабатывает изображения в указанной директории:
        - удаляет файлы .NEF
        - преобразует .HEIC в .JPG
        - удаляет исходные .HEIC после конвертации

    Поддерживает dry-run режим, подробный вывод и логгирование в файл.
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


if __name__ == "__main__":
    app()

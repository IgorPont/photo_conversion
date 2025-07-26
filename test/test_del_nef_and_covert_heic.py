import pytest
from PIL import Image
from photo_converter.del_nef_and_covert_heic import process_dcim


def test_nef_deleted(tmp_path):
    """
    Проверяет, что .NEF-файлы удаляются после обработки.
    """
    dcim = tmp_path / "DCIM" / "100TEST"
    dcim.mkdir(parents=True)

    nef_file = dcim / "test_image.NEF"
    nef_file.write_text("stub")  # создаём заглушку для теста

    process_dcim(tmp_path / "DCIM")

    assert not nef_file.exists(), "NEF-файл должен быть удалён"


@pytest.mark.skipif(
    not hasattr(Image, "HEIC"),
    reason="HEIC сохранение не поддерживается на этой системе",
)
def test_heic_converted_and_deleted(tmp_path):
    """
    Проверяет, что .HEIC-файлы конвертируются в .JPG и удаляются после обработки.
    """
    dcim = tmp_path / "DCIM" / "101TEST"
    dcim.mkdir(parents=True)

    heic_file = dcim / "sample.HEIC"

    # создаём пустую HEIC-картинку (если поддерживается)
    img = Image.new("RGB", (10, 10), color="red")
    try:
        img.save(heic_file, format="HEIC")
    except Exception as e:
        pytest.skip(f"HEIC сохранение не поддерживается: {e}")

    process_dcim(tmp_path / "DCIM")

    jpg_file = dcim / "sample.JPG"
    assert jpg_file.exists(), "JPG-файл должен быть создан"
    assert not heic_file.exists(), "HEIC-файл должен быть удалён"

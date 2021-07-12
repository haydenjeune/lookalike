from PIL import Image

from lib.image.convert import ImageResizer


def test_convert_resizes_image():
    with open("tests/assets/my-profile.jpeg", "rb") as f:
        img = Image.open(f)
        img.load()
    sut = ImageResizer(max_size=512)

    new_img = sut.convert(img)

    assert max(new_img.size) == 512


def test_convert_ignores_image_when_already_small_enough():
    with open("tests/assets/my-profile.jpeg", "rb") as f:
        img = Image.open(f)
        img.load()
    img = img.resize((256, 256))
    sut = ImageResizer(max_size=512)

    new_img = sut.convert(img)

    assert img.size == new_img.size
    assert img == new_img

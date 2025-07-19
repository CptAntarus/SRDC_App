from PIL import Image, ExifTags
import os

def fix_image_rotation(path, output_path=None):
    img = Image.open(path)

    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = img._getexif()

        if exif is not None:
            orientation_value = exif.get(orientation, None)

            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except Exception as e:
        print(f"Failed to adjust EXIF for {path}: {e}")

    if output_path:
        img.save(output_path)
    else:
        img.save(path)

# List of images to fix
images = [
    ""
]

for img_path in images:
    fix_image_rotation(img_path)
    print(f"Fixed: {img_path}")

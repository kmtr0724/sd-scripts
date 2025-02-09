from PIL import Image
import os
import sys
import piexif

quality=95

def convert_png_to_webp(directory):
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    output_dir = os.path.join(directory, "converted")
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(".png"):
            png_path = os.path.join(directory, filename)
            webp_path = os.path.join(output_dir, filename.rsplit(".", 1)[0] + ".webp")
            
            try:
                with Image.open(png_path) as img:
                    param_data = img.info.get("parameters").encode("utf-8")
                    if param_data:
                        exif_data = img.info.get("exif")
                        exif_dict = piexif.load(exif_data) if exif_data else {"Exif": {}}
                        exif_dict["Exif"][piexif.ExifIFD.UserComment] = param_data
                        exif_bytes = piexif.dump(exif_dict)
                        img.save(webp_path, "WEBP", exif=exif_bytes, quality=quality)
                    else:
                        img.save(webp_path, "WEBP", quality=quality)
                    print(f"Converted: {png_path} -> {webp_path}")
            except Exception as e:
                print(f"Failed to convert {png_path}: {e}")
    
    print("Conversion completed!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert.py <directory>")
    else:
        convert_png_to_webp(sys.argv[1])
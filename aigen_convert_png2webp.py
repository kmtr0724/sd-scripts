from PIL import Image
import os
import sys
import piexif

def convert_png_to_webp(directory, quality=95):
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    base_output_dir = os.path.join(directory, "converted")
    total_converted = 0
    
    for root, _, files in os.walk(directory):
        relative_path = os.path.relpath(root, directory)
        output_dir = os.path.join(base_output_dir, relative_path)
        os.makedirs(output_dir, exist_ok=True)
        
        for filename in files:
            if filename.lower().endswith(".png"):
                png_path = os.path.join(root, filename)
                webp_path = os.path.join(output_dir, filename.rsplit(".", 1)[0] + ".webp")
                
                try:
                    with Image.open(png_path) as img:
                        exif_data = img.info.get("exif")
                        parameter_text = img.info.get("parameters").encode("utf-8")
                        
                        exif_dict = piexif.load(exif_data) if exif_data else {"Exif": {}}
                        exif_dict["Exif"][piexif.ExifIFD.UserComment] = parameter_text
                        exif_bytes = piexif.dump(exif_dict)
                        
                        img.save(webp_path, "WEBP", exif=exif_bytes, quality=quality)
                        # Preserve timestamps
                        stat_info = os.stat(png_path)
                        os.utime(webp_path, (stat_info.st_atime, stat_info.st_mtime))
                        total_converted += 1
                        print(f"Converted: {png_path} -> {webp_path} with quality {quality}")
                except Exception as e:
                    print(f"Failed to convert {png_path}: {e}")
    
    print(f"Conversion completed! Total files converted: {total_converted}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python convert.py <directory> [quality]")
    else:
        quality = int(sys.argv[2]) if len(sys.argv) == 3 else 95
        convert_png_to_webp(sys.argv[1], quality)
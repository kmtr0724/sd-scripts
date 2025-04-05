import requests
import base64
import glob
import os

url = "http://127.0.0.1:7860"

# Find files
files = glob.glob('input/*.webp')
os.makedirs("output", exist_ok=True)

for file in files:
    # Get PNG Info
    print(file)
    with open(file, "rb") as f:
        img = base64.b64encode(f.read()).decode('utf-8')

    response = requests.post(url=f'{url}/sdapi/v1/png-info', json={"image": img})
    params = response.json()["parameters"]
    # Generate image
    if(float(params["CFG scale"]) >= 6):
        hrcfg = float(params["CFG scale"])-1  
    else:
        hrcfg = float(params["CFG scale"])  
    #print(params)
    #if(float(params["Size-1"])*float(params["Size-2"]) < 1382400): #<1280*1080
    if(float(params["Size-2"]) < 1080): 
        if(float(params["Size-1"]) <= 1280):
            hrscale = 2
            denoising_strength=0.35
        else:
            hrscale = 1.8
            denoising_strength=0.33        
    else:
        hrscale = 1.75
        denoising_strength=0.33
 
    payload = {
        "prompt": params["Prompt"],
        "negative_prompt": params["Negative prompt"],
        "styles": params.get("Styles array", []),
        "sampler_name": params["Sampler"],
        "scheduler": params["Schedule type"],
        "seed": params["Seed"],
        "steps": params["Steps"],
        "cfg_scale": params["CFG scale"],
        "hr_cfg": hrcfg,
        "clip skip": params["Clip skip"],
        #"width": x,
        #"height": y,
        "width": params["Size-1"],
        "height": params["Size-2"],
        "enable_hr": True,
        "hr_scale": hrscale,            # Upscale by
        "batch_size": 1,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",    # Upscaler
        "hr_second_pass_steps": 12,  # Hires steps
        "denoising_strength": denoising_strength,  # Denoising strength
        "tiling" : "false",
        "alwayson_scripts": {
        }
    }
    #print(payload)

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    # Save image
    with open(os.path.join("output", os.path.basename(file)), 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))
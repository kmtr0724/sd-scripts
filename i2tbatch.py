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
    x=float(params["Size-1"])/1.5
    y=float(params["Size-2"])/1.5
    #print(params)
    payload = {
        "prompt": params["Prompt"],
        "negative_prompt": params["Negative prompt"],
        "styles": params.get("Styles array", []),
        "seed": params["Seed"],
        "steps": params["Steps"],
        "cfg_scale": params["CFG scale"],
        "hr_cfg": params["CFG scale"],
        "clip skip": params["Clip skip"],
        "sampler_name": params["Sampler"],
        "width": x,
        "height": y,
        #"width": params["Size-1"],
        #"height": params["Size-2"],
        "Lora hashes": params["Lora hashes"],
        "enable_hr": True,
        "hr_scale": 1.5,            # Upscale by
        "batch_size": 1,
        "hr_upscaler": "R-ESRGAN 4x+ Anime6B",    # Upscaler
        "hr_second_pass_steps": 9,  # Hires steps
        "denoising_strength": 0.4,  # Denoising strength
        "tiling" : "false",
        "alwayson_scripts": {
            "ADetailer": {
                "args": [
                    "true","false",
                    {
                        "ad_negative_prompt": "lip", #negative 
                        "ad_mask_k_largest": 1,
                        "ad_cfg_scale": 7,
                        "ad_checkpoint": "Use same checkpoint",
                        "ad_clip_skip": 1,
                        "ad_confidence": 0.7,
                        "ad_controlnet_guidance_end": 1,
                        "ad_controlnet_guidance_start": 0,
                        "ad_controlnet_model": "None",
                        "ad_controlnet_module": "None",
                        "ad_controlnet_weight": 1,
                        "ad_denoising_strength": 0.4,
                        "ad_dilate_erode": 4,
                        "ad_inpaint_height": 512,
                        "ad_inpaint_only_masked": "true",
                        "ad_inpaint_only_masked_padding": 32,
                        "ad_inpaint_width": 512,
                        "ad_mask_blur": 4,
                        "ad_mask_max_ratio": 1,
                        "ad_mask_merge_invert": "None",
                        "ad_mask_min_ratio": 0,
                        "ad_model": "face_yolov8n.pt",
                        "ad_model_classes": "",
                        "ad_noise_multiplier": 1,
                        "ad_prompt": "",
                        "ad_restore_face": "false",
                        "ad_sampler": "DPM++ 2M Karras",
                        "ad_scheduler": "Use same scheduler",
                        "ad_steps": 28,
                        "ad_tab_enable": "true",
                        "ad_use_cfg_scale": "false",
                        "ad_use_checkpoint": "false",
                        "ad_use_clip_skip": "false",
                        "ad_use_inpaint_width_height": "false",
                        "ad_use_noise_multiplier": "false",
                        "ad_use_sampler": "false",
                        "ad_use_steps": "false",
                        "ad_use_vae": "false",
                        "ad_vae": "Use same VAE",
                        "ad_x_offset": 0,
                        "ad_y_offset": 0,
                    }
                ]
            },
            "LoRA Block Weight (reForge)": {
        		"args": ["MYSETS:1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\nYOURSETS:0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1", True, 1 ,"","","","","","","","","","","","","",""]
	        },
        }
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    # Save image
    with open(os.path.join("output", os.path.basename(file)), 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))
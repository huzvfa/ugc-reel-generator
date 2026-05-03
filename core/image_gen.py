import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image

class UGCImageGen:
    def __init__(self):
        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", 
            torch_dtype=torch.float16, 
            variant="fp16"
        ).to("cuda")

    def generate(self, prompt, path="input/creator_face.png"):
        # Specialized UGC prompt engineering
        ugc_prompt = f"{prompt}, centered portrait, shot on mobile phone, realistic, social media style"
        image = self.pipe(prompt=ugc_prompt, num_inference_steps=2, guidance_scale=0.0, height=1024, width=576).images[0]
        image.save(path)
        return path

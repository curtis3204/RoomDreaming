# This file is adapted from gradio_*.py in https://github.com/lllyasviel/ControlNet/tree/f4748e3630d8141d7765e2bd9b1e348f47847707
# The original license file is LICENSE.ControlNet in this repo.

from __future__ import annotations

import gc
import pathlib
import sys

import cv2
import numpy as np
import PIL.Image
import torch
from diffusers import (ControlNetModel, DiffusionPipeline,
                       StableDiffusionControlNetPipeline,
                       UniPCMultistepScheduler, StableDiffusionPipeline)




repo_dir = pathlib.Path(__file__).parent
submodule_dir = repo_dir / 'ControlNet'
sys.path.append(submodule_dir.as_posix())

CONTROLNET_MODEL_IDS = {
    'canny': 'lllyasviel/sd-controlnet-canny',
    'seg': 'lllyasviel/sd-controlnet-seg',
    'depth': 'lllyasviel/sd-controlnet-depth',
}



def HWC3(x):
    assert x.dtype == np.uint8
    if x.ndim == 2:
        x = x[:, :, None]
    assert x.ndim == 3
    H, W, C = x.shape
    assert C == 1 or C == 3 or C == 4
    if C == 3:
        return x
    if C == 1:
        return np.concatenate([x, x, x], axis=2)
    if C == 4:
        color = x[:, :, 0:3].astype(np.float32)
        alpha = x[:, :, 3:4].astype(np.float32) / 255.0
        y = color * alpha + 255.0 * (1.0 - alpha)
        y = y.clip(0, 255).astype(np.uint8)
        return y


def resize_image(input_image, resolution):
    H, W, C = input_image.shape
    H = float(H)
    W = float(W)
    k = float(resolution) / min(H, W)
    H *= k
    W *= k
    H = int(np.round(H / 64.0)) * 64
    W = int(np.round(W / 64.0)) * 64
    img = cv2.resize(input_image, (W, H), interpolation=cv2.INTER_LANCZOS4 if k > 1 else cv2.INTER_AREA)
    return img




def download_all_controlnet_weights() -> None:
    for model_id in CONTROLNET_MODEL_IDS.values():
        ControlNetModel.from_pretrained(model_id)


class Model:
    def __init__(self,
                 base_model_id: str = 'runwayml/stable-diffusion-v1-5',
                 task_name: str = 'canny'):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.base_model_id = ''
        self.task_name = ''
        self.pipe = self.load_pipe(base_model_id, task_name)

    def load_pipe(self, base_model_id: str, task_name) -> DiffusionPipeline:
        if self.device.type == 'cpu':
            print("[Stop loading pipeline] as CPU is not supported")
            return None
        
        model_id = CONTROLNET_MODEL_IDS[task_name]

        controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
        
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16)

        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
        
        pipe.enable_xformers_memory_efficient_attention()
        # pipe.enable_model_cpu_offload()

        pipe.to(self.device)
        torch.cuda.empty_cache()
        gc.collect()
        self.base_model_id = base_model_id
        self.task_name = task_name
        print("[Load Diffuser Pipeline Successfully]")
        return pipe


    # def set_base_model(self, base_model_id: str) -> str:
    #     if not base_model_id or base_model_id == self.base_model_id:
    #         return self.base_model_id
    #     del self.pipe
    #     torch.cuda.empty_cache()
    #     gc.collect()
    #     try:
    #         self.pipe = self.load_pipe(base_model_id, self.task_name)
    #     except Exception:
    #         self.pipe = self.load_pipe(self.base_model_id, self.task_name)
    #     return self.base_model_id

    def load_controlnet_weight(self, task_name: str) -> None:
        if task_name == self.task_name:
            return
        # if 'controlnet' in self.pipe.__dict__:
        #     del self.pipe.controlnet
        torch.cuda.empty_cache()
        gc.collect()
        model_id = CONTROLNET_MODEL_IDS[task_name]
        controlnet = ControlNetModel.from_pretrained(model_id,
                                                     torch_dtype=torch.float16)
        controlnet.to(self.device)
        torch.cuda.empty_cache()
        gc.collect()
        # self.pipe.controlnet = controlnet
        self.task_name = task_name


    def get_prompt(self, prompt: str, additional_prompt: str) -> str:
        if not prompt:
            prompt = additional_prompt
        else:
            prompt = f'{prompt}, {additional_prompt}'
        return prompt


    # @torch.autocast('cuda')
    # def run_pipe(
    #     self,
    #     prompt: str,
    #     negative_prompt: str,
    #     control_image: PIL.Image.Image,
    #     num_images: int,
    #     num_steps: int,
    #     guidance_scale: float,
    #     seed: int,
    # ) -> list[PIL.Image.Image]:
    #     if seed == -1:
    #         seed = np.random.randint(0, np.iinfo(np.int64).max)
    #     generator = torch.Generator().manual_seed(seed)
    #     return self.pipe(prompt=prompt,
    #                      negative_prompt=negative_prompt,
    #                      guidance_scale=guidance_scale,
    #                      num_images_per_prompt=num_images,
    #                      num_inference_steps=num_steps,
    #                      generator=generator,
    #                      image=control_image)





    ################## Preprocess the input image for the canny edge task ##################
    @staticmethod
    def preprocess_canny(
        input_image: np.ndarray,
        image_resolution: int,
        low_threshold: int,
        high_threshold: int,
    ) -> tuple[PIL.Image.Image]:
        
        # resize the input image
        image = resize_image(HWC3(input_image), image_resolution)
        control_image = cv2.Canny(image, low_threshold, high_threshold)
        control_image = HWC3(control_image)
        print("finish preprocess canny")
        return PIL.Image.fromarray(control_image)


    ################## process canny ##################
    @torch.inference_mode()
    def process_canny(self, input_image: np.ndarray, prompt: str, 
                      additional_prompt: str,negative_prompt: str, 
                      num_images: int, image_resolution: int, 
                      num_steps: int, guidance_scale: float, 
                      seed: int, low_threshold: int, 
                      high_threshold: int, ) -> list[PIL.Image.Image]:

        control_image = self.preprocess_canny(input_image=input_image,
                                              image_resolution=image_resolution,
                                              low_threshold=low_threshold,
                                              high_threshold=high_threshold,)
        
        

        p = "(((living room))), red chairs, rich wood furniture, traditional patterns, a muted color palette with hints of natural hues"


        self.load_controlnet_weight('canny')

        if seed == -1:
            seed = np.random.randint(0, np.iinfo(np.int64).max)
        generator = torch.Generator().manual_seed(seed)

        results = self.pipe(prompt=prompt,
                            negative_prompt=negative_prompt,
                            guidance_scale=guidance_scale,
                            num_images_per_prompt=num_images,
                            num_inference_steps=num_steps,
                            generator=generator,
                            image=control_image, ).images[0]

        
        
        
        return [control_image] + [results]



import mappings
import os
import sys
import yaml
sd_scripts_install = 'D:\StableDiffusionProjects\sd-scripts' #TODO set this up as a command line argument or some other way so it isn't just a global
sys.path.append(sd_scripts_install)

import train_network as tn
import sdxl_train_network as tn_sdxl
import library.train_util as train_util

def generate_flags(dict: dict) -> list[str]:
    out = []
    for k, v in dict.items():
        if isinstance(v, bool):
            if v:
                out.append(f"--{k}")
            continue
        if isinstance(v, str):
            if v == "": continue
        if isinstance(v, list):
            out.append(f"--{k}={str(v)}")
            continue
        out.append(f"--{k}={v}")
    return out

def train(arg_dict: dict):
    old_work_dir = os.getcwd()
    os.chdir(sd_scripts_install)
    
    sdxl = arg_dict['sdxl']

    if sdxl: 
        lib = tn_sdxl
        trainer = tn_sdxl.SdxlNetworkTrainer()
    else: 
        lib = tn
        trainer = tn.NetworkTrainer()
    mappings.preprocess_config(arg_dict)
    parser = lib.setup_parser()
    flags = generate_flags(arg_dict)
    args = parser.parse_args(flags)
    train_util.verify_command_line_training_args(args)
    print('training')
    trainer.train(args)
    os.chdir(old_work_dir)

def read_yaml(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)
def stack_yamls(paths: list[str]) -> dict:
    out = {}
    for path in paths:
        out.update(read_yaml(path))
    return out
    
def main():
    arg_dict = read_yaml('config.yaml')
    train(arg_dict)

if __name__ == "__main__":
    main()
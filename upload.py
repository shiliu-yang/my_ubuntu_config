#!/usr/bin/env python
#coding=utf-8

import os
import sys
import logging
import shutil

user_home=os.path.expanduser("~")

cur_path=os.path.dirname(os.path.realpath(__file__))
cur_path=os.path.normpath(cur_path)

def log_config(level=logging.INFO):
    FORMAT = '[%(levelname)-8s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
    logging.basicConfig(
        level=level,
        format=FORMAT,
        datefmt='%H:%M:%S'
    )

def copy_file(src, dst):
    src = os.path.normpath(src)
    if not os.path.exists(src):
        logging.error(f"Not find {src}")
        return False

    if os.path.exists(dst):
        if os.path.isfile(dst):
            os.remove(dst)
            logging.debug(f"remove file: {dst}")
        else:
            shutil.rmtree(dst)
            logging.debug(f"remove dir: {dst}")

    if os.path.isfile(src):
        shutil.copy2(src, dst)
    else:
        shutil.copytree(src, dst)

    return True

def copy_omz_config():
    zshrc_path = os.path.join(user_home, ".zshrc")
    omz_custom_path = os.path.join(user_home, ".oh-my-zsh", "custom")
    if not os.path.exists(zshrc_path):
        logging.error(f"Not find {zshrc_path}")
        return False
    
    if not os.path.exists(omz_custom_path):
        logging.error(f"Not find {omz_custom_path}")
        return False
    
    if not os.path.exists(os.path.join(cur_path, "oh-my-zsh")):
        os.makedirs(os.path.join(cur_path, "oh-my-zsh"))

    # copy .zshrc
    if copy_file(zshrc_path, os.path.join(cur_path, "oh-my-zsh", ".zshrc")):
        logging.info("Copy .zshrc success")
    else:
        logging.error("Copy .zshrc fail")

    # copy .oh-my-zsh/custom
    if copy_file(omz_custom_path, os.path.join(cur_path, "oh-my-zsh", ".oh-my-zsh", "custom")):
        logging.info("Copy .oh-my-zsh/custom success")
    else:
        logging.error("Copy .oh-my-zsh/custom fail")

    return True

def copy_lazyvim_config():
    nvim_config = os.path.join(user_home, ".config", "nvim")
    nvim_config_bak = os.path.join(cur_path, "LazyVim", ".config", "nvim")

    if not os.path.exists(os.path.join(cur_path, "LazyVim")):
        os.makedirs(os.path.join(cur_path, "LazyVim"))

    if copy_file(nvim_config, os.path.join(cur_path, "LazyVim", ".config", "nvim")):
        logging.info("Copy nvim config success")
    else:
        logging.error("Copy nvim config fail")

if __name__ == "__main__":
    log_config(logging.DEBUG)

    # copy lazyvim config
    copy_lazyvim_config()

    # copy oh-my-zsh config
    copy_omz_config()

    sys.exit(0)


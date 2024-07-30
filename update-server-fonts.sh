#!/bin/bash

latest_version = $(jq -r '.version' node_modules/@tabler/icons/package.json)

# construct folder name
dataset_name = tabler-icons$latest_version

dataset_path src/server/datasets/$folder_name

mkdir dataset_path
cp node_modules/@tabler/icons/icons.json $dataset_path
cp node_modules/@tabler/icons-webfont/dist/fonts/* $dataset_path
h

#!/bin/bash
pip freeze | grep -v "pkg-resources" > requirements.txt 

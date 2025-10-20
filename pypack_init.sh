#!/bin/bash
############################################
# Author : Justin Traywcick
# Created : 2025-10-20
# Edited : 2025-10-20
# Purpose : Shell script for initializing python package directory structure. 
#           Ran from root package directory.
#############################################

# Get package directory and name as variables.

root_dir=$(echo | pwd)  # Get package directory as variable.
pack_name="${root_dir##*/}"


# Get neccessary module names as variables.

echo "Input comma separated module names if any (no spaces):"
read module_str
echo
    # Parse:
delimiter=","
OIFS="$IFS"  # Save original IFS to variable.
IFS="$delimiter" read -r -a module_arr <<< "$module_str"  # Parse module_str with ',' as delimiter.
IFS="$OIFS"  # Restore IFS to original IFS.


# Make package directories.

dirs_arr=("src/${pack_name}" "tests")  # Array containing directory names.
echo "Making package directories: ${dirs_arr[@]}..."
for directory in "${dirs_arr[@]}";
do
    mkdir -p "${root_dir}/${directory}"
done
echo -e "...done. \n"


# Make module and __init__.py files in root_dir/src/package directory.

# /src files:
echo "Making /src files: ${module_arr[@]}, __init__.py, ${pack_name}.toml..."
for module in "${module_arr[@]}";
do
    touch ${root_dir}/src/${pack_name}/${module}.py  # Make module files.
done

touch ${root_dir}/src/${pack_name}/__init__.py  # Make __init__.py file.
touch ${root_dir}/src/${pack_name}/${pack_name}.toml
echo -e "...done. \n"

# /test files:
echo "Making /test files: __init__.py, test_${pack_name}.py"
touch ${root_dir}/tests/__init__.py  # Make __init__.py file.
touch ${root_dir}/tests/test_${pack_name}.py  # Make test file.
echo -e "...done. \n"

# Make readme and license files.
touch ${root_dir}/README.md
cp /Users/justintraywick/Coding/pypackage_template/LICENSE ./

echo "Python package structure initialization complete."

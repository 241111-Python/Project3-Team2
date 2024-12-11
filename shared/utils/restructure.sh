#!/bin/bash
# Credits for part of this goes to chatgpt. In particular, for create_structure. 


# Define the desired file structure
declare -A structure=(
    ["analyses/"]=""
    ["graphs/"]=""
    ["shared/utils/"]=""
    ["shared/config/"]=""
)

# Function to create directories and files
create_structure() {
    for path in "${!structure[@]}"; do
        # Check if it's a directory
        if [[ "${path}" == */ ]]; then
            if [[ ! -d "$path" ]]; then
                echo "Creating directory: $path"
                mkdir -p "$path"
            fi
        else
            if [[ ! -f "$path" ]]; then
                echo "Creating file: $path"
                echo -e "${structure[$path]}" > "$path"
            fi
        fi
    done
}

remove_pngs() {
    echo "Removing PNG files"
    for file in *.png; do
        if [[ -f "$file" ]]; then
            echo "Deleting $file"
            rm "$file"
        fi
    done
}

move_python_files() {
    echo "Moving python files"
    for file in *.py; do
        if [[ -f "$file" ]]; then
            echo "Moving $file"
            mv "$file" "analyses/$file"
        fi
    done
}

cd ../../

create_structure
remove_pngs
move_python_files

echo "File structure enforcement complete."

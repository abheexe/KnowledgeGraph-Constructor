import subprocess

try:
    # Download the dataset tar file
    subprocess.run([
        'curl', '-L',
        'https://huggingface.co/datasets/khushwant04/Research-Papers/resolve/main/research-papers.tar?download=true',
        '-o', 'research-papers.tar'
    ], check=True)

    # Extract the tar file
    subprocess.run(['tar', '-xf', 'research-papers.tar'], check=True)
    
    print("Download and extraction complete.")
except subprocess.CalledProcessError as e:
    print(f"Error during download/extraction: {e}")

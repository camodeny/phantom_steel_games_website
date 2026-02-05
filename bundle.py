import base64
import os
import re

def bundle_assets():
    # Use the directory where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_html = os.path.join(base_dir, 'index.html')
    output_html = os.path.join(base_dir, 'index_bundled.html')

    print(f"Reading from: {input_html}")

    try:
        with open(input_html, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: index.html not found in {base_dir}")
        return

    # Assets to replace. 
    # Note: Regex patterns are used to ensure we match the specific usage context
    assets = [
        # Fonts
        {
            'filename': 'MokotoGlitchMark.ttf', 
            'mime': 'font/ttf',
            'pattern': r"url\(['\"]?MokotoGlitchMark\.ttf['\"]?\)"
        },
        {
            'filename': 'MokotoRegular.ttf', 
            'mime': 'font/ttf',
            'pattern': r"url\(['\"]?MokotoRegular\.ttf['\"]?\)"
        },
        # Images
        {
            'filename': 'logo_v2.png', 
            'mime': 'image/png',
            'pattern': r'src=["\']logo_v2\.png["\']' 
        }
    ]

    for asset in assets:
        file_path = os.path.join(base_dir, asset['filename'])
        
        if os.path.exists(file_path):
            print(f"Processing {asset['filename']}...")
            
            with open(file_path, 'rb') as f:
                encoded_bytes = base64.b64encode(f.read())
                encoded_string = encoded_bytes.decode('utf-8')
            
            data_uri = f"data:{asset['mime']};base64,{encoded_string}"
            
            # Perform substitution
            if asset['mime'].startswith('font'):
                # For fonts: url('data:...')
                replacement = f"url('{data_uri}')"
                content = re.sub(asset['pattern'], replacement, content)
            else:
                # For img tags: src="data:..."
                # We need to preserve the src= part if we matched it, or just replace the filename if we implement it that way.
                # The pattern matches the whole attribute value: src="logo_v2.png"
                # So we replace it with: src="data:..."
                replacement = f'src="{data_uri}"'
                content = re.sub(asset['pattern'], replacement, content)
                
        else:
            print(f"Warning: Asset {asset['filename']} not found. Skipping.")

    print(f"Writing bundled file to: {output_html}")
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Done!")
    if os.path.exists(output_html):
        print(f"New file size: {os.path.getsize(output_html) / 1024:.2f} KB")

if __name__ == "__main__":
    bundle_assets()

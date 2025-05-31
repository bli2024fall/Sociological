import os

# ==== Config ====
FOLDER = "Archive"          # Your html folder, relative to repo root
README = "README.md"
MARKER_START = "<!-- HTML LINKS START -->"
MARKER_END = "<!-- HTML LINKS END -->"

def get_github_pages_url():
    # Try to get from GitHub Actions env variable
    repo = os.getenv('GITHUB_REPOSITORY')
    if not repo:
        # Try to get from git config (for local use)
        try:
            import subprocess
            remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).decode().strip()
            if remote_url.startswith('git@'):
                repo = remote_url.split(':')[1].replace('.git','')
            elif remote_url.startswith('https://github.com/'):
                repo = remote_url.replace('https://github.com/','').replace('.git','')
        except Exception:
            raise Exception("Cannot detect repo name. Set GITHUB_REPOSITORY env or run in a git repo.")
    user, repo_name = repo.split('/')
    return f"https://{user}.github.io/{repo_name}/"

base_url = get_github_pages_url()

# Find all .html files in the specified folder
html_files = []
for root, _, files in os.walk(FOLDER):
    for f in files:
        if f.endswith('.html'):
            relpath = os.path.relpath(os.path.join(root, f), '.') # relative to repo root
            html_files.append(relpath.replace("\\", "/"))

# Generate markdown links
links_md = '\n'.join([f'- [{os.path.basename(f)}]({base_url}{f.replace(" ", "%20")})' for f in html_files])

# Update README.md between markers
with open(README, 'r') as f:
    content = f.read()
start = content.find(MARKER_START)
end = content.find(MARKER_END)
if start == -1 or end == -1:
    raise Exception("Markers not found in README.md.")
new_content = (
    content[:start+len(MARKER_START)] +
    "\n" + links_md + "\n" +
    content[end:]
)
with open(README, 'w') as f:
    f.write(new_content)

print(f"Inserted {len(html_files)} links into {README}.")



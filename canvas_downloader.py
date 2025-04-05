import os
import requests
import logging

# === Configuration ===
API_URL = "https://umich.instructure.com"  # Replace with your Canvas URL
API_TOKEN = "Enter your key here!"
DOWNLOAD_DIR = "canvas_files"
LOG_FILE = "canvas_download.log"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === Setup ===
headers = {"Authorization": f"Bearer {API_TOKEN}"}
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Also log to terminal
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def get_courses():
    url = f"{API_URL}/api/v1/courses"
    params = {
        'per_page': 100,
        'enrollment_state': 'all',   # instead of just 'active'
        'include[]': 'term',         # optional: includes term name
        'state[]': ['available', 'completed']  # gets active + completed
    }
    courses = []

    while url:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        courses.extend(r.json())
        url = r.links.get('next', {}).get('url')
    return courses

def get_folders(course_id):
    url = f"{API_URL}/api/v1/courses/{course_id}/folders"
    folders = []
    params = {'per_page': 100}

    while url:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        folders.extend(r.json())
        url = r.links.get('next', {}).get('url')
    return folders

def get_files_in_folder(folder_id):
    url = f"{API_URL}/api/v1/folders/{folder_id}/files"
    files = []
    params = {'per_page': 100}

    while url:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        files.extend(r.json())
        url = r.links.get('next', {}).get('url')
    return files

def sanitize(name):
    return name.replace("/", "_").replace(":", "-")

def download_file(file, save_path):
    file_name = sanitize(file['display_name'])
    file_url = file['url']
    full_path = os.path.join(save_path, file_name)

    if os.path.exists(full_path):
        print(f"Already exists: {file_name}")
        return

    print(f"⬇️  Downloading: {file_name}")
    r = requests.get(file_url, headers=headers)
    r.raise_for_status()

    with open(full_path, 'wb') as f:
        f.write(r.content)

def main():
    courses = get_courses()
    print(f"\n🎓 Found {len(courses)} courses.\n")

    print("🧾 Courses:")
    for idx, course in enumerate(courses, start=1):
        print(f"{idx}. {course.get('name')} (ID: {course['id']})")

    selection = input("\n🔢 Enter the course numbers you want to download (comma-separated): ").strip()
    if not selection:
        print("❌ No selection made. Exiting.")
        return

    try:
        selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
    except ValueError:
        print("❌ Invalid input. Please enter numbers separated by commas.")
        return

    selected_courses = [courses[i] for i in selected_indices if 0 <= i < len(courses)]

    for course in selected_courses:
        course_id = course['id']
        course_name = sanitize(course.get('name', f"Course_{course_id}"))
        course_folder = os.path.join(DOWNLOAD_DIR, course_name)
        os.makedirs(course_folder, exist_ok=True)

        print(f"\n📁 Downloading Course: {course_name}")
        folders = get_folders(course_id)

        for folder in folders:
            folder_path = folder['full_name'].replace("course files", "").strip("/")
            folder_local_path = os.path.join(course_folder, sanitize(folder_path))
            os.makedirs(folder_local_path, exist_ok=True)

            try:
                files = get_files_in_folder(folder['id'])
                for file in files:
                    download_file(file, folder_local_path)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"❌ Skipping restricted folder: {folder['full_name']}")
                else:
                    raise

if __name__ == "__main__":
    main()
import glob
import os

from pathlib import Path

txt_files = glob.glob("txt_report/*.txt")
text_titles = [Path(text).stem for text in txt_files]

for file_path in txt_files:
    with open(file_path, 'r', encoding='utf-8', errors='replace') as summary_file:

        filename = Path(file_path).stem

        summary_file.readline() # Skip the header

        # Everything up to Highlights section is written to one file

        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #<-- absolute dir the script is in
        rel_path = f'txt_report/sustainability_goals/{filename}.txt'
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'w+', encoding='utf-8') as write_file:

            current_line = summary_file.readline()

            while 'Highlights' not in current_line:
                write_file.write(current_line)
                current_line = summary_file.readline()
            
        # The highlights go to the other file
        rel_path = f'txt_report/latest_report_highlights/{filename}.txt'
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'w+', encoding='utf-8') as write_file:

            while current_line:
                write_file.write(current_line)
                current_line = summary_file.readline()
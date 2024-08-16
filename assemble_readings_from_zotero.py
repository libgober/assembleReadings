#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:16:41 2024

@author: blibgober
"""


from dotenv import load_dotenv
import os
import argparse
import re
from pyzotero import zotero
import json

import shutil
load_dotenv() 

# Configuration
ZOTERO_LIBRARY_ID = os.getenv("ZOTERO_LIBRARY_ID")
ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY")
ZOTERO_LIBRARY_TYPE = 'user'  # or 'group' if it's a group library
#export library, better Bibtex json
ZOTERO_JSON_PATH = os.getenv("ZOTERO_JSON_PATH")
# Initialize Zotero client
zot = zotero.Zotero(ZOTERO_LIBRARY_ID, ZOTERO_LIBRARY_TYPE, ZOTERO_API_KEY)

def extract_sessions(markdown_text):
    """Extract session numbers and their citations from the Markdown syllabus."""
    session_dict = {}
    missing_citations = []

    # Split the syllabus into blocks by session
    session_blocks = re.split(r'(?=## Session \d+ \([^)]+\):)', markdown_text)

    for block in session_blocks:
        # Use regex to capture just the session number (e.g., "Session 1")
        session_header_match = re.match(r'## (Session \d+)', block)
        if session_header_match:
            session_number = session_header_match.group(1).strip()
            citations = []
            lines = block.split('\n')
            for line in lines:
                if line.strip().startswith('-'):
                    citation_match = re.search(r'@([^\s\)]+)', line)
                    if citation_match:
                        citation_key = citation_match.group(1)
                        citations.append(citation_key)
                    else:
                        missing_citations.append(line.strip())
            session_dict[session_number] = citations

    return session_dict, missing_citations

def load_zotero_json(json_path):
    """Load Zotero data from the exported JSON file."""
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def map_betterbibtex_to_zotero_item(citation_key, zotero_data):
    """Map a Better BibTeX citation key to the Zotero item."""
    for item in zotero_data['items']:
        if 'citationKey' in item and item['citationKey'] == citation_key:
            return item
    return None


def copy_or_download_pdf(citation_key, zotero_data, output_dir):
    """Try to copy the PDF file from Zotero storage; if not found, download it."""
    item = map_betterbibtex_to_zotero_item(citation_key, zotero_data)
    
    if item and 'attachments' in item:
        for attachment in item['attachments']:
            if 'path' in attachment:
                pdf_path = attachment['path']
                destination_path = os.path.join(output_dir, f"{citation_key}.pdf")
                os.makedirs(output_dir, exist_ok=True)
                
                # Try copying the file
                try:
                    shutil.copy(pdf_path, destination_path)
                    return destination_path
                except FileNotFoundError:
                    print(f"File not found at {pdf_path}, attempting to download...")

                # If the file isn't found locally, try downloading it
                if 'uri' in attachment:
                    file_key = os.path.split(attachment['uri'])[1]
                    pdf_content = zot.file(file_key)
                    with open(destination_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_url.content)
                    return destination_path
    return None



def main():
    """Main function to orchestrate the copying or downloading of PDFs based on a Markdown syllabus."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch PDFs from Zotero based on a Markdown syllabus.")
    parser.add_argument('syllabus_file', help="Path to the Markdown syllabus file")
    parser.add_argument('output_dir', help="Directory to save the fetched PDFs")
    parser.add_argument('--missing-keys-output', default='missing_citation_keys.txt', help="File to save missing citation keys")
    parser.add_argument('--failed-downloads-output', default='failed_downloads.txt', help="File to save failed PDF downloads")
    args = parser.parse_args()

    # Load the Zotero JSON library
    zotero_data = load_zotero_json(ZOTERO_JSON_PATH)

    # Read the syllabus markdown
    with open(args.syllabus_file, 'r') as file:
        markdown_text = file.read()

    # Extract sessions and missing citation keys
    sessions, missing_citations = extract_sessions(markdown_text)

    failed_downloads = []

    # Copy or download PDFs organized by session
    for session_name, citations in sessions.items():
        session_output_dir = os.path.join(args.output_dir, session_name)
        for citation in citations:
            pdf_path = copy_or_download_pdf(citation, zotero_data, session_output_dir)
            if pdf_path:
                print(f"Processed PDF for {citation}: {pdf_path}")
            else:
                print(f"Could not find or download PDF for {citation}")
                failed_downloads.append(citation)

    # Save missing citation keys to file
    if missing_citations:
        print("\nThe following items did not have proper citation keys:")
        for missing in missing_citations:
            print(f"- {missing}")

        with open(args.missing_keys_output, 'w') as missing_file:
            for missing in missing_citations:
                missing_file.write(f"{missing}\n")
        print(f"\nMissing citation keys have been saved to {args.missing_keys_output}")

    # Save failed downloads to file
    if failed_downloads:
        print("\nThe following PDFs could not be downloaded:")
        for failed in failed_downloads:
            print(f"- {failed}")

        with open(args.failed_downloads_output, 'w') as failed_file:
            for failed in failed_downloads:
                failed_file.write(f"{failed}\n")
        print(f"\nFailed PDF downloads have been saved to {args.failed_downloads_output}")


if __name__ == "__main__":
    main()


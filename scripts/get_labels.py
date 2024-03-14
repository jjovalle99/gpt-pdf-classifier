import argparse
import asyncio
from base64 import b64encode
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai.chat_models import ChatOpenAI

from src.output_schema import Classification

# Load environment variables
load_dotenv()

# Configuration
TEMPERATURE = 0.3
OUTPUT_PARSER = JsonOutputParser(pydantic_object=Classification)
SYSTEM_MESSAGE = f"""Please classify the following image into the most appropriate category. If the image does not clearly fit any category or if you're unsure, select 'UNKNOWN'. Here are the categories to choose from:

- COVER_PAGE: The image serves as the front page or cover of a document or book.
- BLANK_PAGE: The image shows a blank page without text or significant markings.
- TEXT_PAGE: The image is predominantly text-based, similar to a book or document page.
- IMAGE_PAGE: The image is primarily a photograph or illustration without significant text.
- DIAGRAM_PAGE: The image contains diagrams, charts, or graphs, with minimal text.
- TEXT_PLUS_IMAGE_PAGE: The image includes both text and significant photographic or illustrative content.
- TEXT_PLUS_DIAGRAM_PAGE: The image combines text with diagrams, charts, or graphs.
- TABLE_PAGE: The image features tables or spreadsheets.
- TEXT_PLUS_TABLE_PAGE: The image includes both text and table(s) or spreadsheet(s).

Select the single most fitting category based on the image's content.
{OUTPUT_PARSER.get_format_instructions()}"""

# Models Configuration
gpt = ChatOpenAI(model="gpt-4-vision-preview", temperature=TEMPERATURE)
chain = gpt | OUTPUT_PARSER


def encode_image_to_base64(img_path):
    """Encode the image located at img_path to a base64 string."""
    try:
        with img_path.open("rb") as img_file:
            return b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error reading the image file: {e}")
        return None


def prepare_messages(img_base64, system_message=SYSTEM_MESSAGE):
    """Prepare messages for inference"""
    human_message = HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img_base64}"},
            }
        ],
    )
    messages = [("system", system_message), human_message]
    return messages


def gen_batches(iterable, n=99):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("images_path", help="Path to the Images dir.")
    parser.add_argument("batch_size", type=int, help="Number of images to process at a time.")
    parser.add_argument(
        "--return_exceptions",
        action="store_true",
        help="To allow the API call to return exceptions.",
    )
    parser.add_argument("--regex", help="Regex to filter the images.", default="*.*")
    parser.add_argument("--sleep", type=float, help="Time to sleep between batches.", default=0)
    parser.add_argument("--output-path", help="Path to save the final df.", default="labels.csv")
    args = parser.parse_args()

    DATA_FOLDER = Path(args.images_path)
    file_names = list(DATA_FOLDER.glob(args.regex))
    file_names = sorted(file_names, key=lambda x: int(x.stem.split("_")[0]))
    encoded_images = [encode_image_to_base64(img_path=file) for file in file_names]
    prepared_messages = [prepare_messages(img_base64=img) for img in encoded_images]
    total = len(prepared_messages) // args.batch_size + 1
    print(len(file_names))
    results = []
    for idx, batch in enumerate(gen_batches(prepared_messages, n=args.batch_size), start=1):
        print(f"Batch {idx}/{total} processing...")
        results.extend(await chain.abatch(batch, return_exceptions=args.return_exceptions))
        if args.sleep > 0:
            await asyncio.sleep(args.sleep)
            print(f"Batch {idx}/{total} processed! Sleeping for {args.sleep} seconds...")
        print("-" * 50)

    df = pd.DataFrame(
        zip(file_names, [c["label"] if isinstance(c, dict) else c for c in results]),
        columns=["local_image_path", "label"],
    )

    df.to_csv(args.output_path, index=False)


if __name__ == "__main__":
    asyncio.run(main())
    # Usage: python scripts/get_labels.py data/ 20 --regex "*_2022-denver-green-code.png" --sleep 60 --output-path labels_file1.csv
    # Usage: python scripts/get_labels.py data/ 20 --regex "*_20201119Complete_Denver_Zoning_Code_updated11122020.png" --sleep 60 --output-path labels_file2.csv

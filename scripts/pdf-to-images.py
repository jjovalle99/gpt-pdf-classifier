import argparse
import os

import fitz  # PyMuPDF


def pdf_to_images(pdf_path, output_dir=".", image_format="png", dpi=300):
    """
    Convert each page of a PDF document to high-quality PNG images, saving them to a specified directory.

    Parameters:
        pdf_path (str): Path to the PDF file.
        output_dir (str, optional): Directory to save the output images. Defaults to the current directory.
        image_format (str, optional): The image format for output. Defaults to 'png'.
        dpi (int, optional): Dots per inch for the output image. Higher values increase quality. Defaults to 300.
    """
    # Ensure output directory exists, create if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Failed to open the PDF file: {e}")
        return

    # Extract the base name of the PDF file to use in the output file names
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        output_filename = os.path.join(output_dir, f"{page_num + 1}_{base_name}.{image_format}")
        pix.save(output_filename)
        print(f"Saved {output_filename}")

    doc.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument("--output-dir", help="Directory to save the output images.", default=".")
    parser.add_argument("--image-format", help="The image format for output.", default="png")
    parser.add_argument("--dpi", help="Dots per inch for the output image.", default=300, type=int)
    args = parser.parse_args()
    pdf_to_images(args.pdf_path, args.output_dir, args.image_format, args.dpi)
    # Usage: python scripts/pdf-to-images.py raw_data/20201119Complete_Denver_Zoning_Code_updated11122020.pdf --output-dir data/ --image-format png --dpi 400
    # Usage: python scripts/pdf-to-images.py raw_data/2022-denver-green-code.pdf --output-dir data/ --image-format png --dpi 400

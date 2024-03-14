
# Repository Structure

| Component             | Description                                                                                                                    |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `raw_data/`           | Folder containing source PDFs.                                                                                                 |
| `scripts/`            | Folder with two scripts: one for converting PDF to PNG images (`pdf-to-images.py`), and another for classifying the images into specified labels (`get_labels.py`). |
| `notebooks/`          | Folder containing notebooks: one for label classification in an interactive notebook format, and another for creating the final dataset and a Hugging Face dataset variant. |
| `src/`                | Auxiliary classes and utility functions.                                                                                       |
| `.env.example`        | Template for environment variables (rename to `.env` and populate with actual values for use).                                 |
| `.python-version`     | File specifying the Python version used in this project.                                                                       |
| `poetry.lock`, `pyproject.toml` | Poetry configuration and dependency files.                                                                                    |

## Initial Setup

A `data/` folder is required for processing:

```bash
mkdir data/
```

## Scripts

### pdf-to-images.py
Converts each page of a PDF into a JPG or PNG image using PyMuPDF.
#### Usage
```python
python scripts/pdf-to-images.py <pdf_path> \
    --output-dir <output_directory> \
    --image-format <image_format> \
    --dpi <dpi_value>
```

### get_labels.py
Classifies images into predefined labels using LangChain and OpenAI GPT-4. The script utilizes `chain.abatch(...)` for API calling.

#### Usage 
```python
python scripts/get_labels.py \
    <images_path> \
    <batch_size> \
    (--return_exceptions) \
    --regex <pattern> \
    --sleep <sleep_time_in_seconds> \
    --output-path <output_file>
```

## Examples

#### Converting 20201119Complete_Denver_Zoning_Code_updated11122020.pdf to a set of images:
This command converts the specified PDF into PNG format images with a resolution of 300 dpi, and saves them in the data/ directory.
```python
python scripts/pdf-to-images.py \
    raw_data/20201119Complete_Denver_Zoning_Code_updated11122020.pdf \
    --output-dir data/ \
    --image-format png \
    --dpi 300
```

#### Converting 2022022-denver-green-code.pdf to a set of images:
This command converts the specified PDF into PNG format images with a resolution of 300 dpi, and saves them in the data/ directory.
```python
python scripts/pdf-to-images.py \
    raw_data/2022-denver-green-code.pdf \
    --output-dir data/ \
    --image-format png \
    --dpi 300
```

#### Classifying 20201119Complete_Denver_Zoning_Code_updated11122020.pdf images
Utilizes a batch size of 20, with a 1-minute sleep interval between batches.
```python
python scripts/get_labels.py data/ 20 \
    --regex "*_20201119Complete_Denver_Zoning_Code_updated11122020.png" \
    --sleep 60 \
    --output-path labels_file1.csv
```


#### Classifying 2022022-denver-green-code.pdf images
Utilizes a batch size of 20, with a 1-minute sleep interval between batches.
```python
python scripts/get_labels.py data/ 20 \
    --regex "*_2022-denver-green-code.png" \
    --sleep 60 \
    --output-path labels_file1.csv
```
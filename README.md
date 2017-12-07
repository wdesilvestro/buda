# Bulk Uniform Document Analyzer (BUDA)

BUDA is a document analysis tool written in Python. Inspired by the tedious nature of reviewing standard government documents, BUDA offers an efficient and reliable alternative to parse standardized documents in bulk. Let BUDA do the research for you!

## Prerequisites

BUDA relies upon some standard Python libraries that should already come installed with most Python installations:

- json
- os
- re
- xml.etree
- argparse

Besides these libraries, you may optionally want to install `pdfminer.six`, which is the Python 3 version of the popular `pdfminer` pdf parsing library. This is only required for running the `converter` Bash script if you wish to bulk convert your .pdf files to .txt format. This may be necessary as BUDA only accepts .txt files.

## Converting PDF Files to TXT Format *(Optional)*
As previously stated, BUDA only accepts `.txt` files and thus you may need to convert files of other types to this format for them to work with BUDA. Since most standard government documents and other uniform types of files come in PDF format, BUDA includes a Bash script to help you automate this process.

Located in the root directory of the project is a file called `converter`. It assumes that your system has `pdfminer.six` installed system wide or otherwise it will not work. PDFminer also comes with a `pdf2txt.py` script which should be placed in the same directory as this Bash script along with all the PDF files you wish to convert. The root directory of this project includes the PDFminer script for quick access if you've lost it since installation.

### Example
```
sh converter
```

## Constructing an XML Template
BUDA requires you to provide a template for it to understand the format of your files and how to parse them appropriately. This template must be formatted with Extensible Markup Language (XML) and be valid per XML 1.0 standards for BUDA to parse it correctly. These XML templates are demarcated with [regular expressions](https://en.wikipedia.org/wiki/Regular_expression), which tell BUDA how to search through and interpret your documents.

Below is an example template:
```XML
<?xml version="1.0"?>
<template>
    <container name="consent_agenda" start="\nCONSENT AGENDA\n\n" end="\nREGULAR AGENDA\n\n">
        <record name="committee" start="(Recommendation of the |Recommendations of the )(.*)" group="2">
            <record name="recommendation" start="(\n)(\d+)(\n\n)" group="2">
                <element name="id" group="2">(\n)(\d+)(\n\n)</element>
                <element name="title" group="2">(\n\[)([^\]]+)(]\n)</element>
                <element name="description" group="2" flags="re.DOTALL">(\n\[[^\]]+]\n)(.+?)\n([A-Z\s]+)\s</element>
                <element name="vote" group="3" flags="re.DOTALL">(\n\[[^\]]+]\n)(.+?)\n([A-Z\s]+)\s</element>
            </record>
        </record>
    </container>
</template>
```

### General Structure
Notice that all templates are enclosed by `<template>` and `</template>` tags respectively. Within a template structure, three types of tags exist:
- **Containers** - These are *static* positions within your document that tell BUDA where to look. You can have as many consecutive containers (or nested ones) as you would like, however you must specify a `start` and `end` attribute for each. All documents should contain these containers and they do not contain unique content. It's common to link them to section headers of a document to point BUDA to a consistent area of your document each time. ALL templates **must** contain at least one parent container at the root level (no random records exposed)!
- **Records** - These are `dynamic` positions within your document that assist BUDA with the actual data extraction process. You need only provide a `start` attribute as each new record marks the end of a previous one (and the last record simply stops where its parent container or record ends). The regular expression you provide for the starting position of the record will be its corresponding name in the exported data file.
- **Elements** - These are specific informational attributes of each record that you want to extract from your documents. Unlike containers or records, the regular expression to search for an element is contained *between* tags, **not** *within*.

The most basic attribute BUDA asks for is `name`, which is simply the name of the container, record, or element in the template. This will be used for identification purposes in the exported data file.

### Capturing Groups
You might also notice that BUDA accepts a few more attributes than just `start`, `end`, and `name`. BUDA supports capturing groups from regular expressions (**for records and elements only**) through the `group` attribute. Simply provide the number of the group that should actually be stored in the exported data file and BUDA will handle parsing the regular expression appropriately.

### Flags
BUDA also has support for the following regular expression flags:
- re.ASCII
- re.IGNORECASE
- re.LOCALE
- re.MULTILINE
- re.DOTALL
- re.VERBOSE

Provide as many flags as needed within the `flags` attribute in comma-separated form. Make sure you include **no** spaces between commas/flags!

## Running BUDA
BUDA is a script you can run with Python 3 in the following form:

```
python3 buda.py TEMPLATE_DIR INPUT_DIR OUTPUT_DIR -a
```

`TEMPLATE_DIR` indicates the location to the XML template used to parse the documents. `INPUT_DIR` and `OUTPUT_DIR` are the directories where the .txt files and exported .json files will be sent to respectively.

The optional `-a` parameter indicates whether or not the data should be exported in aggregate or not. Without the parameter, BUDA processes a .json file for each .txt file individually. With it, BUDA will merge the .json files and export one json file at the `OUTPUT_DIR` location called `aggregate.json`. An important note about the aggregate option is that records of the same name will be combined, with their elements replaced by the last record to be combined into that record name. This is generally the behavior you want as long as you construct your templates accordingly!

## Authors

* **Wesley De Silvestro** - [wadesilvestro](https://github.com/wadesilvestro)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for more details.
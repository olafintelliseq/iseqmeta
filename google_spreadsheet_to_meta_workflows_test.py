#!/usr/bin/env python3

from src.google_spreadsheet_to_meta_workflows import *

def test_get_workflows():
    test_data = {
        "author": "https://gitlab.com/olaf.tomaszewski",
        "copyright": "Copyright 2019-2021 Intelliseq",
        "name": "example name",
        "input_sample_id": {
            "index": 1,
            "name": "Sample id",
            "multiselect": False,
            "type": "String",
            "description": "Enter a sample name (or identifier)"
        },
        "input_fastqs": {
            "index": 2,
            "paired": True,
            "multiselect": True,
            "name": "Fastq files",
            "type": "Array[File]",
            "description": "Choose list of paired gzipped fastq files both left and right [.fq.gz or .fastq.gz]",
            "extension": [
                ".fq.gz",
                ".fastq.gz"
            ]
        }
    }

    expected = ["author", "copyright", "name"]
    result = get_workflows(test_data)

    assert result.sort() == expected.sort()


def test_get_inputs():
    test_data = {
        "description": "example description",
        "changes": {
            "2.0.1": "",
            "2.0.0": "",
            "1.2.0": "",
            "1.1.0": "",
            "1.0.0": ""
        },
        "groupOutputs": {
            "logs": {
                "hReadableName": "Logs",
                "description": ""
            }
        },
        "input_sample_id": {
            "index": 1,
            "name": "Sample id",
            "multiselect": False,
            "type": "String",
            "description": "Enter a sample name (or identifier)"
        },
        "input_fastqs": {
            "index": 2,
            "paired": True,
            "multiselect": True,
            "name": "Fastq files",
            "type": "Array[File]",
            "description": "Choose list of paired gzipped fastq files both left and right [.fq.gz or .fastq.gz]",
            "extension": [
                ".fq.gz",
                ".fastq.gz"
            ]
        }
    }

    expected = ["input_sample_id", "input_fastqs"]

    result = get_inputs(test_data)

    assert result.sort() == expected.sort()


def test_get_outputs():
    test_data = {
        "copyright": "Copyright 2019-2021 Intelliseq",
        "name": "example name",
        "input_sample_id": {
            "index": 1,
            "name": "Sample id",
            "multiselect": False,
            "type": "String",
            "description": "Enter a sample name (or identifier)"
        },
        "variant6_input_phenotypes_description": {
            "hidden": True
        },
        "variant7_input_phenotypes_description": {
            "hidden": True
        },
        "output_html_report": {
            "name": "Report from genetic analysis in Polish",
            "type": "File",
            "copy": True,
            "description": "Report with results of the genetic analysis, html format, Polish version"
        },
        "output_docx_report": {
            "name": "Report from genetic analysis in Polish",
            "type": "File",
            "copy": True,
            "description": "Report with results of the genetic analysis, docx format, Polish version"
        }
    }

    expected = ["output_html_report","output_docx_report"]

    result = get_outputs(test_data)

    assert result.sort() == expected.sort()

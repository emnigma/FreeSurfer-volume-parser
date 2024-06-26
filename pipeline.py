import argparse
import json
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
from jinja2 import Environment, FileSystemLoader


def calculate_volumes(aseg_file, aparc_lh_file, aparc_rh_file):
    # Load data from CSV files
    aseg_df = pd.read_csv(aseg_file, sep="\t")
    aparc_lh_df = pd.read_csv(aparc_lh_file, sep="\t")
    aparc_rh_df = pd.read_csv(aparc_rh_file, sep="\t")

    # Calculate Hippocampi volume
    left_hippocampus = aseg_df["Left-Hippocampus"].values[0]
    right_hippocampus = aseg_df["Right-Hippocampus"].values[0]
    hippocampi_volume = (left_hippocampus + right_hippocampus) / 1000

    # Define regions for each lobe
    frontal_regions = [
        "caudalmiddlefrontal_volume",
        "lateralorbitofrontal_volume",
        "medialorbitofrontal_volume",
        "parsopercularis_volume",
        "parsorbitalis_volume",
        "parstriangularis_volume",
        "precentral_volume",
        "rostralmiddlefrontal_volume",
        "superiorfrontal_volume",
        "frontalpole_volume",
    ]
    temporal_regions = [
        "entorhinal_volume",
        "fusiform_volume",
        "inferiortemporal_volume",
        "middletemporal_volume",
        "parahippocampal_volume",
        "superiortemporal_volume",
        "temporalpole_volume",
        "transversetemporal_volume",
    ]
    occipital_regions = [
        "cuneus_volume",
        "lateraloccipital_volume",
        "lingual_volume",
        "pericalcarine_volume",
    ]
    parietal_regions = [
        "inferiorparietal_volume",
        "isthmuscingulate_volume",
        "postcentral_volume",
        "precuneus_volume",
        "superiorparietal_volume",
        "supramarginal_volume",
        "paracentral_volume",
    ]

    # Calculate the volumes for each lobe
    def sum_regions(lh_df, rh_df, regions):
        lh_volumes = lh_df[[f"lh_{region}" for region in regions]].sum(axis=1).values[0]
        rh_volumes = rh_df[[f"rh_{region}" for region in regions]].sum(axis=1).values[0]
        return lh_volumes + rh_volumes

    frontal_volume = sum_regions(aparc_lh_df, aparc_rh_df, frontal_regions) / 1000
    temporal_volume = sum_regions(aparc_lh_df, aparc_rh_df, temporal_regions) / 1000
    occipital_volume = sum_regions(aparc_lh_df, aparc_rh_df, occipital_regions) / 1000
    parietal_volume = sum_regions(aparc_lh_df, aparc_rh_df, parietal_regions) / 1000

    # Create the output dictionary
    volumes = [
        {"name": "Hippocampi (Combined)", "volume": hippocampi_volume},
        {"name": "Frontal Lobe", "volume": frontal_volume},
        {"name": "Temporal Lobe", "volume": temporal_volume},
        {"name": "Parietal Lobe", "volume": parietal_volume},
        {"name": "Occipital Lobe", "volume": occipital_volume},
    ]

    mock_patient_data = {
        "patient_id": "123456",
        "report_date": "January 1, 2023",
        "patient_info": {
            "name": "John Doe",
            "age": 45,
            "gender": "Male",
            "referring_physician": "Dr. Jane Smith",
        },
        "imaging_details": {
            "scan_type": "MRI",
            "scan_date": "December 31, 2022",
            "scanning_facility": "iCObrain-DM Imaging Center",
        },
        "regions": volumes,
        "prepared_by": "Dr. Jane Smith",
    }

    return mock_patient_data


@dataclass
class PatientInfo:
    name: str
    age: int
    gender: str
    referring_physician: str


@dataclass
class ImagingDetails:
    scan_type: str
    scan_date: str
    scanning_facility: str


@dataclass
class Region:
    name: str
    volume: Optional[float] = None
    normal_range_min: Optional[float] = None
    normal_range_max: Optional[float] = None


@dataclass
class PatientReport:
    patient_id: str
    report_date: str
    patient_info: PatientInfo
    imaging_details: ImagingDetails
    regions: List[Region]
    prepared_by: str


@dataclass
class NormalRange:
    regions: List[Region]


@dataclass
class MergedReport:
    patient_id: str
    report_date: str
    patient_info: PatientInfo
    imaging_details: ImagingDetails
    regions: List[Region]
    prepared_by: str


def load_patient_report(data: dict) -> PatientReport:
    patient_info = PatientInfo(**data["patient_info"])
    imaging_details = ImagingDetails(**data["imaging_details"])
    regions = [Region(name=r["name"], volume=r["volume"]) for r in data["regions"]]
    return PatientReport(
        patient_id=data["patient_id"],
        report_date=data["report_date"],
        patient_info=patient_info,
        imaging_details=imaging_details,
        regions=regions,
        prepared_by=data["prepared_by"],
    )


def load_normal_range(data: dict) -> NormalRange:
    regions = [
        Region(
            name=r["name"],
            normal_range_min=r["normal_range_min"],
            normal_range_max=r["normal_range_max"],
        )
        for r in data["regions"]
    ]
    return NormalRange(regions=regions)


def merge_reports(
    patient_report: PatientReport, normal_range: NormalRange
) -> MergedReport:
    merged_regions = []
    for pr in patient_report.regions:
        for nr in normal_range.regions:
            if pr.name == nr.name:
                merged_regions.append(
                    Region(
                        name=pr.name,
                        volume=pr.volume,
                        normal_range_min=nr.normal_range_min,
                        normal_range_max=nr.normal_range_max,
                    )
                )
                break
    return MergedReport(
        patient_id=patient_report.patient_id,
        report_date=patient_report.report_date,
        patient_info=patient_report.patient_info,
        imaging_details=patient_report.imaging_details,
        regions=merged_regions,
        prepared_by=patient_report.prepared_by,
    )


def generate_html(patient_data_file, reference_data_file, template_dir, output_file):
    # Load data
    with open(patient_data_file) as f:
        patient_data = json.load(f)

    with open(reference_data_file) as f:
        reference_data = json.load(f)

    patient_report = load_patient_report(patient_data)
    normal_range = load_normal_range(reference_data)
    merged_report = merge_reports(patient_report, normal_range)

    env = Environment(loader=FileSystemLoader(template_dir))

    template = env.get_template("index.html")
    html = template.render(data=merged_report.__dict__)

    with open(output_file, "w") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(
        description="Brain volume analysis and HTML generation pipeline."
    )
    subparsers = parser.add_subparsers(dest="command")

    # Parser for volume calculation
    volume_parser = subparsers.add_parser(
        "calculate_volumes", help="Calculate brain region volumes."
    )
    volume_parser.add_argument(
        "--aseg", required=True, help="Path to the aseg_volume.csv file"
    )
    volume_parser.add_argument(
        "--aparc_lh", required=True, help="Path to the aparc_lh_volume.csv file"
    )
    volume_parser.add_argument(
        "--aparc_rh", required=True, help="Path to the aparc_rh_volume.csv file"
    )
    volume_parser.add_argument(
        "--output-json", required=True, help="Path to the output JSON file"
    )

    # Parser for HTML generation
    html_parser = subparsers.add_parser(
        "generate_html", help="Generate HTML from JSON data using Jinja2 templates."
    )
    html_parser.add_argument(
        "--data-file", required=True, help="Path to the data JSON file."
    )
    html_parser.add_argument(
        "--reference-data-file",
        required=True,
        help="Path to the reference data JSON file.",
    )
    html_parser.add_argument(
        "--template-dir",
        required=True,
        help="Directory containing the Jinja2 templates.",
    )
    html_parser.add_argument(
        "--output-file", required=True, help="Path to the output HTML file."
    )

    args = parser.parse_args()

    if args.command == "calculate_volumes":
        volumes = calculate_volumes(args.aseg, args.aparc_lh, args.aparc_rh)
        with open(args.output_json, "w") as f:
            json.dump(volumes, f, indent=4)
    elif args.command == "generate_html":
        generate_html(
            args.data_file,
            args.reference_data_file,
            args.template_dir,
            args.output_file,
        )


if __name__ == "__main__":
    main()

import argparse
import json
from dataclasses import asdict, dataclass
from typing import List, Optional

import pandas as pd
from dacite import from_dict
from jinja2 import Environment, FileSystemLoader


def calculate_volumes(aseg_file, aparc_lh_file, aparc_rh_file) -> list["RegionVolume"]:
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
        "superiorfrontal_volume",
        "rostralmiddlefrontal_volume",
        "caudalmiddlefrontal_volume",
        "parsopercularis_volume",
        "parstriangularis_volume",
        "parsorbitalis_volume",
        "lateralorbitofrontal_volume",
        "medialorbitofrontal_volume",
        "frontalpole_volume",
        "precentral_volume",
        "paracentral_volume",
    ]
    temporal_regions = [
        "entorhinal_volume",
        "parahippocampal_volume",
        "temporalpole_volume",
        "fusiform_volume",
        "superiortemporal_volume",
        "middletemporal_volume",
        "inferiortemporal_volume",
        "transversetemporal_volume",
        "bankssts_volume",
    ]
    occipital_regions = [
        "lingual_volume",
        "pericalcarine_volume",
        "cuneus_volume",
        "lateraloccipital_volume",
    ]
    parietal_regions = [
        "postcentral_volume",
        "supramarginal_volume",
        "superiorparietal_volume",
        "inferiorparietal_volume",
        "precuneus_volume",
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

    regions = [
        RegionVolume("Hippocampi", hippocampi_volume),
        RegionVolume("Frontal Lobe", frontal_volume),
        RegionVolume("Temporal Lobe", temporal_volume),
        RegionVolume("Parietal Lobe", parietal_volume),
        RegionVolume("Occipital Lobe", occipital_volume),
    ]

    return regions


@dataclass
class PatientInfo:
    name: str
    age: float
    gender: str
    referring_physician: str


@dataclass
class ImagingDetails:
    scan_type: str
    scan_date: str
    scanning_facility: str


@dataclass
class RegionVolume:
    name: str
    volume: Optional[float] = None


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
    prepared_by: str
    regions: List[Region] = None


@dataclass
class NormalRange:
    regions: List[Region]


def create_patient_json(
    aseg_file: str,
    aparc_lh_file: str,
    aparc_rh_file: str,
    patient_report_json_file: str,
) -> PatientReport:
    with open(patient_report_json_file, "r") as f:
        patient_report = from_dict(PatientReport, json.loads(f.read()))

    patient_report.regions = calculate_volumes(aseg_file, aparc_lh_file, aparc_rh_file)

    return patient_report


def load_patient_report(data: dict) -> PatientReport:
    return from_dict(PatientReport, data)


def load_normal_range(data: dict, gender: str, age: float) -> NormalRange:
    region_data = None
    for _, v in data.items():
        if v["min_age"] <= age <= v["max_age"]:
            region_data = v[gender]["regions"]

    if region_data is None:
        raise ValueError(f"No reference data found for age {age}")

    regions = [
        Region(
            name=name,
            normal_range_min=reg_stats["min"],
            normal_range_max=reg_stats["max"],
        )
        for name, reg_stats in region_data.items()
    ]

    return NormalRange(regions=regions)


def merge_reports(
    patient_report: PatientReport, normal_range: NormalRange
) -> PatientReport:
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
    patient_report.regions = merged_regions
    return patient_report


def generate_html(patient_data_file, reference_data_file, template_dir, output_file):
    with open(patient_data_file) as f:
        patient_data = json.loads(f.read())

    with open(reference_data_file) as f:
        reference_data = json.loads(f.read())

    patient_report = from_dict(PatientReport, patient_data)
    normal_range = load_normal_range(
        reference_data,
        gender=patient_report.patient_info.gender,
        age=patient_report.patient_info.age,
    )
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
        "create_patient_data",
        help="Calculate brain region volumes and merge it with patient metadata.",
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
        "--metadata",
        required=True,
        help="Path to .json with patient metadata (see `PatientInfo`)",
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

    if args.command == "create_patient_data":
        patient_report = create_patient_json(
            args.aseg, args.aparc_lh, args.aparc_rh, args.metadata
        )
        with open(args.output_json, "w") as f:
            json.dump(asdict(patient_report), f, indent=4)
    elif args.command == "generate_html":
        generate_html(
            args.data_file,
            args.reference_data_file,
            args.template_dir,
            args.output_file,
        )


if __name__ == "__main__":
    main()

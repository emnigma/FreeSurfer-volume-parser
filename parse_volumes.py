import argparse
import pandas as pd
import json


def calculate_volumes(aseg_file, aparc_lh_file, aparc_rh_file):
    # Load data from CSV files
    aseg_df = pd.read_csv(aseg_file, sep="\t")
    aparc_lh_df = pd.read_csv(aparc_lh_file, sep="\t")
    aparc_rh_df = pd.read_csv(aparc_rh_file, sep="\t")

    # Calculate Hippocampi volume
    left_hippocampus = aseg_df["Left-Hippocampus"].values[0]
    right_hippocampus = aseg_df["Right-Hippocampus"].values[0]
    hippocampi_volume = left_hippocampus + right_hippocampus

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

    return volumes


def main():
    parser = argparse.ArgumentParser(
        description="Calculate brain region volumes from FreeSurfer outputs."
    )
    parser.add_argument(
        "--aseg", required=True, help="Path to the aseg_volume.csv file"
    )
    parser.add_argument(
        "--aparc_lh", required=True, help="Path to the aparc_lh_volume.csv file"
    )
    parser.add_argument(
        "--aparc_rh", required=True, help="Path to the aparc_rh_volume.csv file"
    )

    args = parser.parse_args()

    volumes = calculate_volumes(args.aseg, args.aparc_lh, args.aparc_rh)

    print(json.dumps(volumes, indent=4))


if __name__ == "__main__":
    main()

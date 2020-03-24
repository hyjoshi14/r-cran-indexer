import argparse
import logging
from multiprocessing import Pool
from random import sample

import requests

from app import Package, session
from app.main.data.package_info import extract_package_info

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Backfill packages for R CRAN Indexer.")
parser.add_argument(
    "--processes",
    dest="N_PROCESSES",
    default=4,
    type=int,
    help="Number of processes to use for backfill. Defaults to 4.",
)
parser.add_argument(
    "--packages",
    dest="N_PACKAGES",
    default=100,
    type=int,
    help="Number of packages to backfill data for. Defaults to 100. Max is 10000.",
)


def backfill_package(package_name, version):
    try:
        logging.info(f"Backfilling description data for {package_name}_{version}")
        package_info = extract_package_info(package_name, version)
        logging.info(f"Saving data for {package_name}_{version}")
        save_package_info(package_info)
        logging.info(f"Backfilled description data for {package_name}_{version}")
        return 1
    except:
        logging.exception(f"Failed to backffill for {package_name}_{version}")
        return 0


def save_package_info(package_info):
    session.add(Package(**package_info))
    session.commit()


def get_packages(n_packages=100):
    logging.info(f"Obtaining random list of {n_packages} packages from CRAN")
    response = requests.get(
        "https://cran.r-project.org/src/contrib/PACKAGES", stream=True
    )
    raw_data = (line.decode("utf-8") for line in response.iter_lines())
    raw_data = (
        line.split(":")[-1].strip()
        for line in raw_data
        if line.startswith(("Package", "Version"))
    )
    logging.info(f"Obtained random list of {n_packages} packages from CRAN")
    sample_size = min(n_packages, 10000)
    # Convert to tuples of (Package, Version) and random sample packages
    return sample(list(zip(raw_data, raw_data)), sample_size)


if __name__ == "__main__":
    args = parser.parse_args()

    logging.info("Deleting exsiting data.")
    session.query(Package).delete()
    session.commit()
    logging.info("Deleted exsiting data.")

    logging.info("Backfilling data.")
    with Pool(args.N_PROCESSES) as p:
        packages_backfilled = sum(
            (p.starmap(backfill_package, get_packages(args.N_PACKAGES)))
        )
        logging.info(
            f"Backfilled {packages_backfilled} out of {args.N_PACKAGES} packages."
        )

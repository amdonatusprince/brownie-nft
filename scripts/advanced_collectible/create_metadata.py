from distutils.command.upload import upload
from importlib.metadata import metadata
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def main():
    advanced_collectible = AdvancedCollectible[-1]
    no_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {no_of_advanced_collectibles} collectibles!")
    for token_id in range(no_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(metadata_filename)

    collectible_metadata = metadata_template

    if Path(metadata_filename).exists():
        print(f"{metadata_filename} already exists! Delete it to overwrite")
    else:
        print(f"creating Metadata file: {metadata_filename}")
        collectible_metadata["name"] = breed
        collectible_metadata["decription"] = f"An adorable {breed} pup!"
        print(collectible_metadata)
        image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
        image_uri = upload_to_ipfs(image_path)
        collectible_metadata["image"] = image_uri

        with open(metadata_filename, "w") as file:
            json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_filename)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001/webui"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


import json
import urllib.request
from pathlib import Path

NUVIO_STORE_URL = (
    "https://raw.githubusercontent.com/"
    "NuvioMedia/NuvioDesktop/Dev/store.json"
)

SOURCE_FILE = Path("source.json")


def fetch_json(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "nuvio-sidestore-source"
        },
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def main():
    store = fetch_json(NUVIO_STORE_URL)

    # Nuvio's store.json already contains the iOS app metadata
    nuvio_app = store["apps"][0]

    versions = []

    for version in nuvio_app.get("versions", []):
        entry = {
            "version": version["version"],
            "buildVersion": version["buildVersion"],
            "date": version["date"],
            "downloadURL": version["downloadURL"],
            "size": version["size"],
        }

        if version.get("localizedDescription"):
            entry["localizedDescription"] = version["localizedDescription"]

        if version.get("minOSVersion"):
            entry["minOSVersion"] = version["minOSVersion"]

        versions.append(entry)

    source = {
        "name": "Nuvio",
        "identifier": "com.jannis0906.nuvio-source",
        "subtitle": "Nuvio for SideStore",
        "description": (
            "Unofficial SideStore source using official "
            "NuvioMedia release files."
        ),
        "apps": [
            {
                "name": nuvio_app["name"],
                "bundleIdentifier": nuvio_app["bundleIdentifier"],
                "developerName": nuvio_app.get(
                    "developerName",
                    "NuvioMedia"
                ),
                "subtitle": nuvio_app.get(
                    "subtitle",
                    "Nuvio"
                ),
                "localizedDescription": nuvio_app.get(
                    "localizedDescription",
                    "Nuvio media application"
                ),
                "iconURL": nuvio_app["iconURL"],
                "versions": versions,
            }
        ],
    }

    SOURCE_FILE.write_text(
        json.dumps(source, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"Updated source.json with "
        f"{len(versions)} Nuvio versions."
    )


if __name__ == "__main__":
    main()

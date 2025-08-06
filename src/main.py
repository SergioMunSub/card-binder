
from core.card_downloader import download_cards


def main(packs: list, tcg_game: str ="yugioh_cards"):
    for pack in packs:
        download_cards(pack)
    print("\n Download completed.")

    return





if __name__ == "__main__":
    packs = [
    "Legend of Blue Eyes White Dragon",
    "Metal Raiders",
    "The Duelist Genesis"
    ]

    main(packs)
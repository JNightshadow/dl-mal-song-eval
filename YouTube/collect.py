# songs = {
#     "Ikkarayanente_Thamasam": [
#         "Ikkarayanente Thamasam cover",
#         "Ikkarayanathe Thamasam cover",
#         "ഇക്കരയന്റെ താമസം cover"
#     ],
#     "Poovukalk_Punyakalam": [
#         "Poovukalk Punyakalam cover",
#         "Poovukalku Punyakalam cover"
#     ],
#     "Nalacharithathile_Naayakano": [
#         "Nalacharithathile Naayakano cover",
#         "Nalacharithathile Nayakano cover"
#     ],
#     "Kuppivala_Kaikalil": [
#         "Kuppivala kaikalil cover",
#         "Kuppivala kaikalil Mayilanchi cover"
#     ],
#     "Pinneyum_Pinneyum": [
#         "Pinneyum Pinneyum cover"
#     ],
#     "Thumbi_Vaa": [
#         "Thumbi Vaa cover"
#     ],
#     "Thumbayum_Thulasiyum": [
#         "Thumbayum Thulasiyum cover"
#     ],
#     "Kannam_Thumbi": [
#         "Kannam Thumbi cover"
#     ]
# }
songs = {
    "Sreeraagamo_Thedunnu": [
        "Sreeraagamo Thedunnu cover",
        "Sreeragamo Thedunnu cover",
        "ശ്രീരാഗമോ തേടുന്നു cover"
    ],

    "Maanikya_Veenayumaayen": [
        "Maanikya Veenayumaayen cover",
        "Manikya Veenayumayen cover"
    ],

    "Kannam_Thumbi": [
        "Kannam Thumbi cover"
    ],

    "Kadalinakkare_Ponore": [
        "Kadalinakkare Ponore cover"
    ],

    "Paattupaadiyurakkaam": [
        "Paattupaadiyurakkaam cover",
        "Pattu Paadiyurakkam cover"
    ],

    "Pathinezhinte_Poomkaralil": [
        "Pathinezhinte Poomkaralil cover"
    ],

    "Chirikubol_Koode_Chirikkan": [
        "Chirikubol Koode Chirikkan cover"
    ],

    "Priyathama_Priyathama_Pranayalekhanam": [
        "Priyathama Priyathama Pranayalekhanam cover"
    ],

    "Kathirippoo_Kanmani": [
        "Kathirippoo Kanmani cover"
    ],

    "Poomugha_Vaathilkal_Sneham": [
        "Poomugha Vaathilkal Sneham cover",
        "Poomugha Vathilkal Sneham cover"
    ],

    "Poomaname": [
        "Poomaname cover"
    ],

    "Kasthoori_Manakkunnallo": [
        "Kasthoori Manakkunnallo cover",
        "Kasturi Manakkunnallo cover"
    ],

    "Poonkatinodum_Kilikalodum": [
        "Poonkatinodum Kilikalodum cover"
    ],

    "Vaishaga_Sandhye": [
        "Vaishaga Sandhye cover",
        "Vaishakha Sandhye cover"
    ]
}


import subprocess
import os

BASE_DIR = "covers_dataset"
os.makedirs(BASE_DIR, exist_ok=True)

for folder, queries in songs.items():
    song_dir = os.path.join(BASE_DIR, folder)
    os.makedirs(song_dir, exist_ok=True)

    print(f"\nDownloading covers for: {folder}")

    video_ids = set()

    for q in queries:
        cmd = ["yt-dlp", f"ytsearch30:{q}", "--get-id"]
        try:
            out = subprocess.check_output(cmd).decode().splitlines()
            video_ids.update(out)
        except subprocess.CalledProcessError:
            pass

    for vid in video_ids:
        url = f"https://www.youtube.com/watch?v={vid}"
        download_cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "wav",
            "--audio-quality", "0",
            "-o", f"{song_dir}/%(id)s.%(ext)s",
            url
        ]
        subprocess.run(download_cmd)

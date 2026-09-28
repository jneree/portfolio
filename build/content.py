"""Everything the site says lives here: copy, image order and captions.

Image paths are relative to one of the source roots in build.py:
  "Ryder/...", "Soundbrenner/...", "Transcelestial/..."  -> ~/Downloads/julneree.com images
  "c2m/..."                                              -> ~/Downloads/julneree-concept-to-manufacturing/videos
  "larkin/...", "writing/..."                            -> build/sources
Edit captions or reorder items, then run `python build/build.py`.
"""


def img(src, cap="", alt=None):
    return {"type": "img", "src": src, "cap": cap, "alt": alt or cap}


def vid(src, cap="", start=0, dur=None):
    return {"type": "vid", "src": src, "cap": cap, "start": start, "dur": dur}


SITE = {
    "title": "Julien Nérée — Hardware product engineer & designer",
    "description": "Julien Nérée takes hardware from the first sketch to mass production. "
                   "Ryder, Transcelestial, Soundbrenner, and now Larkin.",
    "url": "https://julneree.com/",
    "name": "Julien Nérée",
    "statement": "I take hardware from the first sketch to mass production.",
    "sub": "Product engineer and designer. Ten years building consumer electronics between "
           "Hong Kong, Shenzhen and Singapore: industrial design, electronics, packaging, "
           "factories. I also photograph what I ship.",
    "stats": [
        ("200,000+", "devices shipped"),
        ("10 years", "in Shenzhen supply chains"),
        ("Red Dot", "Design Award 2026"),
    ],
    "hero_image": img("Ryder/IMG_2412.JPG", "At our assembly partner in Shenzhen, Ryder One mass production."),
    "links": [
        ("LinkedIn", "https://www.linkedin.com/in/julneree/"),
        ("Instagram", "https://www.instagram.com/julien_neree/"),
        ("X", "https://twitter.com/julneree"),
    ],
}

# Filter keys, in the order they appear in the "What I do" index.
CATEGORIES = [
    ("design", "Industrial & Mechanical Design"),
    ("electronics", "Electronics"),
    ("ux", "App & Device UX"),
    ("packaging", "Packaging"),
    ("accessories", "Accessories"),
    ("prototypes", "Fully Functional Prototypes"),
    ("molding", "Injection Molding & Finishing"),
    ("production", "Mass Production"),
    ("team", "Manufacturing & Design Team"),
    ("unboxing", "Product Unboxing"),
    ("photo", "Product Shots"),
]

PHASES = [
    ("Development", ["design", "electronics", "ux", "packaging", "accessories"]),
    ("Manufacturing", ["prototypes", "molding", "production", "team"]),
    ("Launch", ["unboxing"]),
]

NOW = {
    "id": "larkin",
    "name": "Larkin",
    "years": "2026 — now",
    "role": "Founder",
    "place": "Singapore",
    "url": "https://getlarkin.com",
    "intro": "Larkin is an AI wristband with no screen and nothing to press. It listens through "
             "your day and gives it back as something you can read, learn from and build on. "
             "I'm building all of it: the band, the app and the AI behind it. Reservations are "
             "open and the first units ship in Q1 2027.",
    "items": [
        img("larkin/band-ring-1200.webp", "The light ring. Green means it's listening."),
        img("larkin/band-desk-1200.webp", "Larkin band."),
        img("larkin/band-sill-700.webp", "Larkin band, silver."),
        img("larkin/band-wrist-white-1400.webp", "On the wrist."),
        img("larkin/app-chronicles-720.webp", "Chronicles: every day becomes a chapter."),
        img("larkin/app-day-720.webp", "Day view: who you talked to, what came up."),
    ],
}

COMPANIES = [
    {
        "id": "ryder",
        "num": "01",
        "name": "Ryder",
        "years": "2022 — 2026",
        "role": "Co-founder & CPO",
        "place": "Singapore, with monthly trips to Shenzhen at peak",
        "url": "https://www.ryder.id/",
        "hero": img("Ryder/02_product-shot.jpg", "Ryder One."),
        "intro": "Ryder One is a crypto hardware wallet without a seed phrase. Instead of writing "
                 "24 words on paper, you back it up by tapping Recovery Tags or with people you "
                 "trust. I co-founded the company and led product end to end: the device, the app, "
                 "the recovery experience, packaging, manufacturing and launch.",
        "facts": [
            ("Achievements", [
                "$3.2M seed round led by Tim Draper",
                "2,000+ units shipped",
                "Red Dot Design Award 2026",
                "4.8 rating on Trustpilot",
                "Halborn security audit: 0 critical, 0 high findings",
            ]),
            ("Responsibilities", [
                "Product vision and positioning",
                "Hardware UX and industrial design direction",
                "Manufacturing with our suppliers in China: DFM, tooling, assembly, QC and ramp-up",
                "Led our UX/UI designer across the iOS and Android apps",
                "Recovery Tags, packaging and accessories",
                "Website, launch, product photography and video direction",
            ]),
            ("Technical challenges", [
                "An EAL6+ secure element, encrypted NFC, Qi charging and a 1.6\" AMOLED touch screen "
                "in a pocket-size aluminium and glass body",
                "Wireless charging that still works on a dead battery",
                "Battery-free Recovery Tags that survive being dropped, soaked or lost",
                "Setup in under a minute, with every transaction confirmed on the device",
                "Matching colour and finish across anodized aluminium, glass and polycarbonate",
            ]),
        ],
        "rows": {
            "design": [
                img("Ryder/12_drawing3.png", "Foam mockups to lock the volume and how it sits in the hand."),
                img("Ryder/15_design-process.jpg", "Shape studies on the table during a design review."),
                img("Ryder/11_rendering.png", "CMF direction: finishes, materials and the references we benchmarked."),
                img("Ryder/13_prototyping2.jpg", "Looks-like prototype, checking proportions in hand."),
                img("Ryder/14_902ddb81-9859-42fa-970e-590bead8fb7b.png", "The back, with the embossed logo."),
                img("Ryder/10_dscf9812.jpg", "CNC aluminium frames and tempered glass before assembly."),
                vid("Ryder/IMG_2640.MP4", "Colour samples for the frame."),
            ],
            "electronics": [
                img("Ryder/17_screenshot_2026-04-19_at_7.09.17_pm.png", "Main board bring-up."),
                img("Ryder/18_screenshot_2026-04-19_at_6.43.12_pm.png", "Early firmware running next to the bare board and battery."),
                img("Ryder/IMG_2734.HEIC", "Main board and light guide inside the housing."),
                img("Ryder/20_screenshot_2026-04-19_at_7.11.59_pm.png", "Test mode reading temperature and battery voltage."),
                vid("Ryder/IMG_1980.MP4", "Charging coil modules, panel after panel."),
                img("Ryder/21_dscf0876.jpg", "Coil modules before final assembly."),
            ],
            "ux": [
                img("Ryder/01_app_ryder.png", "Ryder One and the Ryder app."),
                img("Ryder/04_screenshot_2026-07-03_at_5.28.51_pm.png", "Tap to sign. Every transaction is confirmed on the device, over encrypted NFC."),
                img("Ryder/19_img_0817.jpg", "On-device flow: creating a wallet."),
                img("Ryder/03_42c93a99-7a3c-4768-b668-465fd75911a1.png", "Confirming on the 1.6\" touch screen."),
                img("Ryder/06_b2b19ebd-5e1b-4365-969e-22e7c5dd67c6.png", "Device and app designed as one experience."),
                img("Ryder/07_screenshot_2026-07-03_at_3.49.16_pm.png", "The light bar tells you what the device is doing."),
            ],
            "packaging": [
                img("Ryder/08_screenshot_2026-07-03_at_3.49.56_pm.png", "Ryder One, Recovery Tags and accessories, each in its place."),
                img("Ryder/09_screenshot_2026-07-03_at_3.50.08_pm.png", "Opening the box."),
                img("Ryder/IMG_4411.JPG", "Packaging samples on the review table."),
            ],
            "prototypes": [
                img("Ryder/16_dscf1015.jpg", "Functional build: housing, main board, and the app running against it."),
                img("Ryder/Screenshot 2023-08-11 at 9.23.34 PM.png", "Measuring first parts against the drawings."),
                img("Ryder/IMG_2667.JPG", "Engineering build review with the factory team."),
            ],
            "molding": [
                vid("Ryder/IMG_5004.MOV", "Injection molding at our supplier.", 0, 10),
                vid("Ryder/IMG_5012.MOV", "Checking the first shots off the tool.", 14, 10),
                vid("Ryder/IMG_9883.MOV", "Hand spray finishing.", 0, 10),
                img("Ryder/IMG_9882.HEIC", "The spray booth."),
                img("Ryder/23_screenshot_2026-07-03_at_10.26.26_pm.png", "Anodizing line for the aluminium frames."),
            ],
            "production": [
                img("Ryder/22_screenshot_2026-07-03_at_10.32.26_pm.png", "On the line myself during ramp-up."),
                img("Ryder/IMG_0628.JPG", "Final assembly and packing line."),
                img("Ryder/IMG_0644.JPG", "Packing and final QC."),
                img("Ryder/24_screenshot_2026-07-03_at_9.33.05_pm.png", "Finished units."),
                img("Ryder/IMG_1122.JPG", "First mass-production cartons."),
            ],
            "team": [
                img("Ryder/25_7938b8e0-49b9-42aa-9174-fb84a12ccaff.png", "Visiting our assembly partner in Shenzhen."),
                img("Ryder/IMG_3185.JPG", "Design review with our supplier's engineers."),
                img("Ryder/IMG_4604.JPG", "Lunch with a supplier."),
                img("Ryder/IMG_4979.JPG", "Team dinner after a build."),
            ],
        },
    },
    {
        "id": "transcelestial",
        "num": "02",
        "name": "Transcelestial",
        "years": "2021 — 2022",
        "role": "Technical Program Manager, Manufacturing & Software",
        "place": "Singapore",
        "url": "https://transcelestial.com/",
        "hero": img("Transcelestial/AIP_EDI_Transcelestial_2022-06-16_FR_003.jpg", "In the Transcelestial lab, Singapore."),
        "intro": "Transcelestial builds wireless laser communication terminals: fibre-speed links "
                 "through the air, without digging trenches or buying spectrum. The long-term goal "
                 "is a laser network in space. I joined after Entrepreneur First to help move the "
                 "CENTAURI terminals from lab builds to a production process that hits its targets.",
        "facts": [
            ("Achievements", [
                "Scope grew from manufacturing to manufacturing and software after 9 months",
                "Set the delivery cadence for four engineering teams",
            ]),
            ("Responsibilities", [
                "Coordinated software, PAT (pointing, acquisition and tracking), electrical and mechanical teams",
                "Production targets and yield",
                "Action plans, and flagging execution risks early",
                "Technical reviews to keep improving yield and manufacturing processes",
                "From May 2022: product roadmap and R&D initiatives",
            ]),
            ("Technical challenges", [
                "Laser terminals that have to stay aligned over long distances, outdoors",
                "Going from hand-built units to a repeatable, measurable production process",
                "Keeping four disciplines on one roadmap",
            ]),
        ],
        "row_labels": {"production team": "Lab and team"},
        "rows": {
            "production team": [
                img("Transcelestial/20220616_105129.jpg", "Assembly bench in the lab."),
                img("Ryder/30_team-pic.jpg", "The Transcelestial team."),
            ],
        },
    },
    {
        "id": "soundbrenner",
        "num": "03",
        "name": "Soundbrenner",
        "years": "2015 — 2021",
        "role": "Founding Engineer → NPI Engineer → Head of Hardware Product",
        "place": "Hong Kong and Shenzhen, half my time in each",
        "url": "https://www.soundbrenner.com/",
        "hero": img("Soundbrenner/02_05c8f054-816c-43fa-9eb3-75e77ce1629a_rw_1920.jpg", "Soundbrenner Core."),
        "loops": [
            vid("Soundbrenner/04_gif5.gif", "Our patented magnetic lock, on the wrist."),
            vid("Soundbrenner/05_f05ca42b-1611-449c-b912-9265147d2b05.gif", "Unlock it to tune an instrument, throw it back and it locks itself in place."),
        ],
        "intro": "Soundbrenner makes wearables for musicians. I joined in Hong Kong as the first "
                 "engineer, when nothing had shipped yet, and left as Head of Hardware Product after "
                 "200,000+ devices. The big one was Soundbrenner Core, the first smartwatch for "
                 "musicians: a vibrating metronome, a contact tuner and a dB meter in one. Two years "
                 "from concept to mass production.",
        "facts": [
            ("Achievements", [
                "200,000+ devices shipped",
                "$1.5M in Kickstarter pre-orders, the most crowdfunded project in Hong Kong",
                "1 patent, the magnetic lock",
                "500,000 monthly active users on the Soundbrenner app",
                "Retail displays in 130+ stores in the US, Germany and Japan",
            ]),
            ("Responsibilities", [
                "Product development from concept to mass production and launch",
                "Led a cross-functional team in Hong Kong and Shenzhen: mechanical, electrical, firmware, industrial design",
                "Owned the hardware roadmap",
                "Main contact with our OEMs in China",
                "Supply chain: second sources, lead times, costs and MOQs on a US$1M+ yearly budget",
                "EVT, DVT and PVT builds, root-cause analysis and corrective actions",
                "Early on, firmware in C: memory, battery management, Bluetooth with the apps",
            ]),
            ("Technical challenges", [
                "A 7G ERM vibration motor, 7x stronger than the average smartwatch",
                "A magnetic lock so the watch pops out of its base and becomes a contact tuner",
                "Keeping it thin despite both",
                "Firmware syncing up to 5 devices with less than 15ms delay, plus accurate tuning",
                "5+ days of battery life in daily use",
            ]),
        ],
        "rows": {
            "design": [
                img("Soundbrenner/09_mechanical0.jpg", "First drawings, built around the dimensions of the key electronic components."),
                img("Soundbrenner/10_mechanical_2.jpg", "First 3D print to check the overall volume."),
                img("Soundbrenner/11_mechanical_1.jpg", "A few iterations to confirm the ergonomics."),
                img("Soundbrenner/12_f9f929df-33c1-469f-8934-50855f2fa9ad_rw_3840.jpg", "Countless evaluations (and teardowns) of the products that inspired us."),
                img("Soundbrenner/13_3dprint-tests.jpg", "One mechanical part, 9 variants. It took around 30 iterations to get there."),
                img("Soundbrenner/15_mechanical_3.jpg", "High-quality mockups to decide on materials and dimensions."),
                img("Soundbrenner/16_material-choice.jpg", "Evaluating colours and materials."),
                img("Soundbrenner/17_design-review-dfm.jpg", "A DFM review. One of the hardest and most important steps."),
                img("Soundbrenner/18_steel-1-1.jpg", "Final product, with parts straight out of the molds."),
            ],
            "electronics": [
                img("Soundbrenner/19_board.jpg", "First board, to test and confirm our key components."),
                img("Soundbrenner/20_module.jpg", "Custom boards, sometimes just to validate one feature."),
                img("Soundbrenner/21_pcb.jpg", "First board at final dimensions, fitting the mechanical design."),
                img("Soundbrenner/22_electronics-testing-1.jpg", "Countless tests to cover every functional requirement."),
                img("Soundbrenner/23_process-build.jpg", "First build of boards placed in their casings."),
            ],
            "packaging": [
                img("Soundbrenner/24_packaging-firststep.jpg", "Studying other packaging for materials and dimensions."),
                img("Soundbrenner/25_process-packaging-mockup.jpg", "First prototype, only to confirm the experience. Looks don't matter yet."),
                img("Soundbrenner/26_process-prototype_packaging.jpg", "Mockups to evaluate design, materials and suppliers."),
                img("Soundbrenner/27_pen-packaging.jpg", "Final artwork."),
                img("Soundbrenner/28_process-packaging.jpg", "Golden sample, signed off for mass production."),
            ],
            "accessories": [
                img("Soundbrenner/14_Screen_Shot_2022-11-17_at_10.34.24_AM.png", "Straps got the same design refinement as the watch."),
                img("Soundbrenner/54_2020-07-01-Steel-1-scaled.jpg", "Everything included in the box."),
                img("Soundbrenner/55_2020-07-01-Straps2.jpg", "A full range of straps: leather, nylon and silicone."),
                img("Soundbrenner/03_straps-lineup-core.jpg", "The strap line-up."),
            ],
            "prototypes": [
                img("Soundbrenner/29_process-prototype.jpg", "First fully functional prototype. It took a few iterations to get every feature working."),
                img("Soundbrenner/30_iterated_prototype.jpg", "A lot of work on cosmetics. Here, the two screens were still too visible."),
                img("Soundbrenner/31_qc_tests-1-scaled.jpg", "Reliability testing, like humidity and drop tests."),
                img("Soundbrenner/32_process-prototype_3.jpg", "First unit confirmed ready for mass production."),
                img("Soundbrenner/33_first-build.jpg", "The first build of 20 devices. A few more builds before production ramped up."),
            ],
            "molding": [
                img("Soundbrenner/34_IMG_20190517_120014_1.jpg", "A mold starts as a large block of steel."),
                img("Soundbrenner/35_IMG_20190517_120137.jpg", "A few weeks later it's ready. You can see the 2 cavities."),
                img("Soundbrenner/36_IMG_20190517_120147.jpg", "One cavity. This mold is for the case."),
                img("Soundbrenner/37_IMG_20190517_152904_1.25.39_AM.jpg", "Colour mixing at our injection molding partner."),
                img("Soundbrenner/38_IMG_20190517_143641.jpg", "Adjustments to get the texture and colour right."),
                img("Soundbrenner/39_IMG_20190517_154259.jpg", "Which means a lot of rejected parts."),
                img("Soundbrenner/40_IMG_20190517_141812.jpg", "The mold goes into the injection machine."),
                vid("c2m/1-injection-molding-casings.mp4", "The mold making two casings."),
                vid("c2m/2-glass-sheet-cutting.mp4", "Cutting the top glass from a sheet."),
                vid("c2m/3-glass-cutting-polishing.mp4", "Each glass piece is cut and polished."),
                vid("c2m/4-laser-etching.mov", "Laser-etching the back of our Kickstarter backers' devices.", 0, 12),
            ],
            "production": [
                img("Soundbrenner/41_mass-production-materials.jpg", "All the parts from our suppliers, ready for mass production."),
                img("Soundbrenner/42_process-assembly.jpg", "Each operator learned one specific assembly task."),
                img("Soundbrenner/43_process-fixture1.jpg", "Some assembly issues needed custom fixtures and jigs."),
                img("Soundbrenner/44_process-assembly3.jpg", "The QC team. I spent a lot of hours with them setting the quality bar."),
                img("Soundbrenner/45_mass-production-testing-table.jpg", "My table on the line. Every issue had to be fixed fast while production kept running."),
                img("Soundbrenner/46_processs-assembly2.jpg", "The first devices out of the assembly line."),
                img("Soundbrenner/49_manufacturing-steel-scaled.jpg", "Devices charging on the line."),
                img("Soundbrenner/47_process-shipping2.jpg", "Packed and ready to ship."),
                img("Soundbrenner/48_mass-production-shipping.jpg", "After 2 years of work, the first cartons."),
            ],
            "team": [
                img("Soundbrenner/50_Screenshot_2022-10-30_at_10.20.27_PM.png", "Our line operators celebrating the first shipment."),
                img("Soundbrenner/51_assembly-guitar.jpg", "A guitar on the production line, to test the tuner. A first for our manufacturer."),
                img("Soundbrenner/52_testing-1.jpg", "Our mechanical and industrial designers testing materials."),
                img("Soundbrenner/53_management-team.jpg", "Our manufacturer's management team, after two years together."),
            ],
            "unboxing": [
                vid("c2m/5-unboxing-core.mov", "Unboxing Core.", 0, 20),
                vid("c2m/6-unboxing-core-steel.mov", "Unboxing Core Steel.", 0, 20),
            ],
        },
    },
]

VIDEOS = [
    ("WxOzGlUw5gI", "From the factory to your hands: we're finally shipping Ryder One"),
    ("ZnGElIaLUMY", "From concepts to Ryder One, with Ray Horacek, our industrial designer"),
    ("dIBUpqcWcp4", "Building Ryder One: address collection, production ramp-up and security audits"),
    ("aYknJ0h0--4", "We shipped. Here's what you need to know about Ryder One"),
    ("cQppFX0CwSI", "Ryder One unboxing"),
]

ARTICLES = [
    {
        "slug": "ledger-nano-x",
        "title": "Ledger Nano X — Unboxing and Onboarding Review",
        "date": "December 29, 2022",
        "kind": "Review",
        "description": "A hardware wallet review: packaging, materials, onboarding, and why the seed phrase is the problem.",
    },
    {
        "slug": "4-key-lessons",
        "title": "4 Key Lessons I Learned Working in Hardware Startups",
        "date": "June 8, 2022",
        "kind": "Article",
        "description": "Lessons from nearly a decade in hardware startups and 150,000+ devices shipped.",
    },
    {
        "slug": "from-concept-phase-to-manufacturing",
        "title": "From Concept to Mass Production of a Wearable Device",
        "date": "September 14, 2020",
        "kind": "Case study",
        "description": "How Soundbrenner Core went from the concept phase to mass production, in pictures.",
    },
]

# Studio work for the photography section, in display order.
PHOTOS = [
    img("Soundbrenner/57_DSCF3458.jpg", "Soundbrenner Core"),
    img("Ryder/05_screenshot_2026-07-03_at_3.47.16_pm.png", "Ryder One"),
    img("Soundbrenner/62_Tuner.jpg", "Soundbrenner Core, tuner"),
    img("Ryder/16_dscf1015.jpg", "Ryder One, exploded"),
    img("Soundbrenner/56_Steel_closeup-scaled.jpg", "Soundbrenner Core Steel"),
    img("Soundbrenner/65_Live-drums.jpg", "Soundbrenner Core, live"),
    img("Ryder/21_dscf0876.jpg", "Ryder One, coil modules"),
    img("Soundbrenner/59_SideSteel.jpg", "Soundbrenner Core Steel"),
    img("Soundbrenner/61_Tuner-Plastic2.jpg", "Soundbrenner Core, tuner"),
    img("Ryder/10_dscf9812.jpg", "Ryder One, frames and glass"),
    img("Soundbrenner/64_Bass3.jpg", "Soundbrenner Core, bass"),
    img("Soundbrenner/58_Steel-plastoc.jpg", "Soundbrenner Core and Core Steel"),
    img("Ryder/24_screenshot_2026-07-03_at_9.33.05_pm.png", "Ryder One"),
    img("Soundbrenner/01_Screen_Shot_2022-11-17_at_10.40.32_AM.png", "Soundbrenner Core"),
    img("Soundbrenner/66_dB-meter-scaled.jpg", "Soundbrenner Core, dB meter"),
    img("Soundbrenner/60_Assembly1-scaled.jpg", "Soundbrenner Core on the line"),
    img("Soundbrenner/63_Tuner-Plastic1.jpg", "Soundbrenner Core, tuner"),
    img("Soundbrenner/55_2020-07-01-Straps2.jpg", "Soundbrenner straps"),
]

ABOUT = {
    "portrait": img("Ryder/32_julien11_2.jpg", "Julien Nérée"),
    "text": [
        "I grew up in the French countryside and studied engineering in Paris. Since 2015 I've "
        "lived between Hong Kong, Shenzhen and Singapore, building products with the people who "
        "manufacture them.",
        "I like the whole thing: the first sketch, the DFM meeting that kills half the ideas, the "
        "first 20 units off the line, and the photo that finally makes it look as good as it is.",
    ],
    "before": [
        ("2021", "Entrepreneur First, Singapore", "Founder in residence. Started a solar venture. It didn't work out, I learned a lot."),
        ("2017", "Sofar Sounds, Hong Kong", "City leader. Launched it in Hong Kong on the side, monthly shows, all sold out."),
        ("2015", "Brandbodh, Pune", "Project manager assistant at a design and communication studio."),
        ("2013", "TEDxECE, Paris", "Founded the first TEDx at my engineering school. 8 speakers, 150 attendees."),
    ],
}

import time
from core.engine import Engine

class Launcher:
    def __init__(self):
        self.engine = Engine()
        print("Bot initialized...")

    def start(self):
        print("Bot starting up...")
        self.engine.load_urls([
            "https://tcr-therapies-summit.com/",
            "https://mrna-processmanufacturing.com/",
            "https://cell-therapy-analytics-europe.com/",
            "https://genetherapy-ophthalmology.com/",
            "https://lnp-characterization-analytical-development.com/",
            "https://genetherapy-immunogenicity.com/",
            "https://car-tcr-summit.com/",
            "https://inner-ear-disorders-therapeutics.com/",
            "https://lipid-nanoparticle-delivery-summit.com/",
            "https://mrnabased-therapeutics.com/",
            "https://gamma-delta-t-therapies-summit.com/",
            "https://in-vivo-engineering.com/",
            "https://process-development-celltx.com/",
            "https://peptide-based-therapeutics-summit.com/",
            "https://cdx-europe.com/",
            "https://lnp-formulation-process-development-pharma.com/",
            "https://genetherapy-conference.com/",
            "https://immuno-oncologyeurope.com/",
            "https://genetherapy-patient-engagement.com/",
            "https://mrna-quality-control.com/",
            "https://genetherapy-neurological-europe.com/",
            "https://cell-therapy-potency-assay.com/",
            "https://allogeneic-cell-therapies.com/",
            "https://ipsc-manufacturing-summit.com/",
            "https://genetherapy-analytical-europe.com/",
            "https://mrna-processmanufacturing-europe.com/",
            "https://genetherapy-comparability.com/",
            "https://supply-cell-immunotherapy.com/",
            "https://cartcr-europe.com/",
            "https://mrna-analytical-development.com/",
            "https://allogeneic-cell-therapies-europe.com/",
            "https://mrnabased-therapeutics-europe.com/",
            "https://cell-therapy-analytics.com/",
            "https://synthetic-biology-therapeutics-summit.com/",
            "https://dry-amd-therapeutics.com/",
            "https://crispr-conference.com/",
            "https://innate-killer-europe.com/",
            "https://macrophage-directed-therapies.com/",
            "https://b-and-t-cell-for-autoimmune.com/",
            "https://optimizing-aav-safety.com/",
            "https://innerear-disorders-therapeutics.com/",
            "https://multi-functional-cell-therapies.com/"
        ])
        self.engine.run()
        print("Bot finished!")

    def stop(self):
        print("Bot stopped!")

if __name__ == "__main__":
    bot = Launcher()
    # Press play here in PyCharm!
    bot.start()

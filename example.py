from goldilocks.goldilocks import Goldilocks
from goldilocks.strategies import VariantCounterStrategy, GCRatioStrategy, NucleotideCounterStrategy, KMerCounterStrategy

#TODO Methods may take a list of locations or may need to actually analyze
#     a proper genomic sequence
"""Execute Goldilocks search."""
data = {"ONE": {1: [1,2,5]}}
g = Goldilocks(VariantCounterStrategy(), data, is_seq=False, stride=1, length=3)

candidates = g._filter("max", actual_distance=1)

print candidates

#########################################
data = {"ONE": {1: "CCCGGGAGATTT"}}
g = Goldilocks(GCRatioStrategy(), data, 3, 1)

candidates = g._filter("max", actual_distance=1)

print candidates

candidates.export_fasta(["ONE"])

#########################################
data = {"ONE": {1: "AAACCCGGGCCCGGGAGAAAAAAA"}}
g = Goldilocks(KMerCounterStrategy(["AAA", "CCC"]), data, 6, 1)

candidates = g._filter("max", actual_distance=1, track="AAA")

print candidates

candidates.export_fasta("ONE")
g.export_meta("ONE", sep="\t")

#########################################
data = {
    "ONE": {
        1: "ANAGGGANACAN",
        2: "ANAGGGANACAN",
        3: "ANANNNANACAN"
    },
    "TWO": {
        1: "ANAGGGANACAN",
        2: "ANAGGGANACAN",
        3: "ANANNNANACAN"
    }
}
g = Goldilocks(NucleotideCounterStrategy(["N"]), data, 3, 1)
print g.groups
candidates = g._filter("max")

candidates.export_fasta(["ONE", "TWO"], filename="example", divide=True)
candidates.export_fasta()

candidates = g._filter("min", limit=0,
        exclusions={
            # Filter any region with a starting position <= 3 AND an ending postion >= 4
            0: {
                "start_lte": 3,
                "end_gte": 4
            },

            # Filter anything from Chrm1
            1: {
                "chr": True
            },

            # Filter any region with an ending postion >= 9
            3: {
                "start_gte": 9
            }
        }, use_and=True)
print candidates
candidates.export_fasta("ONE")

#########################################
data = {
    "ONE": {
        1: "ANAGGGANACANANAGGGANACANANAGGGANACANANAGGGANACANANAGGGACGCGCGCGGGGANACAN",
        2: "ANAGGCGCGCNANAGGGANACGCGGGGCCCGACANANAGGGANACANANAGGGACGCGCGCGCGCCCGACAN",
        3: "ANAGGCGCGCNANAGGGANACGCGGGGCCCGACANANAGGGANACANANAGGGACGCGCGCGCGCCCGACAN",
        4: "GCGCGCGCGCGCGCGCGGGGGGGGGCGCCGCCNNNNNNNNNNNNNNNNGCGCGCGCGCGCGCGNNNNNNNNN"
    }
}
g = Goldilocks(GCRatioStrategy(), data, 3, 1)

candidates = g._filter("min")

print candidates
g.plot("ONE")

#########################################
from Mountain.IO import fastareaders
f = fastareaders.FASTA_Library("/store/sanger/ref/hs37d5.fa1")
f.get_next()
data = {
    "ONE": {
        1: f.get_next().seq,
     }
}

# Will assume that files follow the recommendation that sequence lines
# are no longer than 80 characters
g = Goldilocks(GCRatioStrategy(), data, 1000000, 500000)

# Avoid human leukocyte antigen loci on chr6
candidates = g._filter("max", percentile_distance=10, limit=10, exclusions={"chr": [6]})

print candidates

g.plot()

#########################################
from Mountain.IO import fastareaders
f = fastareaders.FASTA_Library("/store/sanger/ref/hs37d5.fa1")
f.get_next()
data = {
    "ONE": {
        1: f.get_next().seq,
     }
}

# Will assume that files follow the recommendation that sequence lines
# are no longer than 80 characters
g = Goldilocks(KMerCounterStrategy(["AAA", "TTT", "GATTACA"]), data, 1000000, 500000)
candidates = g._filter("max", track="AAA")

print candidates

g.plot(track="AAA")

import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    the_joint_probability = 1

    for person in people: # loops through every person
        num_genes = 0 # how many genes the current person has
        if person in one_gene:
            num_genes = 1
            if people[person]['mother'] == None: # if they have no parents
                the_joint_probability *= PROBS['gene'][1] # use unconditional probability
            else: # if they have parents
                the_joint_probability *= conditional_probability(people, person, one_gene, two_genes) # use conditional probability
        elif person in two_genes:
            num_genes = 2
            if people[person]['mother'] == None: # if they have no parents
                the_joint_probability *= PROBS['gene'][2] # use unconditional probability
            else: # if they have parents
                the_joint_probability *= conditional_probability(people, person, one_gene, two_genes) # use conditional probability

        else:
            if people[person]['mother'] == None: # if they have no parents
                the_joint_probability *= PROBS['gene'][0] # use unconditional probability
            else: # if they have parents
                the_joint_probability *= conditional_probability(people, person, one_gene, two_genes) # use conditional probability

        # using num_genes (found earlier), find conditional probability of having the trait
        if person in have_trait: # if they have the trait
            the_joint_probability *= PROBS['trait'][num_genes][True]
        else: # if they don't have the trait
            the_joint_probability *= PROBS['trait'][num_genes][False]
        
    return the_joint_probability

def conditional_probability(people, person, one_gene, two_genes):
    """
    Custom function that I added.
    This function calculates the conditional probability that a child has 0, 1, or 2 genes
    (this conditional probability is dependent upon the parents).

    This function returns the calculated conditional probability.
    """
    yes_mother_prob = 0 # probability child gets gene from mother
    no_mother_prob = 0 # probability child doesn't get gene from mother
    yes_father_prob = 0 # probability child gets gene from father
    no_father_prob = 0 # probability child doesn't get gene from father

    if people[person]['mother'] in one_gene: # if mother has 1 gene
        yes_mother_prob = .5
        no_mother_prob = 1 - yes_mother_prob
    elif people[person]['mother'] in two_genes: # if mother has 2 genes
        yes_mother_prob = 1 - PROBS["mutation"]
        no_mother_prob = 1 - yes_mother_prob
    else: # if mother has 0 genes
        yes_mother_prob = 0 + PROBS["mutation"]
        no_mother_prob = 1 - yes_mother_prob

    if people[person]['father'] in one_gene: # if father has 1 gene
        yes_father_prob = .5
        no_father_prob = 1 - yes_father_prob
    elif people[person]['father'] in two_genes: # if father has 2 genes
        yes_father_prob = 1 - PROBS["mutation"]
        no_father_prob = 1 - yes_father_prob
    else: # if father has 0 genes
        yes_father_prob = 0 + PROBS["mutation"]
        no_father_prob = 1 - yes_father_prob

    if person in one_gene: # if child only has 1 gene, probability is if child gets it from the mother and not the father OR the child gets it from the father and not the mother
        return (yes_mother_prob * no_father_prob) + (yes_father_prob * no_mother_prob)
    elif person in two_genes: # if child has 2 genes, probability is if child gets it from both parents
        return yes_mother_prob * yes_father_prob
    else: # if child has 0 genes, probability is if child gets it from neither parent
        return no_mother_prob * no_father_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] / total
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] / total
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] / total

        total = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / total
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] / total


if __name__ == "__main__":
    main()

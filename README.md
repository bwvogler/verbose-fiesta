# verbose-fiesta

Appendix A. Pseudo-code for codon optimization in Gene Designer
FOR EACH A.A. sequence

   FOR EACH codon in sequence

      Select a codon randomly from the probability distribution. †

FOR EACH A.A. sequence that needs homologue (aiming/avoidance)

   Prepare homologue alignment matrix.

   Pre select codons that are (closest to/furthest from) homologue sequence.

   IF homologue dna contains unwanted restriction sites or other unwanted sequences THEN

      Ask/warn user and eliminate if necessary.

Create a Ukkonen Suffix Tree of the entire construct concatenated with its reverse compliment.

H = homologue score for all A.A. sequences that require it.

R = number of repeats over given threshold.

M = size of largest repeat.

WHILE R > 0 DO ‡

   Change a codon in the largest repeat region based on the probability distribution. †

   H new = homologue score after change.

   R new = number of repeats after change.

   M new = size of largest repeat after change.

   IF H new ≥ H AND ( R <R new OR M <M new ) THEN

      Accept change.

      H = H new

      R = R new

      M = M new

FOR EACH A.A. sequence that requires 5' translation optimization

   Create a Ukkonen Suffix Tree of the 5' end concatenated with its reverse compliment.

   Find hairpins in 5' end.

   GC goal = CG ratio wanted × 3 × number of codons being considered in 5' end.

   H = homologue score for the 5' end.

   R = number of hairpins.

   GC = total number of G's and C's in 5' end.

   WHILE R > 0 OR GC > GC goal DO ‡

      Change a random codon in 5'end based on the probability distribution. †

      H new = homologue score after change.

      R new = number of hairpins after change.

      GC new = number of G's and C's after change.

      IF H new ≥ H AND ( R new <R OR ( R new = R AND GC new <GC )) THEN

         Accept change.

         H = H new

         R = R new

         GC = GC new

FOR EACH restriction enzyme that needs to be checked for methylation

   Find methylated sites.

   WHILE still methylated DO ‡

      Change a codon in the site based on the probability distribution. †

FOR EACH restriction enzyme that needs to be avoided.

   Find restriction sites.

   WHILE restriction site still exists DO ‡

      Change a codon in the site based on the probability distribution. †

† Based on a given precompiled codon bias table.

‡ This can go on forever, must be stopped artificially after a given number of iterations

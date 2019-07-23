from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


class LeftBranchGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="movement",
                         field="syntax",
                         linguistics="island_effects",
                         uid="complex_left_branch_echoQ",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.all_safe_nouns = np.setdiff1d(self.all_nouns, self.all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, self.all_common_nouns)
        self.all_D_wh = get_all("category_2", "D_wh")
        self.which_what = np.append(get_all_conjunctive([("expression", "which")], self.all_D_wh), get_all_conjunctive([("expression", "what")], self.all_D_wh))


    def sample(self):
        # You are  petting whose dog?
        # N1  V_do V1      wh    N2

        # Whose are  you petting dog?
        # wh    V_do N1  V1      N2

        V1 = choice(self.all_non_finite_transitive_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_nouns)))
        except TypeError:
            pass
        V_do = return_aux(V1, N1, allow_negated=False)
        wh = choice(self.all_D_wh)
        try:
            N2 = choice(get_matches_of(V1, "arg_2", self.all_common_nouns))
        except TypeError:
            pass
        if N2['animate'] == "1":
            wh = choice(self.which_what)
        else:
            wh = choice(self.all_D_wh)

        data = {
            "sentence_good": "%s %s %s %s %s?" % (N1[0], V_do[0], V1[0], wh[0], N2[0]),
            "sentence_bad": "%s %s %s %s %s?" % (wh[0], V_do[0], N1[0], V1[0], N2[0]),
            "two_prefix_prefix_good": "%s %s %s %s" % (N1[0], V_do[0], V1[0], wh[0]),
            "two_prefix_prefix_bad": "%s %s %s %s" % (wh[0], V_do[0], N1[0], V1[0]),
            "two_prefix_word": N2[0]
        }
        return data, data["sentence_good"]

generator = LeftBranchGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

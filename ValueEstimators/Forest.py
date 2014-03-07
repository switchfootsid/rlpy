from Representations import Representation
from Representations.BinaryTree import Tree

class Forest(Representation.Representation):

    def __init__(self, domain, logger, num_trees=10, weighted=False, **kwargs):
        self.trees = [Tree(domain, logger, random_seed=i, **kwargs) for i in range(num_trees)]
        self.representation = self
        self.weighted = weighted

    @property
    def features_num(self):
        return sum((t.features_num for t in self.trees))

    @property
    def theta(self):
        return np.hstack([t.theta for t in self.trees])

    def learn(self, s, a, r, ns, terminal):
        for t in self.trees:
            t.learn(s, r, ns, terminal)

    def V(self, s, terminal, pactions):
        return self.predict(s, terminal)

    def predict(self, s, terminal=False):
        v = 0.
        w = 0.

        if self.weighted:
            for t in self.trees:
                w += 1 / (t.tderr + 1e-3)
                v += 1 / (t.tderr + 1e-3) * t.predict(s, terminal)
        else:
            for t in self.trees:
                w += 1.
                v += t.predict(s, terminal)
        return v / w

    @property
    def alpha(self):
        return self.trees[0].root.mu()

    def partitioning(self, s, terminal=False):
        if terminal:
            return self.trees[0].num_leafs
        return self.trees[0].predict_leaf_id(s, terminal) - 1

    @property
    def num_parts(self):
        return self.trees[0].num_leafs + 1

    def episodeTerminated(self):
        for t in self.trees:
            t.episodeTerminated()


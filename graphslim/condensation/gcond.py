from tqdm import trange

from graphslim.condensation.gcond_base import GCondBase
from graphslim.dataset.utils import save_reduced
from graphslim.evaluation.utils import verbose_time_memory
from graphslim.utils import *
from graphslim.models import *
from torch_geometric.utils import dense_to_sparse
from graphslim.dataset import *
from graphslim.evaluation import *
from graphslim.evaluation.utils import *
from graphslim.models import *
from torch_sparse import SparseTensor
from graphslim.dataset.convertor import ei2csr
from graphslim.utils import accuracy, seed_everything, normalize_adj_tensor, to_tensor, is_sparse_tensor, is_identity, \
    f1_macro


class GCond(GCondBase):
    """
    "Graph Condensation for Graph Neural Networks" https://cse.msu.edu/~jinwei2/files/GCond.pdf
    """
    def __init__(self, setting, data, args, **kwargs):
        super(GCond, self).__init__(setting, data, args, **kwargs)

    @verbose_time_memory
    def reduce(self, data, verbose=True):
        args = self.args
        pge = self.pge
        self.feat_syn, labels_syn = to_tensor(self.feat_syn, label=data.labels_syn, device=self.device)
        if args.setting == 'trans':
            features, adj, labels = to_tensor(data.feat_full, data.adj_full, label=data.labels_full, device=self.device)
        else:
            features, adj, labels = to_tensor(data.feat_train, data.adj_train, label=data.labels_train,
                                              device=self.device)

        # initialization the features
        feat_init = self.init()
        # self.reset_parameters()
        self.feat_syn.data.copy_(feat_init)

        adj = normalize_adj_tensor(adj, sparse=True)

        outer_loop, inner_loop = self.get_loops(args)
        loss_avg = 0
        best_val = 0
        model = eval(args.condense_model)(self.d, args.hidden,
                                          data.nclass, args).to(self.device)
        for it in trange(args.epochs):

            model.initialize()
            model_parameters = list(model.parameters())
            optimizer_model = torch.optim.Adam(model_parameters, lr=args.lr)
            model.train()

            for ol in range(outer_loop):
                adj_syn = pge(self.feat_syn)
                self.adj_syn = normalize_adj_tensor(adj_syn, sparse=False)
                model = self.check_bn(model)
                loss = self.train_class(model, adj, features, labels, labels_syn, args)
                loss_avg += loss.item()

                self.optimizer_feat.zero_grad()
                self.optimizer_pge.zero_grad()
                loss.backward()

                if it % 50 < 10:
                    self.optimizer_pge.step()
                else:
                    self.optimizer_feat.step()

                feat_syn_inner = self.feat_syn.detach()
                adj_syn_inner = pge.inference(feat_syn_inner)
                adj_syn_inner_norm = normalize_adj_tensor(adj_syn_inner, sparse=False)
                feat_syn_inner_norm = feat_syn_inner
                for j in range(inner_loop):
                    optimizer_model.zero_grad()
                    output_syn_inner = model.forward(feat_syn_inner_norm, adj_syn_inner_norm)
                    loss_syn_inner = F.nll_loss(output_syn_inner, labels_syn)
                    loss_syn_inner.backward()
                    optimizer_model.step()

            loss_avg /= (data.nclass * outer_loop)

            if it in args.checkpoints:
                self.adj_syn = adj_syn_inner
                data.adj_syn, data.feat_syn, data.labels_syn = self.adj_syn.detach(), self.feat_syn.detach(), labels_syn.detach()
                best_val = self.intermediate_evaluation(best_val, loss_avg)

        return data

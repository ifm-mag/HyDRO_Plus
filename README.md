# HyDRO
=======================================================

This repository contains implementations of:
1. Random Walk Guided Hyperbolic Graph Distillation (HyDRO)
2. Efficient and Privacy-Preserved Link Prediction via Condensed Graphs (HyDRO+)

Both methods are built upon the GraphSlim generation framework:
https://github.com/Emory-Melody/GraphSlim/tree/main

Related Papers:
- HyDRO: https://arxiv.org/abs/2501.15696
- HyDRO+: https://arxiv.org/html/2503.12156v1

Requirements
------------
- Python 3.8+
- PyTorch 1.10+
- PyTorch Geometric
- geoopt
- NetworkX
- Scipy

Installation
-----------
1. Clone the repository:
   git clone [your-repo-url]
   
2. Install dependencies:
   pip install -r requirements.txt

Experiment Scripts
-----------------
The following scripts are available in run/scripts/:

1. Core Experiments:
   - performance_HyDRO.sh: Runs HyDRO performance benchmarks
   - performance_HyDRO+.sh: Runs HyDRO+ performance benchmarks

2. Additional Analyses:
   - robustness.sh: Robustness evaluation
   - mia.sh: Membership inference attacks evaluation
   - visual.sh: Visualization scripts
   - nas.sh: Neural architecture search experiments
   - graph_property.sh: Evaluates graph property preservation

Citation
--------
If you use this work, please cite the original papers:

@article{long2025random,
  title={Random Walk Guided Hyperbolic Graph Distillation},
  author={Long, Yunbo and Xu, Liming and Schoepf, Stefan and Brintrup, Alexandra},
  journal={arXiv preprint arXiv:2501.15696},
  year={2025}
}
@article{long2025efficient,
  title={Efficient and Privacy-Preserved Link Prediction via Condensed Graphs},
  author={Long, Yunbo and Xu, Liming and Brintrup, Alexandra},
  journal={arXiv preprint arXiv:2503.12156},
  year={2025}
}

Contact
-------
For questions or issues, please contact [your-email@example.com]
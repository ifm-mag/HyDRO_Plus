# Graph Property Preservation
for dataset in citeseer cora flickr pubmed dblp; do
    python ../graph_property.py -D $dataset -W
done
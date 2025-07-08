for method in hydro; do
  for dataset in photo; do
    python ../visual.py -D $dataset -M $method -R 0.01 -W
  done
done
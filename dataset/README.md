# Dataset: email-Eu-core-temporal

## Source
- **URL**: https://snap.stanford.edu/data/email-Eu-core-temporal.html
- **Download**: https://snap.stanford.edu/data/email-Eu-core-temporal.txt.gz

## Description
The email-Eu-core-temporal dataset contains email communication records from a large European research institution. Each record represents a directed email interaction between two users with an associated Unix timestamp.

## Statistics
- **Number of users (nodes)**: 986
- **Number of temporal email events (edges)**: 332,334
- **Type**: Directed, temporal

## File Format
Each line contains three whitespace-separated values:
```
source_user_id  destination_user_id  unix_timestamp
```

### Example
```
0 1 1262454010
0 2 1262454020
1 0 1262454030
```

## Download Instructions
1. Download the compressed file:
   ```
   curl -O https://snap.stanford.edu/data/email-Eu-core-temporal.txt.gz
   ```
2. Extract using gzip (or 7-Zip on Windows):
   ```
   gzip -d email-Eu-core-temporal.txt.gz
   ```
3. Place the extracted `email-Eu-core-temporal.txt` in this `dataset/` directory.

## Citation
If using this dataset in academic work, please cite:
> Ashwin Paranjape, Austin R. Benson, and Jure Leskovec.
> "Motifs in Temporal Networks."
> Proceedings of the Tenth ACM International Conference on Web Search and Data Mining, 2017.

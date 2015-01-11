### Setup
```pip install requirements.txt```

### Basic Usage
```python compare_texts.py iterations top_words sample_size method --verbose```

##### Arguments
``` iterations ```  : number of iterations to run for each comparison. Recommended 10,000.

``` top_words ``` : test the top N words from text A against the frequencies of those words in text B.

``` sample_size ``` : percentage of the smaller text to sample (an equal number of words will be sampled from the larger text). 0 < sample_size <= 1.

``` methods ``` : (chisquare|gtest) - statistical test to use for determining text similarity.

``` --verbose ```: output additional descriptive and monitoring text during execution.

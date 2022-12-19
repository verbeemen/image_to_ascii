# Image to Ascii

TODO

# How to use?

- Load the library
- Initialize the model
  - Parameters: 
    - Define the n-gram size, The amount of characters to use for predicting the next character
    - Define a path to the corpus file
  - During initialisation, the model loads its corpus and starts calculating the probability distributions for each n-gram pair

```python

    # Import the necessary libraries
    from n_gram_text_generator.generator import NGramTextGenerator

    # Initialize the generator
    generator = NGramTextGenerator(n=4, path_corpus="./data/names.csv", seed=42)
```

## Results:
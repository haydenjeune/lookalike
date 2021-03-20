# Lookalike

Lookalike helps you to find your celebrity lookalike!

Under development - coming soon.

## The Plan

The plan is to used a pretrained facial recognition model to output a vector that encodes what a face "looks like". We can use this to generate vectors to represent many different celebrities by passing one picture for each through the model. Then, to find your lookalike celebrity, we run a picture of yours through the model, get the vector, then do a vector similarity search through the celebrity vectors to find the best match.

For now, we will use one reference picture per celebrity, and do a simple pairwise comparison using the dot product of the two vectors. After that, some ideas for future improvement are:

- Take the mean of several images of the same celebrity as the search vectors
- Use a vector similarity search library such as [Faiss](https://github.com/facebookresearch/faiss) to do efficient lookups

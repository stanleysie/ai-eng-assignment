# Stanley's Notes

## Assumptions, problem analysis, and solution approach

I started this project by understanding the codebase and actually getting the program to run, to get a sense of what has been built so far.

My currrent assumptions are:

- All reviews are valid, such as follows natural-language patterns, where we can identify the specific modications (if there are any)
- Duplicated reviews won't affect the result, or it doesn't mean that it should be prioritized over other reviews

While it is true that the existing codebase in general is working without any issue, one important improvement is to improve the prompt further to handle edge cases like multiple modifications in a single review. In particular, when there are multiple modifications (either to the instructions or ingredients) in a single review.

## Implementation details and challenges overcome

- I improved the prompt further to handle edge cases like multiple modifications in a single review.

- I added a simple Python Flask API to serve the recipe data and allowing users to try and enhance the recipe based on a single review.

- Initially thought if it's possible to generate suggestion based on multiple reviews, but this seems to be out of scope, and not really a good idea, as it might have been too complex for the LLM to handle (in terms of context length and complexity).

## Future Improvements

- We can potentially add a confidence score to each modification and maybe display it as well to the user, so that the user understands the confidence in the modification and can make a informed decision on whether to apply it or not
- We can also improve the pipeline further by actually fine-tuning a small LLM-based model to improve the modifications, given a review and a recipe

## Personal Note

I'm really sorry I didn't get to prepare a full presentation for this assignment, as something urgent came up and I had to prioritize it. I hope the codebase and the NOTES.md file are sufficient to understand the work that I've done.

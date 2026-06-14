# Evaluation Spec — Pod Classifier

Complete this spec **before** writing any code for Milestone 3.

Use Plan or Ask mode to think through each blank field. When you're done,
your answers here become the blueprint for `compute_accuracy()` and
`compute_per_class_accuracy()` in `evaluate.py`.

---

## Background: What is evaluation?

After building a classifier, we need to know how well it works. Evaluation answers:
- **Overall:** What fraction of episodes did we classify correctly?
- **Per-class:** Are we better at some labels than others?

Both functions take the same inputs: a list of predicted labels and a list of
ground-truth labels, in the same order.

---

## compute_accuracy(predictions, ground_truth)

### What it does
Returns the fraction of predictions that exactly match the ground truth.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`, one per episode. |
| `ground_truth` | `list[str]` | The correct labels, in the same order as `predictions`. |

### Output

| Return value | Type | Description |
|---|---|---|
| accuracy | `float` | A value between 0.0 and 1.0. |

---

### Spec fields — fill these in before writing code

**Formula:**

```

 The formula would be the total correct number of predictions that match the ground truth divided by the total predictions made. 

```

---

**Step-by-step logic:**

```
 1. Determine if the prediction is correct by matching it w/ the ground truth
 2. Sum the total number of correct predictions
 3. Divide the sum by the total number of predictions 
 4. Return the quotient
```

---

**Edge case — what if both lists are empty?**

```
If both lists are empty, the accuracy should be 0 since there's nothing to compare it to.
```

---

**Worked example:**

```
predictions  = ["interview", "solo", "panel", "interview"]
ground_truth = ["interview", "solo", "solo",  "narrative"]


1. Sum of correct predictions: 3
2. Divide total correct by total predictions: 3/4
3. Answer: 75%

```

---

## compute_per_class_accuracy(predictions, ground_truth)

### What it does
Returns accuracy broken down by each label. For each label in `VALID_LABELS`,
reports how many episodes with that ground-truth label were classified correctly.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`. |
| `ground_truth` | `list[str]` | Correct labels, in the same order. |

### Output

A `dict` keyed by label. Each value is a dict with three keys:

```python
{
    "interview": {"correct": int, "total": int, "accuracy": float},
    "solo":      {"correct": int, "total": int, "accuracy": float},
    "panel":     {"correct": int, "total": int, "accuracy": float},
    "narrative": {"correct": int, "total": int, "accuracy": float},
}
```

---

### Spec fields — fill these in before writing code

**What does "correct" mean for a given class?**

```
If the episode label from the predictions list matches the value in the corresponding position in the ground_truth list.

```

---

**What does "total" mean for a given class?**

```
The total is the amount of predictions for that specific label.

```

---

**Step-by-step logic:**

```
 1. Initialize the dictionary with four label keys each with a dictionary value holding 3 keys (amount of correct predictions, total predictions, and accuracy)
 2. Loop over the prediction list
 3. For each pair (predicted, truth) see if they match and if so, increment the correct key value of the dictionary
 4. After the loop update the remaining keys of the dictionary (total and the accuracy (based on the accuracy formula))
 5. Return the dictionary
```

---

**Edge case — what if a class has no examples in ground_truth (total == 0)?**

```
0.0

```

---

**Worked example:**

```
predictions  = ["interview", "interview", "solo", "panel", "panel"]
ground_truth = ["interview", "solo",      "solo", "panel", "narrative"]

[blank — fill in the per-class results table below]

label       correct  total  accuracy
----------  -------  -----  --------
interview   [blank]  [blank]  [blank]
solo        [blank]  [blank]  [blank]
panel       [blank]  [blank]  [blank]
narrative   [blank]  [blank]  [blank]
```

---

## Reflection questions (discuss at the checkpoint)

1. Your overall accuracy might be decent even if one class has very low accuracy.
   Why is per-class accuracy a more informative metric than overall accuracy alone?
   ```
      Per-class accuracy can tell us if the llm is performing better with certain type of labels than others and helps us focus on what specifically to improve one. 
   ```

2. If `panel` episodes consistently get misclassified as `interview`, what does
   that tell you about your training labels or your prompt?
   ```
   I may have more training labels of `interview` than `panel` since the llm model may have had more exposure and recognition of interviews, leading it to recognize more interview podcasts than panels.
   ```

3. You labeled 20 training episodes and evaluated on 20 test episodes (5 per class).
   How might the evaluation results change if you had labeled 100 training episodes?
   What if you had 200 test episodes?
   ```
   More training episodes may increase the accuracy of our evaluation results since the LLM model would have seen more instances of each label classications, leading to better predictions. 

   If I had 200 test episodes, for just 100, the accuracy may decrease slightly since there's a higher chance having different variances of podcasts that the llm model may not have seen based on its training data.
   
   ```

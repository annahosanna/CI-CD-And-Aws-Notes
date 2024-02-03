```
# Assumes average over a infinite number of samples unless max_count is set
really_big_float next = 0
really_big_float current = 0
int count = 0
int max_count = 0

function average(number) {
  count = count + 1
  if (max_count != 0) && (count > max_count) { count = max_count }
  next = current + (number - current)/count
  current = next
}
```

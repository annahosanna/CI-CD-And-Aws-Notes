/*
// Assumes average over a infinite number of samples unless max_count is set


// If I wanted to do this over a fixed number of samples
// then I could instead use an array
// The double looses more percision every loop but an array would not
*/

double average(double new_number, double current, long count, long max_count) {
    double next_current = 0.0;
    if (max_count != 0) && (count > max_count) { count = max_count; }
    next_current = current + (new_number - current)/count;
    return next_current;
}

int main() {
    long count = (long)0;
    count = count + (long)1;
    double new_number = 0.0;
    double current = 0.0;

    while (1) {
        count = count + 1;
        new_number = (double)count; // some function to get next new_number here
        current = average(new_number, current, count, 0);
    }
}
